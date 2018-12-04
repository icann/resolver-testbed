#!/usr/bin/env python3
'''
Run on freshly-made resolvers to install things that are needed
'''

import os, subprocess, sys

# Some program-wide constants
PROG_DIR = os.path.abspath(os.getcwd())
CLONE_BASENAME = "debian960-base"

# Run the main program
if __name__ == "__main__":
    ''' Do initial setup on a VM; dies if the VM is not ready '''
    in_vm_name = sys.argv[1]
    ok_vm_list = [ "gateway-vm", "servers-vm", "control_addr" ]
    if not in_vm_name in ok_vm_list:
        exit("The argument to setup_vm must be a VM name from '{}'".format(" ".join(ok_vm_list)))
    # Be sure this is running on an VM, not the control host
    this_hostname = subprocess.getoutput("hostname")
    if this_hostname != CLONE_BASENAME:
        if this_hostname in ok_vm_list:
            exit("This host's hostname is {}, which indicates it has already been set up.".format(this_hostname))
        else:
            exit("Weird: this hosts hostname is {}, which is not expected.".format(this_hostname))
    print("Setting up {}".format(in_vm_name))
    # Change the hostname to this_vm
    # Add the /etc/hosts/interfaces file
    # Do VM-specific setup
