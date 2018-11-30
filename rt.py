#!/usr/bin/env python3
'''
Testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import glob, json, os, shutil, subprocess, sys, time, logging
import fabric

# Constants
PROG_DIR = os.getcwd()
LOG_FILE = "{}/Local/log_resolver_testbed.txt".format(PROG_DIR)
RESOLVER_TEST_LOWEST_BASE = "restest1604"
PROVISION_FILE = "run_at_start.sh"
TCPDUMP_PREFIX = "tcpdump -i"
SUDO_NOHUP_TCPDUMP_PREFIX = "sudo nohup tcpdump -i"
VM_CONFIG = "{}/config_for_vms.json".format(PROG_DIR)
BUILD_CONFIG = "{}/config_for_rt_builds.json".format(PROG_DIR)

HELP_TEXT = '''
Available commands are:
help:           Show this text
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
    ''' show some help text to the user '''
    print(HELP_TEXT)

def cmd_to_vm(cmd_to_run, vm_target):
    ''' Runs a command on a named VM. Returns list of [ success_boolean, output_text ] '''
    if not vm_target in vm_info:
        die("Attempt to run on {}, which is not a valid VM".format(vm_target))
    if vm_target == "resolvers-vm":
        is_resolvers_vm_running()
    ######## More goes here

def is_resolvers_vm_running():
    ''' Check if the resolvers-vm is running; die if not '''
    ############ More goes here

def initialize_control_host():
    ''' Make sure everything on the control host is set up; might die if it can't '''
    ############### More goes here

def config_from_json(in_file):
    ''' Return the object in a JSON file '''
    if not os.path.exists(in_file):
        die("Could not find {}.".format(in_file))
    f = open(in_file, mode="rt")
    try:
        this_config = json.load(f)
        return this_config
    except:
        die("Could not parse the JSON in {}.".format(in_file))
    ################ More goes here

def run_main():
    ''' The main program; always exits '''
    log("## Starting run on date {}".format(time.strftime("%Y-%m-%d")))
    # Parse the input
    if len(sys.argv) < 2:
        show_help()
        die("There were no arguments on the command line.")
    # Make sure that vboxmanage is available
    try:
        subprocess.check_call("VBoxManage --version", shell=True)
    except:
        die("Could not run VBoxManage at start of program.")
    # Get the configuration for VMs
    vm_info = config_from_json(VM_CONFIG)
    initialize_control_host()  # Make sure everything is set up correctly
    # Make sure the needed VMs are running
    for this_vm_name in vm_info:
        try:
            subprocess.check_call("VBoxManage showvminfo {}".format(this_vm_name))
        except:
            die("Could not find {} in the VirtualBox inventory.".format(this_vm_name))
    ##### More goes here
    # Get the command
    cmd = sys.argv[1]
    cmd_args = sys.argv[2:]
    log("Command was {} {}".format(cmd, " ".join(cmd_args)))
    # Figure out which command it was
    if cmd == "help":  # Help
        show_help()
    else:
        log("'{}' is not a valid command.".format(cmd))
        show_help()
    # We're done, so exit
    exit()

# Run the main program
if __name__ == "__main__":
    run_main()
