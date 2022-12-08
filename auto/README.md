Work In Progress for further automating the testbed with Vagrant and Ansible
============================================================================

Notes
-----
Requires VirtualBox, Vagrant and Ansible to be already installed on the system.

For now bullet point documentation follows.

Current implementation
----------------------
- Configure inventory/host_vars/VBox-host; either specify an existing one or
  the new one to be created by VirtualBox.
  Current configuration is for testing on the same VirtualBox installation as
  the old testbed so vboxnet1 with 192.168.57.0/24.
- `ansible-playbook playbooks/setup_VirtualBox.yml`; this will setup the
  configured vboxnet and DHCP server.
- `vagrant up`; this will fetch the images (boxes), configure them, bring them
  up and provision their initial networking configuration.
- servers-vm (FreeBSD) takes a lot of time for _initial_ boot; it seems to be
  installing itself.
  Vagrant may timeout while trying to connect.
  **If that happens**, after the VM is ready (try with `vagrant ssh servers-vm`)
  issue `vagrant reload --provision servers-vm` to continue initial provisioning.
- VMs will be shutdown after initial provisioning for configuration to take
  effect with the next boot; `vagrant up` to bring them up.
- Further interaction with the VMs should only be done through vagrant cli.

TODO
----
- Check Ansible inventory variable inheritance together with Vagrant inventory
- Compile the resolver software in parallel on the resolvers-vm with Ansible
- Run the tests and properly clean up if the test is cancelled midway
- vboxnetN is probably not needed anymore since we rely on Vagrant for
  connecting to the VMs.
- One place configuration instead of hunting values in different files?
  Mainly because two different tools are used (Vagrant and Ansible).
  ~Idea: Jinja templating before starting anything i.e., to generate Vagrantfile
  and host_vars?~
  Another idea: Vagrantfile is plain ruby; the Ansible inventory can be the
  canonical configuration place and Vagrantfile just reads those YAML files.
  Some host_vars values will only be relevant for vagrant but that is fine.
