Work In Progress for further automating the testbed with Vagrant and Ansible
============================================================================

Notes
-----
Requires VirtualBox, Vagrant and Ansible to be already installed on the system.

For now bullet point documentation follows.

Current implementation
----------------------
- Configure `ansible/host_vars/VBox-host`; either specify an existing one or
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
- VMs **need** to be reloaded for possible OS changes to take effect with
  `vagrant reload`.
- If system changes are needed in the future, after editing the relevant files,
  run `vagrant provision` followed by `vagrant reload`.
- Provision the resolvers-vm and gateway-vm with
  `ansible-playbook ansible/provision_resolvers-vm.yml` and
  `ansible-playbook ansible/provision_gateway-vm.yml`.
- Further interaction with the VMs should only be done through vagrant cli.

TODO
----
- Figure out if vagrant can not delete entries from the inventory upon shutdown.
- Compile the resolver software in parallel on the resolvers-vm with Ansible
- Run the tests and properly clean up if the test is cancelled midway
- vboxnetN is probably not needed anymore since we rely on Vagrant for
  connecting to the VMs.
- [DONE] Check Ansible inventory variable inheritance together with Vagrant inventory
- [DONE] One place configuration instead of hunting values in different files?
  Mainly because two different tools are used (Vagrant and Ansible).
  ~Idea: Jinja templating before starting anything i.e., to generate Vagrantfile
  and host_vars?~
  Another idea: Vagrantfile is plain ruby; the Ansible inventory can be the
  canonical configuration place and Vagrantfile just reads those YAML files.
  Some host_vars values will only be relevant for vagrant but that is fine.

NOTES
-----
- There is a dependency on the ansible utils plugin, which needs to be
  installed with: `ansible-galaxy collection install ansible.utils`
- The bridge_net or BRIDGE_NET VirtualBox network is only necessary on our
  FreeBSD machine where VirtualBox NAT doesn't work. To run this on different
  systems, there should be no nic5 and no nic4 in gateway-vm and resolvers-vm.
  I commented out the following network items:
  - `enp0s16` in `auto/ansible/host_vars/gateway-vm`, and
  - `enp0s10` in `auto/ansible/host_vars/resolvers-vm`.

