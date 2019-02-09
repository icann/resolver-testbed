#!/usr/bin/env python3
'''
Testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import os, subprocess, sys, time, logging, json
import fabric

# Some program-wide constants
CLONE_BASENAME = "debian960-base"
SERVER_LIBRARIES = [
    "apt-get -y install apt-transport-https lsb-release ca-certificates wget",
    "wget -O /etc/apt/trusted.gpg.d/knot-latest.gpg https://deb.knot-dns.cz/knot-latest/apt.gpg",
    "sh -c 'echo \"deb https://deb.knot-dns.cz/knot-latest/ $(lsb_release -sc) main\" > /etc/apt/sources.list.d/knot-latest.list'",
    "apt update",
    "apt install -y libknot-dev",
    "apt install -y libssl-dev libcap-dev",
    "apt install -y pkg-config libuv1-dev libcmocka-dev libluajit-5.1-dev liblua5.1-0-dev autoconf libtool liburcu-dev libgnutls28-dev libedit-dev",
    "apt install -y libldns-dev libexpat-dev libboost-dev"
]

VM_INFO = {
    "gateway-vm": {
        "control_addr": "192.168.56.2"
    },
    "servers-vm": {
        "control_addr": "192.168.56.3"
    },
    "resolvers-vm": {
        "control_addr": "192.168.56.4"
    }
}

CLI_COMMANDS = [
"help",
"check_vms",
"prepare_servers_vm",
"build_resolvers"
]

HELP_TEXT = '''
Available commands for rt.py are:
help                 Show this text
check_vms            Run simple checks on the VMs
prepare_servers_vm   Set up the servers_vm
build_resolvers      Build all resolvers on the resolvers-vm
'''.strip()

# Do very early check for contents of the directory that we're running in
LOG_FILE = "{}/log_resolver_testbed.txt".format(os.path.abspath(os.getcwd()))
LOG_FORMAT = logging.Formatter("%(message)s")
LOG_HANDLER = logging.FileHandler(LOG_FILE)
LOG_HANDLER.setFormatter(LOG_FORMAT)
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
LOG.addHandler(LOG_HANDLER)

def log(in_str):
	''' Prints a message and logs it, but only if the message is non-null; returns nothing '''
	if not in_str:
		return
	out = "{}: {}".format(time.strftime("%H-%M-%S"), in_str)
	LOG.info(out)
	print(out)

def die(in_str):
    ''' log then exit  '''
    err_str = in_str + " Exiting."
    log(err_str)
    sys.exit(1)

def show_help():
    print(HELP_TEXT)

def cmd_to_vm(cmd_to_run, vm_name):
    ''' Runs a command on a named VM. Returns success_boolean, output_text '''
    if not vm_name in VM_INFO:
        die("Attempt to run on {}, which is not a valid VM".format(vm_name))
    is_vm_running(vm_name)
    this_control_address = (rt_config["vm_info"][vm_name]).get("control_addr")
    if not this_control_address:
        die("There was no address for {}".format(vm_name))
    fabconn = fabric.Connection(host=this_control_address, user="root")
    try:
        fabconn.open()
    except:
        die("Could not open an SSH connection to {} on {}.".format(vm_name, this_control_address))
    # Is this the right VM?
    ret_hostname = fabconn.run("hostname", hide=True)
    if ret_hostname.failed:
        die("Could not run hostname on {}".format(vm_name))
    ret_text = ret_hostname.stdout
    if ret_text.rstrip() != vm_name:
        die("The host at {} is not {}: '{}'".format(this_control_address, vm_name, ret_text))
    # Run the command
    ret_main_cmd = fabconn.run(cmd_to_run, hide=True, warn=True)
    if ret_main_cmd.failed:
        return False, "Error: {}".format(ret_main_cmd.stderr.strip())
    else:
        return True, ret_main_cmd.stdout.strip()
    fabconn.close()

def is_vm_running(vm_name):
    ''' Check if the VM is running; die if not '''
    p = subprocess.Popen("VBoxManage list runningvms", stdout=subprocess.PIPE, shell=True)  
    ret_val = p.wait()
    if ret_val > 0:
        die("VBoxManage runningvms failed to run.")
    running_vms_lines = (p.stdout.read()).decode("latin-1").strip().split("\n")
    running_vms = []
    for this_line in running_vms_lines:
        running_vms.append(this_line[1:this_line.find('"', 2)])
    if not vm_name in running_vms:
        log("{} is not in the list of running VMs: '{}'.".format(vm_name, " ".join(running_vms)))
        log("Attempting to start {}".format(vm_name))
        p = subprocess.Popen("VBoxManage startvm {} --type headless".format(vm_name), stdout=subprocess.PIPE, shell=True)  
        ret_val = p.wait()
        if ret_val > 0:
            die("VBoxManage startvm did not start {}: {}.".format(vm_name, (p.stdout.read()).decode("latin-1")))      

def startup_and_config_general():
    ''' Make sure everything on the control host is set up correctly, and die if it is not; returns local configuration '''
    # Get the directory in which rt.py is
    path_to_rt = os.path.abspath(os.path.split(sys.argv[0])[0])
    # Make sure that vboxmanage is available
    p = subprocess.Popen("VBoxManage --version >/dev/null 2>/dev/null", shell=True)
    ret_val = p.wait()
    if ret_val > 0:
        die("Could not run VBoxManage during sanity check.")
    # Make sure the three VMs at least exist
    for this_vm_name in VM_INFO:
        p = subprocess.Popen("VBoxManage showvminfo {} >/dev/null 2>/dev/null".format(this_vm_name), shell=True)
        ret_val = p.wait()
        if ret_val > 0:
            die("Could not find '{}' in the VirtualBox inventory.".format(this_vm_name))
    # Keep the configuration info here; this could expand in the future
    this_local_config = {}
    # Add VM_INFO to the local configuration
    this_local_config["vm_info"] = {}
    for this_key in VM_INFO:
        this_local_config["vm_info"][this_key] = VM_INFO[this_key]
    build_config_file = "{}/build_config.json".format(path_to_rt)
    # Add build_config_file to the local configuration
    try:
        build_f = open(build_config_file, mode="rt")
    except:
        die("Could not find {}".format(build_config_file))
    try:
        build_input = json.load(build_f)
    except:
        die("The JSON in {} is broken.".format(build_config_file))
    # Sanity check the input
    if not (("builds" in build_input) and ("templates" in build_input)):
        die("{} does not have the right components.".format(build_config_file))
    this_local_config["build_info"] = build_input
    # Finish up initialization
    return this_local_config

def do_check_vms():
    ''' See if the VMs are running and have the expected things on them; fix silently if that's easy, otherwise die '''
    for this_vm in rt_config["vm_info"]:
        log("Starting sanity check on {}".format(this_vm))
        is_vm_running(this_vm)
        # On servers-vm and resolvers-vm, install all the stuff for building if it isn't already there
        if this_vm in ("servers-vm", "resolvers-vm"):
            this_ret, this_str = cmd_to_vm("apt list --installed", this_vm)
            if not this_ret:
                die("Could not run 'apt list' on {}.".format(this_vm))
            if not "libknot" in this_str:
                log("Did not find libknot on servers-vm, so installing libraries.")
                for this_line in SERVER_LIBRARIES:
                    this_ret, this_str = cmd_to_vm(this_line, this_vm)
                log("Finished instsalling libraries on {}".format(this_vm))

