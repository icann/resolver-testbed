#!/usr/bin/env sh

### Copy the normal files that will be the config after reboot
echo "Copy the rc.conf"
# This sets the hostname and makes the needed sshd config
cp /root/resolver-testbed-master/config-files/servers-rc.conf /etc/rc.conf  || exit
echo "Set the resolver"
cp /root/resolver-testbed-master/config-files/resolv-with-8844 /etc/resolv.conf || exit
echo "Installing from pkg"
pkg install -y bind914 wget nano ca_root_nss  || exit
echo "Making the bind-configs"
mkdir /root/bind-configs || exit
echo "Copying root files"
cp /root/resolver-testbed-master/config-files/root-zone-basic/* /root/bind-configs || exit
echo "Copy the rc.local"
cp /root/resolver-testbed-master/config-files/servers-rc.local /etc/rc.local
echo "Setting permissions on servers-ipfw-long-to-short.sh"
chmod a+x /root/resolver-testbed-master/config-files/servers-ipfw-long-to-short.sh
echo "Making boot faster"
echo 'autoboot_delay="2"' >/boot/loader.conf

### Finish up
echo "Shutting down"
sleep 2
shutdown -p now

