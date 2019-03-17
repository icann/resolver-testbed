#!/usr/bin/env sh

VBoxManage --nologo clonevm debian960-base --name gateway-vm --register
VBoxManage --nologo modifyvm gateway-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet --nic3 intnet --intnet3 servnet --nic4 nat
VBoxManage --nologo modifyvm gateway-vm  --cpus 2 --memory 1024
VBoxManage --nologo clonevm debian960-base --name resolvers-vm --register
VBoxManage --nologo modifyvm resolvers-vm --nic1 hostonly --hostonlyadapter1 vboxnet0 --nic2 intnet --intnet2 resnet
VBoxManage --nologo modifyvm resolvers-vm --cpus 2 --memory 2048
VBoxManage --nologo startvm gateway-vm
VBoxManage --nologo startvm resolvers-vm

