#!/usr/bin/env python3
'''
Testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import os, subprocess, sys, time, logging, configparser
import fabric

# Some program-wide constants
PROG_DIR = os.path.abspath(os.getcwd())
LOG_FILE = "{}/log_resolver_testbed.txt".format(PROG_DIR)
LOCAL_CONFIG = "{}/local_config.txt".format(PROG_DIR)
BUILD_CONFIG = "{}/build_config.json".format(PROG_DIR)

VM_INFO = {
    "gateway-vm": {
        "control_addr": "192.168.56.2"
    },
    "servers-vm": {
        "control_addr": "192.168.56.3"
    },
    "resovers-vm": {
        "control_addr": "192.168.56.4"
    }
}

CLI_COMMANDS = [
"help",
"setup_vm"
]

HELP_TEXT = '''
Available commands for rt.py are:
help                 Show this text
setup_vm <vmname>    Sets up a VM for the first time;
                     must be run as roon on the VM itself
'''.strip()

# Do very early check for contents of the directory that we're running in
if not os.path.exists("{}/Local".format(PROG_DIR)):
    exit("The current directory does not have a Local/ subdirectory, which is needed for logs and other files. Exiting.")
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
    exit()

def show_help():
    print(HELP_TEXT)

def cmd_to_vm(cmds_to_run, vm_name):
    ''' Runs a list of commands on a named VM. Returns list of [ success_boolean, output_text ] '''
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
        die("Could not open an SSH connection to {}.".format(vm_name))
    # Is this the right VM?
    try:
        ret_text = fabconn.run("hostname")
    except Exception as this_e:
        die("Could not run hostname on {}: '{}'".format(vm_name, this_e))
    if ret_text.strip() != vm_name:
        die("The host at {} is not {}: '{}'".format(this_control_address, vm_name, ret_text.strip()))
    # Find the commands
    #   The argument can be a list or a string
    if isinstance(cmds_to_run, list):
        commands_list = cmds_to_run
    elif isinstance(cmds_to_run, str):
        commands_list = [ cmds_to_run ]
    else:
        die("The command going to cmd_to_vm has to be a list or a string.")
    # Run the commands
    for this_command in commands_list:
        try:
            ret_text = fabconn.run(this_command)
        except Exception as this_e:
            die("Could not run '{}' on {}: '{}'".format(this_command, vm_name, this_e))

def is_vm_running(vm_name):
    ''' Check if the VM is running; die if not '''
    p = subprocess.Popen("VBoxManage runningvms", stdout=subprocess.PIPE, shell=True)  
    ret_val = p.wait()
    if ret_val > 0:
        die("VBoxManage runningvms failed to run.")
    the_running_vms = (p.stdout.read()).decode("latin-1").strip().split()
    if not vm_name in the_running_vms:
        die("{} is not in the list of running VMs: '{}'.".format(vm_name, " ".join(the_running_vms)))

def startup_and_config():
    ''' Make sure everything on the control host is set up correctly, and die if it is not; returns local configuration '''
    # Be sure we are running from the directory the program is in
    if sys.argv[0] != "./rt.py":
        die("This program must be run as ./rt.py so that all the additional files are found.")
    # Make sure certain files exist
    for this_file in [LOCAL_CONFIG, BUILD_CONFIG]:
        if not os.path.exists(this_file):
            die("{} was not found, but that file is needed.".format(this_file))
    # Parse the configuration
    c = configparser.ConfigParser()
    try:
        c.read(LOCAL_CONFIG)
    except:
        die("The configuration in {} was malformed.".format(LOCAL_CONFIG))
    if not "resolver" in c.sections:
        die("The configuration in {} does not have a [resolver]section.".format(LOCAL_CONFIG))
    this_local_config = {}
    for this_key in c["resolver"]:
        this_local_config[this_key] = c["resolver"][this_key]
    # Be sure the required configuration bits are there
    if not this_local_config.get("local_internet_interface"):
        die("The configuration in {} did not include a local_internet_interface item.".format(LOCAL_CONFIG))
    if this_local_config["local_internet_interface"]:
        die("The configuration in {} had a blank local_internet_interface item.".format(LOCAL_CONFIG))
    # Make sure that vboxmanage is available
    try:
        subprocess.check_call("VBoxManage --version", shell=True)
    except:
        die("Could not run VBoxManage during sanity check.")
    # Make sure the three VMs at least exist
    for this_vm_name in VM_INFO:
        try:
            subprocess.check_call("VBoxManage showvminfo {}".format(this_vm_name))
        except:
            die("Could not find {} in the VirtualBox inventory.".format(this_vm_name))
    # Add VM_INFO to the local configuration
    this_local_config["vm_info"] = {}
    for this_key in VM_INFO:
        this_local_config["vm_info"][this_key] = VM_INFO[this_key]
    # Finish up initialization
    return this_local_config

def do_setup_vm(this_vm):
    ''' Do initial setup on a VM; dies if the VM is not ready '''
    if this_vm == "" or (" " in this_vm):
        die("The setup_vm command takes one argument: the name of the VM")
    vm_list = (rt_config["vm_info"]).keys()
    if not this_vm in vm_list:
        die("The argument to setup_vm must be a VM name from '{}'".format(" ".join(vm_list)))
    ######### More here
    # Change the hostname to this_vm
    # Add the /etc/hosts/interfaces file
    # Do VM-specific setup
    

# Run the main program
if __name__ == "__main__":
    log("## Starting run on date {}".format(time.strftime("%Y-%m-%d")))
    # Parse the input
    if len(sys.argv) < 2:
        show_help()
        die("There were no arguments on the command line.")
    rt_config = startup_and_config()  # Get the config, and make sure everything is set up correctly
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
    elif cmd == "setup_vm":
        do_setup_vm(cmd_args)
    # We're done, so exit
    exit()
