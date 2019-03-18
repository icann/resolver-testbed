#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the rc.conf"
# This sets the hostname and makes the needed sshd config
cp /root/resolver-testbed-master/config-files/servers-rc.conf /etc/rc.conf
echo "Set the resolver"
cp /root/resolver-testbed-master/config-files/resolv-with-8844 /etc/resolv.conf

##### Still need to install and set up BIND for authoritative

### Finish up
echo "Rebooting in 2 seconds"
sleep 2
reboot
