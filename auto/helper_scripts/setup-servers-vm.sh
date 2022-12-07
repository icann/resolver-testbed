#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the rc.conf"
# This sets the hostname and makes the needed sshd config
cp /vagrant/files/servers-rc.conf /etc/rc.conf  || exit
echo "Set the resolver"
cp /vagrant/files/resolv-with-8844 /etc/resolv.conf || exit

# XXX This can happen later with Ansible
#echo "Installing from pkg"
#pkg install -y bind916 wget nano ca_root_nss  || exit
#echo "Making the bind-configs"
#mkdir /root/bind-configs || exit
#echo "Copying root files"
#cp /vagrant/files/root-zone-basic/* /root/bind-configs || exit
#echo "Copy the rc.local"
#cp /vagrant/files/servers-rc.local /etc/rc.local
#echo "Setting permissions on servers-ipfw-long-to-short.sh"
# XXX Need to first copy this to /root; don't touch the repo file
#chmod a+x /vagrant/files/servers-ipfw-long-to-short.sh

echo "Making boot faster; always autoboot"
echo 'autoboot_delay="-1"' >/boot/loader.conf

### Finish up echo "Shutting down"
sleep 2
shutdown -p now