def do_prepare_servers_vm():
    ''' On the servers_vm, set up BIND, configure the first test-root, and start up BIND '''
    # Build BIND if it is not already there
    this_ret, this_str = cmd_to_vm("ls /root/Target/bind-9.12.3", "servers-vm")
    if not this_ret:
        log("bind-9.12.3 does not exist on servers-vm, building now, may take a few minutes.")
        this_ret, this_str = cmd_to_vm("cd /root/resolver-testbed; ./build_from_source.py bind-9.12.3", "servers-vm")
        if not this_ret:
            die("Could not build bind-9.12.3: {}".format(this_str))
    root_zone_basic_dir = "/root/resolver-testbed/config-files/root-zone-basic"
    # Be sure that root_zone_basic_dir exists before doing more
    this_ret, this_str = cmd_to_vm("ls {}".format(root_zone_basic_dir), "servers-vm")
    if not this_ret:
        die("Did not find {} or servers-vm; this indicates that the repo was not correct.".format(root_zone_basic_dir))
    root_bind_configs = "/root/bind-configs"
    # create /root/bind-configs on servers-vm if it isn't already there, then clear it and put the needed files in it and fix the config
    this_ret, this_str = cmd_to_vm("mkdir {}".format(root_bind_configs), "servers-vm")
    # Ignore the errors, because it might already be there
    this_ret, this_str = cmd_to_vm("rm -r {}/*".format(root_bind_configs), "servers-vm")
    # Ignore the errors, because it might already be empty
    # Copy all the files, even though only some are needed
    this_ret, this_str = cmd_to_vm("cp {}/* {}/".format(root_zone_basic_dir, root_bind_configs), "servers-vm")
    if not this_ret:
        die("Copying files from {} to {} failed: {}.".format(root_zone_basic_dir, root_bind_configs, this_str))
    sed_cmd = "sed 's/SOME_DIRECTORY_GOES_HERE/\/root\/bind-configs/' {0}/named.conf >/tmp/named.conf ; mv /tmp/named.conf {0}/named.conf".format(root_bind_configs)
    this_ret, this_str = cmd_to_vm(sed_cmd, "servers-vm")
    if not this_ret:
        die("Running sed to change the directory name failed: {}.".format(this_str))
    # Launch BIND
    bind_start = "/root/Target/bind-9.12.3/sbin/named -c {}/named.conf".format(root_bind_configs)
    this_ret, this_str = cmd_to_vm(bind_start, "servers-vm")
    if not this_ret:
        die("Starting BIND as {} failed: {}.".format(bind_start, this_str))

