# Setting up and Running the Resolver Testbed

## Setup

The steps can be summarized as:

0. Build the base VM image in VirtualBox
0. Clone this VM for other VMs in the testbed
0. Push configurations out to the VMs
0. Run tests

The last two steps can be repeated as the configurations change for different testing.

## Building the Base VM Image

* Get the recent Debiain image from `http://cdimage.debian.org/cdimage/release/current/amd64/iso-cd/debian-9.6.0-amd64-netinst.iso`

* Choose which SSH keys you will use for logging into the VMs on the testbed.
This needs to have the private key _not_ password-protected, so you might want to create a new keypair for the testbed.
To ease installation, you might put this as an authized_keys file on a locally-managed web server.

* Start Virtualbox
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
	* Network &rarr; Adatper 1: Attached to "Bridged Adapter" on the NIC for your computer that leads to the Internet
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
			* Any mirror is fine; Use the default
			* Popularity contest: No
		* Software selection
			* Unselect "Debian desktop environment"
			* Unselect "print server"
			* Select "SSH server"
			* Leave "standard system utilities" selected

* After automatic reboot
	* Log in as root with the password created above
	* General machine preparation
		* `apt update`
		* `apt -y upgrade`
		* `apt -y install build-essential git`
	* Get the project repo so that the VMs can be set up easily
		* `git clone https://github.com/icann/resolver-testbed.git`
	* Set up SSH for automated logging in
		* `mkdir .ssh`
		* `chmod 700 .ssh`
		* `cd .ssh`
		* Install the authorized_keys file, possibly by getting it off of the locally-administered web server
		* `chmod 600 authorized_keys`
	* `shutdown -h now`

## Clone the Base VM Image to the Other VMs

All clones are full clones because they are faster.

### Gateway VM

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: gateway-vm
	* Clone type: Full clone
* Machine &rarr; Settings
	* Network &rarr; Adatper 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adatper 2: Attached to "Internal Network" _resnet_
	* Network &rarr; Adatper 3: Attached to "Internal Network" _servnet_
	* Network &rarr; Adatper 4: Attached to "Bridged Adapter" on the NIC for your computer that leads to the Internet

### Root Servers VM

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: servers-vm
	* Clone type: Full clone
* Machine &rarr; Settings
	* Network &rarr; Adatper 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adatper 2: Attached to "Internal Network" _servnet_

### Resolver Systems

* Select debian96-base in the VirtualBox UI
* Machine &rarr; Clone
	* Name: resovers-vm
	* Clone type: Full clone
* Machine &rarr; Settings
	* Network &rarr; Adatper 1: Attached to "Host-only Adapter" _vboxnet0_
	* Network &rarr; Adatper 2: Attached to "Internal Network" _resnet_

