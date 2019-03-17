#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the interfaces"
cp /root/resolver-testbed-master/config-files/interfaces-resolvers-vm /etc/network/interfaces || exit
echo "Set the hostname"
cp /root/resolver-testbed-master/config-files/hostname-resolvers-vm /etc/hostname || exit
echo "Set the resolver"
cp /root/resolver-testbed-master/config-files/resolv-with-8844 /etc/resolv.conf || exit
echo "Copy the sshd config"
cp /root/resolver-testbed-master/config-files/sshd-config /etc/ssh/sshd_config || exit

### Finish up
echo "Rebooting in 2 seconds"
sleep 2
reboot
