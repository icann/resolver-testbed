# Resolver Testbed

This repo describes a testbed to test various DNS resolvers.
The purpose of the testbed is to allow researchers to set up many resolvers and run tests on each.
For example, a test might see what the resolver emits when it is priming, or when
it is responding to a particular query while using DNSSEC validation.

The project is sponsored by ICANN.

For information on the project, please contact [Paul Hoffman](mailto:paul.hoffman@icann.org).

## Installation and Requirements

The testbed has been tested on Ubuntu workstation (and derivatives like Xubuntu),
as well as MacOS.

Install the testbed by cloning from GitHub at <https://github.com/icann/resolver-testbed>.

You need to have Python 3 installed.

VMs are kept in [VirtuaBox](https://www.virtualbox.org/).
On Ubuntu hosts, use `sudo apt install -y virtualbox` instead of installing from the software store.

The VMs are all accessed using the "root" user only.

@@ More requirements here

## Running

The steps can be summarized as:

0. Build the base VM image in VirtualBox
0. Get, build, and install all the open source resolvers
0. Design and run some tests

### Building the base VM image

@@ FIX THESE @@

* Get the Ubuntu 16.04.3 server image from `http://mirror.us.leaseweb.net/ubuntu-releases/16.04.3/ubuntu-16.04.3-server-amd64.iso`

* Start the Virtualbox image using this server image
	* Name: restest1604
	* Memory: 2048M
	* Drive: VMDK, dynamically-allocated, 40 gig

* Settings changes:
	* System->Motherboard: PS2 Mouse
	* System->Processor: 2 CPUs (or more, if you can afford it)
	* Audio: off
	* USB: off

* Boot Ubuntu 16.04.3
	* Hostname: vagrant-box
	* User "vagrant", pass "vagrant" (this is the default for Vagrant)
	* Guided, use entire disk
	* No automated updates
	* OpenSSH server

* Setup after first boot
	* `sudo visudo`
         *`vagrant ALL=(ALL) NOPASSWD: ALL`
	* `sudo apt update`
	* `sudo apt -y upgrade`
	* `sudo apt install -y linux-headers-$(uname -r) build-essential dkms`
	* GUI Devices -> Insert Guest Additions CD (will need to be downloaded)
	* `sudo mount /dev/cdrom /media/cdrom`
	* `sudo sh /media/cdrom/VBoxLinuxAdditions.run`
	* `sudo reboot`
	* `mkdir .ssh`
	* `chmod 700 .ssh`
	* `cd .ssh`
	* Install the very unsafe but needed Vagrant public key: `wget https://github.com/hashicorp/vagrant/blob/master/keys/vagrant.pub`
	* `mv vagrant.pub authorized_keys`
	* `chmod 600 authorized_keys`
	* `sudo nano /etc/sysctl.conf` and add `net.ipv6.route.max_size = 64000` to the bottom
	* `sudo nano /etc/apt/apt.conf.d/10periodic` to set `Update-Package-Lists` to `0` to reduce DNS queries from the system
	* `sudo shutdown -h now`

### Set up the VMs in the testbed

@@ STUFF GOES HERE

## Configuration

The configuration is kept in JSON in a file called `config_for_resolver_test.json`.
That file is a JSON object that contains four other objects:

* `builds` – Descriptions of how to get and build each open source package, and tags
for grouping the builds. For example:

		"unbound-1.6.4":
			{ "tags": [ "unbound", "recent" , "oct" ],
			"url": "http://unbound.net/downloads/unbound-1.6.4.tar.gz",
			"base": "common",
			"conf_type": "unbound",
			"make_str": "!unboundmake",
			"desc": "",
			"start": "!unboundstart"
			},

* `templates` – Text that is often repeated in `builds`, such as how to make a particular
package and how to start it in the VM.

* `bases` - A description of each VM. In the current implementation of the testbed, all
open source goes into one base, called `common`. You could, if you want, create different
VMs for different builds.

* `tests` – Each test has a name, and an object that gives various attributes. Currently,
the only attribute is `on-vm`, which is the name of a program that will run on the VM
each time a test is run on a particular build. These are usually simple shell scripts,
often with a `dig` command or something similar.

## Running Tests

@@ STUFF GOES HERE

## License

See the `LICENSE` file.

