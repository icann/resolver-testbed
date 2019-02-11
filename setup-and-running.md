# Setting up and Running the Resolver Testbed

## Setup

The steps can be summarized as:

0. Build the base VM image in VirtualBox
0. Clone this VM for other VMs in the testbed
0. Do initial setup from the control host
0. Push configurations out to the VMs
0. Run tests

The last two steps can be repeated as the configurations change for different testing.

## Building the Base VM Image on the Control Host

* Get the recent Debiain image from `http://cdimage.debian.org/cdimage/release/current/amd64/iso-cd/debian-9.6.0-amd64-netinst.iso`

* Choose which SSH keys you will use for logging into the VMs on the testbed.
This needs to have the private key _not_ password-protected, so you might want to create a new keypair for the testbed.
To ease installation, you might put this as an authized_keys file on a locally-managed web server.

* In VirtualBox, choose File &rarr; Host Network Manager and make sure that vboxnet0 is defined. If it is not,
click the "Create" button to define it.

* Start VirtualBox
	* Machine &rarr; New
		* Name: debian960-base
		* Type: Linux
		* Version: Debian (64-bit)
		* Memory: 2048M
		* Create new virtual hard drive
			* Type: VDI
			* Storage: dynamically allocated
			* Size: 20 gig

* Before booting, change settings
	* System &rarr; Motherboard: Uncheck floppy
	* System &rarr; Motherboard: Pointing Device: PS2 Mouse, 
	* System &rarr; Processor: 2 CPUs
	* Storage &rarr; Controller: IDE: Channge "empty" to attach the Debian ISO from above
	* Network &rarr; Adapter 1: Attached to "NAT"
	* Ports &rarr; USB: off

* Boot the new `debian960-base` VM
	* Use Non-graphical installation, and use the default choices other than these:
		* Hostname: debian960-base
		* Domain name: Make sure this is blank
		* Root password: This will be used for all interaction with all VMs, so use a strong one
		* User: Any name, any password (this user will not be used in the testbed)
		* Time zone: Use your local time zone
		* Partition disks:
			* Guided - use entire disk
			* All files in one partition
		* Configure the package manager
			* No additional CDs
			* Any mirror is fine; you can use the default
			* Package user survey: No
		* Software selection
			* Unselect "Debian desktop environment"
			* Unselect "print server"
			* Select "SSH server"
			* Leave "standard system utilities" selected
		* Install GRUB to the drive you just created, /dev/sda

* After automatic reboot
	* Log in as root with the password created above
	* General machine preparation
		* `apt update`
		* `apt -y upgrade`
		* `apt -y install build-essential dnsutils git python3-pip`
		* `pip3 install fabric`
	* Get the project repo in the home directory for the root user
		* `git clone https://github.com/icann/resolver-testbed.git`
	* Set up SSH for automated logging in
		* `mkdir .ssh`
		* `chmod 700 .ssh`
		* `cd .ssh`
		* Install the authorized_keys file, possibly by getting it off of the locally-administered web server
		* `chmod 600 authorized_keys`
	* `shutdown -h now`

## Create the host mangement network _vboxnet0_

In the Virtualbox _Host Network Manager_ create a new management network called _vboxnet0_. It should use the network 192.168.56/24 and have DHCP enabled.

## Clone the Base VM Image to the Other VMs

Be sure that "Reinitialze the MAC address of all network cards" is selected when cloning the three images.

All clones are full clones because they are faster.

### Gateway VM

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: gateway-vm
	* Clone type: Full clone
* Be sure that the gateway-vm VM is selected
* Machine &rarr; Settings
	* Network &rarr; Adapter 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adapter 2: Attached to "Internal Network" _resnet_
	* Network &rarr; Adapter 3: Attached to "Internal Network" _servnet_
	* Network &rarr; Adapter 4: Attached to "NAT"
* Start the VM
* Log in as root
* Give the command `/root/resolver-testbed/vm_initial_setup.py gateway-vm`
* Reboot

### Root Servers VM

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: servers-vm
	* Clone type: Full clone
* Be sure that the servers-vm VM is selected
* Machine &rarr; Settings
	* Network &rarr; Adapter 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adapter 2: Attached to "Internal Network" _servnet_
* Start the VM
* Log in as root
* Give the command `/root/resolver-testbed/vm_initial_setup.py servers-vm`
* Reboot

### Resolver Systems

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: resolvers-vm
	* Clone type: Full clone
* Be sure that the resolvers-vm VM is selected
* Machine &rarr; Settings
	* Network &rarr; Adapter 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adapter 2: Attached to "Internal Network" _resnet_
* Start the VM
* Log in as root
* Give the command `/root/resolver-testbed/vm_initial_setup.py resolvers-vm`
* Reboot

## Do the Initial Setup and Sanity Checks on the Control Host

* Get the testbed repo: `git clone https://github.com/icann/resolver-testbed.git`
* Change into that directory: `cd resolver-testbed`
* Check that the VMs are running, and add things initially if needed: `./rt.py check_vms`
	* This builds a recent version of BIND on servers-vm to be used as the authoritative server
* Build all the resolvers on resolvers-vm: `./rt.py build_resolvers`
	* It is known that some of these don't build currently
* Prepare the servers-vm (build BIND, do initial configuration): `./rt.py prepare_servers_vm`
