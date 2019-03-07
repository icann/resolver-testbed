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
	* Settings &rarr; Pointer: PS/2 Mouse
	* Storage &rarr; Controller: IDE: Channge "empty" to attach the Debian ISO from above
	* Network &rarr; Adapter 1: Attached to "NAT"
	* Ports &rarr; USB: off

* Boot the new `debian960-base` VM
	* Use Non-graphical installation, and use the default choices other than these:
		* Hostname: debian960-base
		* Domain name: Make sure this is blank
		* Root password: BadPassword
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
	* Log in as root / BadPassword
	* `wget https://holder.proper.com/testbed-startup.sh`
	* `sh testbed-startup.sh`
	* `shutdown -h now`

## Create the host mangement network _vboxnet0_

In the Virtualbox _Host Network Manager_ create a new management network called _vboxnet0_. It should use the network 192.168.56/24 and have DHCP enabled.

## Do the Initial Setup and Sanity Checks on the Control Host

* Get the testbed repo: `git clone https://github.com/icann/resolver-testbed.git`
* Change into that directory: `cd resolver-testbed`
* Create the first two VMs by cloning from debian960-base, setting the IP addresses, and so on:
	* `./rt.py make_gateway_clone`
		* This also sets up the gateway as a NAT
	* `./rt.py make_resolvers_clone`
		* This also builds all the current resolvers; this takes 30 minutes or more
		* It is known that some of these don't build currently
* Prepare the 13 server VMs (server1-vm through server13-vm):
	* `./rt.py prepare_server_clones`
	* This takes about 20 minutes

