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

You need to have Python3 installed.

The testbed automates tests using [Vagrant](https://www.vagrantup.com/).
Install Vagrant from <https://www.vagrantup.com/downloads.html>; use 2.0.0 or later.
For example, use:

     wget https://releases.hashicorp.com/vagrant/2.0.0/vagrant_2.0.0_x86_64.deb
     sudo dpkg -i vagrant_2.0.0_x86_64.deb

VMs are kept in [VirtuaBox](https://www.virtualbox.org/).
On Ubuntu hosts, use `sudo apt install -y virtualbox` instead of installing from the software store.

The testbed automatically launches `tcpdump` under `sudo` when running tests,
so `sudo` access is required.

The testbed uses `dig` to add marker requests in the `tcpdump` output, so
either BIND or bindutils must be installed.

The testbed uses `wget` to download the source for the various open source
software, and unbundles the sources with `tar`, so they must be installed.

You also need to have BIND utilities such as named-checkconf and dnssec-keygen installed;
this is usually done by installing "bindutils" or "bind9" from your packaging system.

The user on the host must be able to `sudo` with no password prompt because the testing uses tcpdump.

## Running

The steps can be summarized as:

0. Build the base VM image in VirtualBox
0. Use this vase VM to create a Vagrant box
0. Get, build, and install all the open source resolvers
0. Design and run some tests

### Building the base VM image

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

### Creating the Vagrant box

On the host, give the following commands to turn the VirtualBox VM into a Vagrant box:

* `vagrant package --base restest1604 --out restest1604-package.box`
* `vagrant box add -name restest1604 restest1604-package.box`

### Set up the VMs in the testbed

* `cd /path/to/resolver-testbed`
* `./resolver_test.py update_sources` to get all the source tarballs.
* `./resolver_test.py make_bases` to make all the bases for VMs. This might take an hour.
* `./resolver_test.py build all` to make each source package in the VirtualBox VM. This can take many hours; maybe run this under nohup.

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

Each test must be named in the configuration file. The configuration files are copied into
the Vagrant environment for each build and used for configuration.

For each test for each type of resolver, there must be
file in the Tests/ directory that has the form X-Y.conf, where X matches the `conf_type` listed in the
`builds` section of the configuration file, and Y matches the test name. Thus, for example,
to run the test "t1" against a build whose `conf_type` is "bind9", there must be a file in
the Tests/ directory called "bind9-t1.conf".

Note that the configurations can refer to other files. For example, in the default Tests/
directory, there are subdirectories called oct10/ and oct11/ which have files that have additional
files needed for the configurations, such as zone files.

## License

See the `LICENSE` file.

