#!/usr/bin/env python3
'''
Testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files 
'''

######### Add IPv6

######### Run tests for preferred root server selection

import os, subprocess, sys, time, logging, json
import fabric

# Some program-wide constants
CLONE_BASENAME = "debian960-base"
ROOT_PASS = "BadPassword"
GUESTCONTROL_TEMPLATE = "VBoxManage --nologo guestcontrol {} --username root --password PASSWORD_GOES_HERE".replace("PASSWORD_GOES_HERE", ROOT_PASS)
RESOLVER_LIBRARIES = [
"apt update",
"apt install -y build-essential",
"apt install -y libssl-dev libcap-dev python3-ply dnsutils",
"apt install -y pkg-config libuv1-dev libcmocka-dev libluajit-5.1-dev liblua5.1-0-dev autoconf libtool liburcu-dev libgnutls28-dev libedit-dev",
"apt install -y libldns-dev libexpat-dev libboost-dev",
"apt install -y python3-pip",
"pip3 install meson",
"apt-get -y install apt-transport-https lsb-release ca-certificates wget",
"wget -O /etc/apt/trusted.gpg.d/knot-latest.gpg https://deb.knot-dns.cz/knot-latest/apt.gpg",
"sh -c 'echo \"deb https://deb.knot-dns.cz/knot-latest/ $(lsb_release -sc) main\" > /etc/apt/sources.list.d/knot-latest.list'",
"apt update",
"apt install -y libknot-dev liblmdb-dev ninja-build"
]
REMOTE_REPO = "/root/resolver-testbed-master"

VM_INFO = {
"gateway-vm": { "control_addr": "192.168.56.20" },
"resolvers-vm": { "control_addr": "192.168.56.30" },
"servers-vm": { "control_addr": "192.168.56.40" }
}

CLI_COMMANDS = [
"help",
"initial_vm_config",
"make_resolvers",
"refresh_repo",
"run_test"
]

