# Setting up and Running the Resolver Testbed

## Setup

The steps can be summarized as:

1. Install and configure VirtualBox and get the testbed software
0. Build and configure the base VM images in VirtualBox
0. Run tests

## Install VirtualBox

VirtualBox can be downloaded from `https://www.virtualbox.org/wiki/Downloads`. 

In the Virtualbox _Host Network Manager_ create a new management network called _vboxnet0_. It should use the network 192.168.56/24 and have DHCP enabled.

The control host also needs to have Python 3 installed. It also needs Fabbic (`https://fabfile.org`) for Python 3; Fabric is best installed with `pip3 install fabric`.

## Get a local copy of the testbed software

* `wget https://github.com/icann/resolver-testbed/archive/master.zip`
* `unzip master.zip`
* `rm master.zip`

## Build the base VM for gateway-vm and resolvers-vm VMs

Because the gateway-vm and resolvers-vm VMs are both based on Debian, build a base VM
that will be cloned into the two VMs.

* Get a Debiain Buster image from `https://cdimage.debian.org/mirror/cdimage/release/10.0.0/amd64/iso-cd//debian-10.0.0-amd64-netinst.iso`
                                    
* In VirtualBox, choose File &rarr; Host Network Manager and make sure that vboxnet0 is defined. If it is not,
click the "Create" button to define it.

* Start VirtualBox
	* Machine &rarr; New
		* Name: debian100-base
		* Type: Linux
		* Version: Debian (64-bit)
		* Memory: 2048M  (Changed from default of 1024)
		* Create new virtual hard drive
			* Type: VDI
			* Storage: dynamically allocated
			* Size: 20 gig (Changed from default of 8 gig)

* Before booting, change settings
	* System &rarr; Pointer: PS/2 Mouse
	* Storage &rarr; Controller: IDE: Change "empty" to attach the Debian ISO from above
	* Network &rarr; Adapter 1: Attached to "NAT"
	* Ports &rarr; USB: off

* Boot the new `debian100-base` VM
	* Use Non-graphical installation (the "Install" option), and use the default choices other than these:
		* Hostname: debian100-base
		* Domain name: Make sure this is blank
		* Root password: BadPassword
		* User: Any name, any password (this user will not be used in the testbed)
		* Time zone: Pick any time zone
		* Partition disks:
			* Guided - use entire disk
			* All files in one partition
		* Configure the package manager
			* No additional CDs
			* Use the default mirror
			* Package user survey: No
		* Software selection
			* Unselect "Debian desktop environment"
			* Unselect "print server"
			* Select "SSH server"
			* Leave "standard system utilities" selected
		* Install GRUB to the drive you just created, /dev/sda

* After automatic reboot
	* Log in as root / BadPassword
	* `wget https://github.com/icann/resolver-testbed/archive/master.zip`
	* `apt install -y unzip`
	* `unzip master.zip`
	* `rm master.zip`
	* `shutdown -h now`

## Build the servers-vm VM

In the instructions below, you tell VirtualBox that the system will be a Linux Debian system even though
it will really be a FreeBSD system. This is necessary due to a recent bug in the way FreeBSD is installed
on VirtualBox VMs.

* Get a FreeBSD 12.0 image from `https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/12.0/FreeBSD-12.0-RELEASE-amd64-bootonly.iso`

* Start VirtualBox
	* Machine &rarr; New
		* Name: servers-vm
		* Type: Linux
		* Version: Debian (64-bit)  (Note that this is incorrect, but needed)
		* Memory: 1024M
		* Create new virtual hard drive
			* Type: VDI
			* Storage: dynamically allocated
			* Size: 8 gig

* Before booting, change settings
	* System &rarr; Pointer: PS/2 Mouse
	* Storage &rarr; Controller: IDE: Change "empty" to attach the FreeBSD ISO from above
	* Network &rarr; Adapter 1: Attached to "NAT"
	* Ports &rarr; USB: off

* Boot the new `servers-vm` VM
	* Select Install
	* Continue with default keymap
	* Hostname: servers-vm
	* Optional system components: leave as-is
	* Networking
		* em0
		* Configure IPv4
		* Use DHCP
		* Don't configure IPv6
		* Leave resolver configuration as-is from DHCP
	* Use main package mirror
	* Partitioning:
		* Auto (UFS)
		* Entire disk
		* Change to "BSD labels" (instead of the default MS-DOS)
		* Use default layout
		* Finish and commit
	* (Lots of packages are then downloaded and unpacked)
	* Root password: BadPassword
	* Time zone: UTC, but you don't need to set the time
	* System configuration: leave sshd and dumpdev selected
	* No system hardening
	* Do not add additional users (only root is used in the testbed)
	* Apply system configuration and exit installer
	* Select manual configuration to get a shell
		* `shutdown -p now`
* In VirtualBox, unmount the CD-ROM
	* Storage &rarr; Controller: IDE: Select the FreeBSD ISO, then under Optical Drive, select "Remove Disk from Virtual Drive"
* Start the VM up again. In the servers-vm window
	* Log in as root / BadPassword
	* `fetch --no-verify-peer https://github.com/icann/resolver-testbed/archive/master.zip`
	* `unzip master.zip`
	* `rm master.zip`
	* `sh /root/resolver-testbed-master/config-files/setup-servers-vm.sh`
	* This will shutdown when finished

## Create the clones for gateway-vm and resolvers-vm

* On the control host, change into the directory for the testbed
	* `cd resolver-testbed`
* The following does the necessary VirtualBox steps to clone the VMs
	* `sh config-files/clone-testbed-vms.sh`
* The gateway VM needs another adapter, NIC4, to be configured
	* In VirtualBox, select "gateway-vm" in the list on the left and select Machine &rarr; Settings &rarr; Network
	* In Adapter 4, select "Enable Network Adapter", set "Attached to" "Bridged Adapter", and under "Name" choose the adapter on your
	  system that is connected to the outside Internet connection and a DHCP server for IPv4 and automatic configuration for IPv6.

## Initial configuration for the VMs

* Start gateway-vm, resolvers-vm, and servers-vm by selecting them and clicking the "Start" button.

* In the gateway-vm window
	* Log in as root / BadPassword
	* `sh /root/resolver-testbed-master/config-files/setup-gateway-vm.sh`

* In the resolvers-vm window
	* Log in as root / BadPassword
	* `sh /root/resolver-testbed-master/config-files/setup-resolvers-vm.sh`

* In the servers-vm window
	* Log in as root / BadPassword

## Build the resolvers on resolvers-vm

* On the control host
	* `./rt.py make_resolvers`
	* This also builds all the current resolvers; this takes 30 minutes or more

