# Setting up and Running the Resolver Testbed

## Setup

The steps can be summarized as:

0. Build the base VM image in VirtualBox
0. Clone this VM for other VMs in the testbed
0. Do initial setup from the control host
0. Push configurations out to the VMs
0. Run tests

The last two steps can be repeated as the configurations change for different testing.

## Create the host mangement network _vboxnet0_

In the Virtualbox _Host Network Manager_ create a new management network called _vboxnet0_. It should use the network 192.168.56/24 and have DHCP enabled.

## Build the Debian base VM image

Because the middlebox-vm and resolvers-vm VMs are both based on Debian, build a base VM
that will be cloned into the two VMs.

* Get the recent Debiain image from `http://cdimage.debian.org/cdimage/release/current/amd64/iso-cd/debian-9.6.0-amd64-netinst.iso`

* In VirtualBox, choose File &rarr; Host Network Manager and make sure that vboxnet0 is defined. If it is not,
click the "Create" button to define it.

* Start VirtualBox
	* Machine &rarr; New
		* Name: debian960-base
		* Type: Linux
		* Version: Debian (64-bit)
		* Memory: 2048M  (Changed from default of 1024)
		* Create new virtual hard drive
			* Type: VDI
			* Storage: dynamically allocated
			* Size: 20 gig (Changed from default of 8 gig)

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
	* `apt install unzip`
	* `unzip master.zip`
	* `rm master.zip`
	* `shutdown -h now`

* Create the two clones with commands on the control host
	* `VBoxManage --nologo clonevm debian960-base --name gateway-vm --register`
	* `VBoxManage --nologo modifyvm gateway-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet --nic3 intnet --intnet3 servnet --nic4 nat`
	* `VBoxManage --nologo modifyvm gateway-vm  --cpus 2 --memory 1024`
	* `VBoxManage --nologo clonevm debian960-base --name resolvers-vm --register`
	* `VBoxManage --nologo modifyvm resolvers-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet`
	* `VBoxManage --nologo modifyvm resolvers-vm --cpus 2 --memory 2048`

## Do the initial setup for resolvers-vm and the middlebox-vm

* Get the testbed repo on the control host: `git clone https://github.com/icann/resolver-testbed.git`
* Change into that directory: `cd resolver-testbed`
* Create the first two VMs by cloning from debian960-base, setting the IP addresses, and so on:
	* `./rt.py make_gateway_clone`
		* This also sets up the gateway as a NAT
	* `./rt.py make_resolvers_clone`
		* This also builds all the current resolvers; this takes 30 minutes or more
		* It is known that some of these don't build currently

## Build the servers-vm VM

* Start VirtualBox
	* Machine &rarr; New
		* Name: servers-vm
		* Type: BSD
		* Version: FreeBSD (64-bit)
		* Memory: 1024M
		* Create new virtual hard drive
			* Type: VDI
			* Storage: dynamically allocated
			* Size: 16 gig

* Before booting, change settings
	* Storage &rarr; Controller: IDE: Channge "empty" to attach the FreeBSD ISO from above
	* Network &rarr; Adapter 1: Attached to "NAT"
	* Ports &rarr; USB: off

* Boot the new `servers-vm` VM
	* Select Install
	* Continue with default keymap
	* Hostname: freebsd12-base
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
		* Change to "BSD labels"
		* Use default layout
		* Finish and commit
	* (Lots of packages are then downloaded)
	* Root password: BadPassword
	* Time zone: UTC, but you don't need to set the time
	* System configuration: leave sshd and dumpdev selected
	* No system hardening
	* Do not add additional users (only root is used in the testbed)
	* Apply system configuration and exit installer
	* Select manual configuration to get a shell
		* `fetch http://holder.proper.com/freebsd12-testbed-startup.sh`
		* `shutdown -p now`
	* In VirtualBox, unmount the CD-ROM
		* In the window for the VM, select the second icon from the left (the CD-ROM), and select Remove disc from virtual drive

* Create the VM
	* `VBoxManage --nologo clonevm freebsd12-base --name servers-vm --register`
	* `VBoxManage --nologo startvm servers-vm`
	* Log in as root / BadPassword
	* `sh ./freebsd12-testbed-startup.sh`
	* `shutdown -p now`

* Set up the interfaces
	* `VBoxManage --nologo modifyvm servers-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 servnet`
	* `VBoxManage --nologo startvm servers-vm`

