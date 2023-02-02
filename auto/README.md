# Work In Progress for further automating the testbed with Vagrant and Ansible


## Notes

Requires VirtualBox, Vagrant and Ansible to be already installed on the system.

For now bullet point documentation follows.

## Current implementation


### Virtual Box configuration


- Configure `ansible/host_vars/VBox-host`; either specify an existing host-only
  interface or _the_ new one to be created by VirtualBox.
  Current configuration is for testing on the same VirtualBox installation as
  the old testbed so vboxnet1 with 192.168.57.0/24.
- `ansible-playbook ansible/setup_VirtualBox.yml`; this will setup the
  configured vboxnet and DHCP server.

### VM creation and network provisioning


- `vagrant up`; this will fetch the images (boxes), configure them and bring
  them up.
- servers-vm (FreeBSD) takes a lot of time for _initial_ boot; it seems to be
  installing itself.
  Vagrant may timeout while trying to connect.
  **If that happens**, just reissue `vagrant up` to make sure the VMs are up.
- VMs **need** to be provisioned for their initial network/system configuration.
  Do that with `ansible-playbook ansible/network_provision_*`; _it will
  shutdown the VMs when done_.
- Bring the VMs up again with `vagrant up`. This will make sure the system
  configuration changes that were made, will take effect regardless of OS
  services peculiarities.
- If system changes are needed in the future, after editing the relevant files,
  run `ansible-playbook ansible/network_provision_*` followed by `vagrant up`.
- Further interaction with the Virtual Box VMs should only be done through the
  Vagrant cli to allow Vagrant specific actions to take effect.
- Changing the box configuration (e.g., adding more CPU, memory, interfaces)
  requires a simple `vagrant reload`. This will shutdown the box and bring it
  up with updated resources.

### Regular provisioning


- Provision the VMs with `ansible-playbook ansible/provision_*`. This will
  ensure that the VMs are always in a predictable state and updated with the
  latest configuration changes.

### Local extra configuration

It is possible to include extra configuration and hosts that are not part of
this testbed.

You can use `.local_config.yml` for extra settings; have a look at `.local_config.yml.sample`.

If you specify extra inventory, you would need to also change the shipped
`ansible.cfg` file to reflect those changes, or point to a different one with
the `ANSIBLE_CONFIG` environmnet variable.

### Destroying VMs

- `vagrant destroy` destroys everything; you can specify specific VMs if needed
  and the additional `-f` option gets rid of the confirmation.
- If cloning is used (by default currently), the master VM needs to be manually
  deleted from VirtualBox as well.
- Vagrant keeps downloaded boxes around. To free disk space check which ones
  are currently there with `vagrant box list` and remove with
  `vagrant box remove ...`.
- If cloning is used (by default currently), and the VM is not part of
  VirtualBox but Vagrant still has the initial box around it keeps some
  information around and older Vagrant versions may complain that the master VM
  is not present. To solve this, manually remove
  `~/.vagrant.d/boxes/<box>/<version>/virtualbox/master_id`

### Testing connectivity

There are currently 2 connectivity tests available:
- ping from resolvers-vm to the servers-vm
- ping from resolvers-vm to all the IPs defined for the group root_servers

When all relevant VMs are up and network provisioned, you can run the following
playbooks respectively:
```
ansible-playbook ansible/test_resolvers_servers_connectivity.yml
ansible-playbook ansible/test_resolvers_root_connectivity.yml
```

These ensure that the separate nodes in the different networks can reach each
other through the gateway-vm.

NOTE: Testing of the NAT networking (first interface on each VM) is implicitly
checked by Vagrant while powering up the VM.


## TODO

- [DONE] Compile the resolver software in parallel on the resolvers-vm with Ansible
  - pdns 4.1.15 and knots are not compiling yet
- Run the tests and properly clean up if the test is cancelled midway
- vboxnetN is probably not needed anymore since we rely on Vagrant for
  connecting to the VMs.
- [DONE] We can have cloned Virtual Boxes by using `v.linked_clone = true` in the
  virtualbox configuration. Not done at the moment because we are actively
  still testing and Vagrant does not destroy the master VM when the last cloned
  VM is destroyed. For cleaner environment now, useful when we need to spin up
  identical boxes.
- [DONE] Check Ansible inventory variable inheritance together with Vagrant inventory
- [DONE] One place configuration instead of hunting values in different files?
  Mainly because two different tools are used (Vagrant and Ansible).
  ~Idea: Jinja templating before starting anything i.e., to generate Vagrantfile
  and host_vars?~
  Another idea: Vagrantfile is plain ruby; the Ansible inventory can be the
  canonical configuration place and Vagrantfile just reads those YAML files.
  Some host_vars values will only be relevant for vagrant but that is fine.
- [DONE] Figure out if vagrant can not delete entries from the inventory upon
  shutdown; can't find an option/workaround. Vagrant provisioning is stripped
  to the bare minimum for the auto-generated inventory to be created.

## NOTES

- There is a dependency on the ansible utils plugin, which needs to be
  installed with: `ansible-galaxy collection install ansible.utils`
- The bridge_net or BRIDGE_NET VirtualBox network is only necessary on our
  FreeBSD machine where VirtualBox NAT doesn't work. To run this on different
  systems, there should be no nic5 and no nic4 in gateway-vm and resolvers-vm.
  Following network interfaces are custom for our FreeBSD shared infra:
  - `enp0s16` in `auto/ansible/host_vars/gateway-vm`, and
  - `enp0s10` in `auto/ansible/host_vars/resolvers-vm`.
  we will replace this with something more generic soonish.
- VM state must not be altered outside of Vagrant. It will bypass Vagrant
  specific actions like sharing the current directory with the VM and making
  sure the NAT SSH forwarding works.
  - Shutting down is allowed but needs to be followed by `vagrant up`.
  - Rebooting is forbidden.