HELP_TEXT = '''
Available commands for rt.py are:
help                   Show this text
make_resolvers         Make the resolvers on the resolvers-vm VM
refresh_repo           Update the testbed software on the VMs
run_test <testname>    Run the specified test
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
    # Run the command
    ret_main_cmd = fabconn.run(cmd_to_run, hide=True, warn=True)
    fabconn.close()
    if ret_main_cmd.failed:
        return False, "Error: {}".format(ret_main_cmd.stderr.strip())
    else:
        return True, ret_main_cmd.stdout.strip()

def cp_from_vm(file_to_get, dest_dir, vm_name):
    ''' Gets a file from a named VM. Returns success_boolean, output_text '''
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
    dest_file = "{}/{}".format(dest_dir, os.path.basename(file_to_get))    
    # Get the file
    try:
        fabconn.get(file_to_get, local=dest_file)
    except:
        log("Could not get {} from {}. Continuing.")
    fabconn.close()

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
        build_input = json.load(build_f, strict=False)
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
    # Build all the resolvers on resolvers-vm
    # Install all the stuff for building if it isn't already there
    this_ret, this_str = ssh_cmd_to_vm("apt list --installed", "resolvers-vm")
    if not this_ret:
        die("Could not run 'apt list' on resolvers-vm.")
    if not "build-essential" in this_str:
        log("Did not find build-essential on servers-vm, so installing libraries.")
        for this_line in RESOLVER_LIBRARIES:
            log("Running {}".format(this_line))
            this_ret, this_str = ssh_cmd_to_vm(this_line, "resolvers-vm")
            log("Ran {}, got {}".format(this_line, this_str))
        log("Finished instsalling libraries on resolvers-vm")
    for this_build in rt_config["build_info"]["builds"]:
        # See if it is already there
        this_ret, this_str = ssh_cmd_to_vm("ls Target/{}".format(this_build), "resolvers-vm")
        if this_ret:
            log("{} already present".format(this_build))
        else:
            log("Building {}".format(this_build))
            # Replace the make string abbreviation (starts with "!") with the full string
            build_url = rt_config["build_info"]["builds"][this_build]["url"]
            build_make_str = rt_config["build_info"]["builds"][this_build]["make_str"]
            if build_make_str.startswith("!"):
                if build_make_str in rt_config["build_info"]["templates"]:
                    build_make_str = rt_config["build_info"]["templates"][build_make_str]
                else:
                    die("{} has a make string of {}, but there is no equivalent for that.".format(this_build, build_make_str))
            this_ret, this_str = ssh_cmd_to_vm("cd {}; ./build_from_source.py '{}' '{}' '{}'"\
                .format(REMOTE_REPO, this_build, build_url, build_make_str), "resolvers-vm")
            if not this_ret:
                log("Could not build {}:\n{}\nContinuing".format(this_build, this_str))

def do_refresh_repo():
    ''' Refresh the repo software on all three VMs'''
    for this_vm in VM_INFO:
        log("Refreshing repo software in {}".format(this_vm))
        this_ret, this_str = ssh_cmd_to_vm("wget https://github.com/icann/resolver-testbed/archive/master.zip ", this_vm)
        if not this_ret:
            die("Could not wget: {}".format(this_str))
        this_ret, this_str = ssh_cmd_to_vm("rm -r {}".format(REMOTE_REPO), this_vm)
        if not this_ret:
            die("Could not remove {}: {}".format(REMOTE_REPO, this_str))
        this_ret, this_str = ssh_cmd_to_vm("unzip master.zip ", this_vm)
        if not this_ret:
            die("Could not unzip: {}".format(this_str))
        this_ret, this_str = ssh_cmd_to_vm("rm master.zip", this_vm)
        if not this_ret:
            die("Could not remove master.zip: {}".format(this_str))

def start_tcpdump_on_gateway(tcpdump_filename):
    ''' Starts tcpdump for a test run; takes the name of the file to create in /tmp '''
    this_cmd = "dtach -n /tmp/tmpsocket tcpdump -i enp0s8 -n -w /tmp/{}".format(tcpdump_filename)
    this_ret, this_str = ssh_cmd_to_vm(this_cmd, "gateway-vm")
    if not this_ret:
        die("Starting tcpdump on gateway-vm with '{}' returned '{}'.".format(this_cmd, this_str))
    return
    
def stop_tcpdump_on_gateway():
    ''' Gracefully stops any tcpdump running on gateway-vm '''
    this_ret, this_str = ssh_cmd_to_vm("ps ax | grep tcpdump", "gateway-vm")
    if not this_ret:
        die("Getting the PID of the tcpdump running on gateway-vm failed in ps: '{}'".format(this_str))
    ps_lines = []
    for this_line in this_str.splitlines():
        if not ("grep tcpdump" in this_line):
            if not ("dtach -n" in this_line):
                ps_lines.append(this_line)
    if ps_lines == []:
        die("There were no matching lines looking for tcpdump on gateway-vm.")
    if len(ps_lines) != 1:
        die("When getting the PID for tcpdump on gateway-vm, got multiple lines.\n{}".format(ps_lines))
    ps_parts = (ps_lines[0]).strip().split()
    tcpdump_pid = ps_parts[0]
    this_ret, this_str = ssh_cmd_to_vm("kill -HUP {}".format(tcpdump_pid), "gateway-vm")
    if not this_ret:
        die("Killing tcpdump running on gateway-vm failed in ps: '{}'".format(this_str))
    return

def get_pid_of_resolver(this_resolver):
    ''' Returns the PID of the named resolver running on resolvers-vm; returns nothing if it failed '''
    this_ret, this_str = ssh_cmd_to_vm("ps ax | grep Target", "resolvers-vm")
    if not this_ret:
        log("Getting the PID of the resolver failed in ps; continuing.")
        return
    ps_lines = []
    for this_line in this_str.splitlines():
        if not ("grep Target" in this_line):
            if not ("dtach -n" in this_line):
                ps_lines.append(this_line)
    if ps_lines == []:
        log("There were no matching lines looking for the running resolver; continuing.")
        return
    if len(ps_lines) != 1:
        die("When getting the PID of the resolver, got multiple lines.\n{}".format(ps_lines))
    ps_parts = (ps_lines[0]).strip().split()
    return ps_parts[0]

def do_run_test(test_name):
    ''' Run the named test against all resolvers'''
    # Read the test description
    test_dir = "config-files/{}".format(test_name)
    if not os.path.exists(test_dir):
        log("Could not find {}".format(test_dir))
        return
    test_file_name = "{}/test-config.json".format(test_dir)
    if not os.path.exists(test_file_name):
        log("Could not find {}".format(test_file_name))
        return
    test_file_f = open(test_file_name, mode="rt")
    try:
        test_description = json.load(test_file_f)
    except:
        log("Bad JSON found in {}".format(test_file_name))
        return
    # Find the target resolvers to send the queries
    if (test_description.get("targets") == None) or (test_description.get("targets") == [ "all" ]):
        these_targets = []
        for this_target in rt_config["build_info"]["builds"]:
            if test_name in rt_config["build_info"]["builds"][this_target].get("use_in_all"):
                these_targets.append(this_target)
        log("Testing {} targets".format(len(these_targets)))
    else:
        these_targets = test_description["targets"]
        for named_target in these_targets:
            if not named_target in rt_config["build_info"]["builds"]:
                die("Found target named '{}', but that doesn't exist in the main configuration.".format(named_target))
        log("Testing {} targets".format(len(these_targets)))
    # Save the filenames on gateway-vm to retrieve when done
    tcpdump_filenames = []
    # Run the tests on each resolver
    for this_resolver in these_targets:
        log("Starting test on {}".format(this_resolver))
        # Start a new tcpdump capture on middlebox-vm
        tcpdump_timestring = time.strftime("%Y-%m-%d-%H-%M")
        this_tcpdump_filename = "{}-{}-{}.pcap".format(test_name, this_resolver, tcpdump_timestring)
        start_tcpdump_on_gateway(this_tcpdump_filename)
        tcpdump_filenames.append(this_tcpdump_filename)
        # Start the resolver, including clearing out any saved state; verify that this happened
        this_start = rt_config["build_info"]["builds"][this_resolver].get("start_str")
        if not this_start:
            log("There was no start string for {}".format(this_resolver))
            pass
        else:
            if this_start.startswith("!"):
                if this_start in rt_config["build_info"]["templates"]:
                    this_start = rt_config["build_info"]["templates"][this_start]
                else:
                    die("{} has a start string of {}, but there is no equivalent for that.".format(this_resolver, this_start))
            full_start = this_start.replace("TEST_DIR", "{}/{}".format(REMOTE_REPO, test_dir))
            full_start = full_start.replace("PREFIX", "/root/Target/{}".format(this_resolver))
            log("Running {}".format(full_start))
            this_ret, this_str = ssh_cmd_to_vm(full_start, "resolvers-vm")
            if not this_ret:
                log("Running '{}' on resolvers-vm returned '{}'. Skipping.".format(full_start, this_str))
                stop_tcpdump_on_gateway()
            start_pid = get_pid_of_resolver(this_resolver)
            # Give the resolver some time to get started
            time.sleep(2)
        # Send the queries
        for this_query in test_description["queries"]:
            if len(this_query) < 2:
                die("The query '{}' was too short.".format(this_query))
            this_qname = this_query[0]
            this_time = this_query[1]
            if len(this_query) >= 3:
                this_qtype = this_query[2]
            else:
                this_qtype = "A"
            # Wait for the given time; this somewhat assumes that each query takes zero time to complete
            try:
                time_as_int = int(this_time)
            except:
                die("In the test file, a time was not convertable to an int.")
            time.sleep(time_as_int)
            # Use "dig" to send a query to 127.0.0.1
            this_dig = "dig @127.0.0.1 {} {} +short".format(this_qname, this_qtype)
            this_ret, this_str =  ssh_cmd_to_vm(this_dig, "resolvers-vm")
            if not this_ret:
                log("Dig for time {} failed. Continuing.".format(this_time))
            # Maybe process this_answer in a later version of the testbed
            log("Result for '{}': '{}'".format(this_dig, this_str))
        # Shut down the resolver; verify that this happened
        if start_pid:
            this_ret, this_str = ssh_cmd_to_vm("kill {}".format(start_pid), "resolvers-vm")
            if not this_ret:
                log("Killing {} on resolvers-test failed: '{}'".format(this_resolver, this_str))
        # Stop the tcpdump on the middlebox-vm
        stop_tcpdump_on_gateway()
    # Get the results from the middlebox-vm
    log("All tests finished, now getting saved pcaps.")
    for this_to_get in tcpdump_filenames:
        log("Getting {}".format(this_to_get))
        cp_from_vm("/tmp/{}".format(this_to_get), test_dir, "gateway-vm")
    log("Got pcaps in {}".format(test_dir))

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
    elif cmd == "refresh_repo":
        do_refresh_repo()
        log("Done refreshing the software on the VMs")
    elif cmd == "run_test":
        if len(sys.argv) < 3:
            die("Need to give a name for the test to run.") 
        test_name = sys.argv[2]
        do_run_test(test_name)
        log("Done running test {}".format(test_name))
    # We're done, so exit
    log("## Finished run")
    exit()

''' Still to do:

- Start a test on something with less tooling than resovers-vm
  - Generate a test instance name
  - Start dnstap on gateway-vm
  - Stop dnstap on gateway-vm
  - Collect the dnstap files from gateway-vm

'''
