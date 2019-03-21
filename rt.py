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
ROOT_PASS = "BadPassword"
GUESTCONTROL_TEMPLATE = "VBoxManage --nologo guestcontrol {} --username root --password PASSWORD_GOES_HERE".replace("PASSWORD_GOES_HERE", ROOT_PASS)
RESOLVER_LIBRARIES = [
"apt install -y build-essential"
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
"gateway-vm": { "control_addr": "192.168.56.20" },
"resolvers-vm": { "control_addr": "192.168.56.30" },
"servers-vm": { "control_addr": "192.168.56.40" }
}

CLI_COMMANDS = [
"help",
"initial_vm_config",
"make_resolvers"
]

HELP_TEXT = '''
Available commands for rt.py are:
help                   Show this text
make_resolvers_clone   Make the resolvers-vm VM
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

def ssh_cmd_to_vm(cmd_to_run, vm_name):
    ''' Runs a command on a named VM. Returns success_boolean, output_text '''
    if not vm_name in VM_INFO:
        die("Attempt to run on {}, which is not a valid VM".format(vm_name))
    is_vm_running(vm_name)
    this_control_address = (rt_config["vm_info"][vm_name]).get("control_addr")
    if not this_control_address:
        die("There was no address for {}".format(vm_name))
    fabconn = fabric.Connection(host=this_control_address, user="root", connect_kwargs= {"password": ROOT_PASS})
    try:
        fabconn.open()
    except Exception as this_e:
        die("Could not open an SSH connection to {} on {}: '{}'.".format(vm_name, this_control_address, this_e))
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

def send_with_guestcontrol(this_cmd):
    ''' Send a message and look for the response; die if it failed '''
    p = subprocess.Popen(this_cmd, shell=True)
    ret_val = p.wait()
    if ret_val > 0:
        die("Failed run '{}'.".format(this_cmd))
    
def is_vm_running(vm_name):
    ''' Check if the VM is running; die if not '''
    p = subprocess.Popen("VBoxManage --nologo list runningvms", stdout=subprocess.PIPE, shell=True)  
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
        p = subprocess.Popen("VBoxManage --nologo startvm {} --type headless".format(vm_name), stdout=subprocess.PIPE, shell=True)  
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

def do_make_resolvers():
    ''' Make the resolvers_vm '''
    this_vm = "resolvers-vm"
    # Build all the resolvers on resolvers-vm
    # Install all the stuff for building if it isn't already there
    this_ret, this_str = ssh_cmd_to_vm("apt list --installed", "resolvers-vm")
    if not this_ret:
        die("Could not run 'apt list' on resolvers-vm.")
    if not "libknot" in this_str:
        log("Did not find libknot on servers-vm, so installing libraries.")
        for this_line in RESOLVER_LIBRARIES:
            this_ret, this_str = ssh_cmd_to_vm(this_line, "resolvers-vm")
        log("Finished instsalling libraries on resolvers-vm")
    for this_build in rt_config["build_info"]["builds"]:
        # See if it is already there
        this_ret, this_str = ssh_cmd_to_vm("ls Target/{}".format(this_build), "resolvers-vm")
        if this_ret:
            log("{} already present".format(this_build))
        else:
            log("Building {}".format(this_build))
            this_ret, this_str = ssh_cmd_to_vm("cd /root/resolver-testbed; ./build_from_source.py {}".format(this_build), "resolvers-vm")
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
    elif cmd == "make_resolvers":
        do_make_resolvers()
        log("Done making the resolvers")
    # We're done, so exit
    log("## Finished run")
    exit()

''' Still to do:
- Work on building multiple knot-resolver versions
  - RESOLVER_LIBRARIES needs to be fixed because libknot needs to be done version-by-version. The current only works for 3.7 and above

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
