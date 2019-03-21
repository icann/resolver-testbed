#!/usr/bin/env sh

echo "Cloning and starting gateway-vm"
VBoxManage --nologo clonevm debian960-base --name gateway-vm --register || exit
VBoxManage --nologo modifyvm gateway-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet --nic3 intnet --intnet3 servnet --nic4 nat || exit
VBoxManage --nologo modifyvm gateway-vm  --cpus 2 --memory 1024 || exit
VBoxManage --nologo startvm gateway-vm || exit

echo "Cloning and starting resolvers-vm"
VBoxManage --nologo clonevm debian960-base --name resolvers-vm --register || exit
VBoxManage --nologo modifyvm resolvers-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet || exit
VBoxManage --nologo modifyvm resolvers-vm --cpus 2 --memory 2048 || exit
VBoxManage --nologo startvm resolvers-vm || exit

echo "Configuring and starting servers-vm"
VBoxManage --nologo modifyvm servers-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 servnet || exit
VBoxManage --nologo modifyvm servers-vm --cpus 2 --memory 2048 || exit
VBoxManage --nologo startvm servers-vm || exit
