#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the interfaces"
cp /vagrant/files/interfaces-gateway-vm /etc/network/interfaces || exit
echo "Set the hostname"
cp /vagrant/files/hostname-gateway-vm /etc/hostname || exit
echo "Set the resolver"
cp /vagrant/files/resolv-with-8844 /etc/resolv.conf || exit

# XXX not needed, Vagrant sets this up
#echo "Copy the sshd config"
#cp /vagrant/files/sshd-config /etc/ssh/sshd_config || exit

# XXX will be done later with ansible
### Install additional things needed
#echo "Getting things from apt"
#apt update; apt install -y tcpdump dtach iptables

# XXX will be done later with ansible
### Stuff specific to the gateway-vm
#echo "Make /etc/rc.local to do NAT"
#cp /vagrant/files/rc-local-on-gateway-vm /etc/rc.local || exit
#echo "Setting to runnable"
#chmod u+x /etc/rc.local || exit
#echo "Do daemon-reload"
#systemctl daemon-reload || exit

# XXX Rebooting bypasses vagrant logic; shutdown instead.
### Finish up
#echo "Rebooting in 2 seconds"
#sleep 2
#reboot

echo "Shutting down"
sleep 2
shutdown -h now
