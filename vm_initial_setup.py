#!/usr/bin/env python3
'''
Run on freshly-made resolvers to install things that are needed
'''

import os, subprocess, sys, shutil

# Some program-wide constants
PROG_DIR = "/root/resolver-testbed"
CLONE_BASENAME = "debian960-base"
OK_VM_LIST = [ "gateway-vm", "servers-vm", "resolvers-vm" ]

def die(in_str):
    ''' log then exit  '''
    err_str = in_str + " Exiting."
    print(err_str)
    exit()

# Run the main program
if __name__ == "__main__":
    ''' Do initial setup on a VM; dies if the VM is not ready '''
    if len(sys.argv) == 1:
        die("Must give one argument: the name of this vm. Must be one of '{}'.".format(" ".join(OK_VM_LIST)))
    in_vm_name = sys.argv[1]
    if not in_vm_name in OK_VM_LIST:
        die("The argument to setup_vm must be a VM name from '{}'.".format(" ".join(OK_VM_LIST)))
    # Be sure this is running on an VM, not the control host
    this_hostname = subprocess.getoutput("hostname")
    if this_hostname != CLONE_BASENAME:
        if this_hostname in OK_VM_LIST:
            die("This host's hostname is {}, which indicates it has already been set up.".format(this_hostname))
        else:
            die("Weird: this hosts hostname is {}, which is not expected.".format(this_hostname))
    print("Setting up {}".format(in_vm_name))
    # Add the /etc/hosts/interfaces file
    this_interfaces_file = "{}/config-files/interfaces-{}".format(PROG_DIR, in_vm_name)
    if not os.path.exists(this_interfaces_file):
        die("The file {} does not exist, so cannot update this system.".format(this_interfaces_file))
    try:
        shutil.copy(this_interfaces_file, "/etc/network/interfaces")
    except:
        die("Could not copy {} to {}.".format(this_interfaces_file, "/etc/network/interfaces"))
    # For gateway-vm, cause the NAT rules to be automatically executed on startup
    if in_vm_name == "gateway-vm":
        try:
            shutil.copy("{}/config-files/nat-on-gateway-vm.sh", "/etc/rc.local")
        except:
            die("Could not copy {} to {}.".format("{}/config-files/nat-on-gateway-vm.sh", "/etc/rc.local"))
        try:
            subprocess.call("systemctl daemon-reload", shell=True)
        except:
            die("Could not run 'systemctl daemon-reload'.")
        try:
            subprocess.call("systemctl start rc-local", shell=True)
        except:
            die("Could not run 'systemctl start rc-local'.")
    # Change the hostname to this_vm for future boots
    try:
        f = open("/etc/hostname", mode="wt")
        f.write("{}\n".format(in_vm_name))
        f.close()
    except:
        die("Failed to write out /etc/hostname.")
    die("Finished setting up {}. Reboot to bring up the new settings.".format(in_vm_name))