def build_all_resolvers():
    ''' Build all the resolvers on resolvers-vm '''
    for this_build in rt_config["build_info"]["builds"]:
        # See if it is already there
        this_ret, this_str = cmd_to_vm("ls Target/{}".format(this_build), "resolvers-vm")
        if this_ret:
            log("{} already present".format(this_build))
        else:
            log("Building {}".format(this_build))
            this_ret, this_str = cmd_to_vm("cd /root/resolver-testbed; ./build_from_source.py {}".format(this_build), "resolvers-vm")
            if not this_ret:
                log("Could not build {}:\n{}\nContinuing".format(this_build, this_str))   

# Run the main program
if __name__ == "__main__":
    log("## Starting run on date {}".format(time.strftime("%Y-%m-%d")))
    # Parse the input
    if len(sys.argv) < 2:
        show_help()
        die("There were no arguments on the command line.")
    rt_config = startup_and_config_general()  # Get the config, and make sure everything is set up correctly
    # Get the command
    cmd = sys.argv[1]
    cmd_args = sys.argv[2:]
    log("Command was {} {}".format(cmd, " ".join(cmd_args)))
    if not cmd in CLI_COMMANDS:
        show_help()
        die("{} is not valid command.".format(cmd))
    # Figure out which command it was
    if cmd == "help":
        show_help()
    elif cmd == "check_vms":
        do_check_vms()
        log("VMs are running as expected")
    elif cmd == "prepare_servers_vm":
        do_prepare_servers_vm()
        log("servers_vm is now set up")
    elif cmd == "build_resolvers":
        build_all_resolvers()
        log("Done building resolvers")
    # We're done, so exit
    log("## Finished run")
    exit()

''' Still to do:
- Work on building multiple knot-resolver versions
  - SERVER_LIBRARIES needs to be fixed because libknot needs to be done version-by-version. The current only works for 3.7 and above

- Set up the servers on servers-vm
  - Modify the root zone to nclude a test TLD that can be used to be sure that the resolver is going to the testbed root servers
  - Create new DNSSEC keys and sign
  - Create the necessary BIND configuration for this new zone and keys

- Start a test on resovers-vm
  - Be sure that the resolver cache is empy
  - Generate a test instance name
  - Start dnstap on gateway-vm
  - Start the test
  - During the test, collect cache dumps
  - During the test, collect system log changes
  - Finish the test
  - Stop dnstap on gateway-vm
  - Collect the dnstap files from gateway-vm
  
- Start a test on something with less tooling than resovers-vm
  - Generate a test instance name
  - Start dnstap on gateway-vm
  - Stop dnstap on gateway-vm
  - Collect the dnstap files from gateway-vm

'''
