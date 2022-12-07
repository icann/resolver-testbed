#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the interfaces"
cp /vagrant/files/interfaces-resolvers-vm /etc/network/interfaces || exit
echo "Set the hostname"
cp /vagrant/files/hostname-resolvers-vm /etc/hostname || exit
echo "Set the resolver"
cp /vagrant/files/resolv-with-8844 /etc/resolv.conf || exit


# XXX not needed, Vagrant sets this up
#echo "Copy the sshd config"
#cp /root/resolver-testbed-master/config-files/sshd-config /etc/ssh/sshd_config || exit

# XXX Rebooting bypasses vagrant logic; shutdown instead.
### Finish up
#echo "Rebooting in 2 seconds"
#sleep 2
#reboot

### Finish up
echo "Shutting down"
sleep 2
shutdown -h now
