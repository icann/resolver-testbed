#!/bin/bash

EXPIRATION_DATE="20300101"
TTL="60"

zones=(a b c d e f g h i j k l m)
for ((i = 0; i < ${#zones[@]}; ++i)); do
    x=${zones[$i]}
    ip=172.21.$(( $i + 101 )).1
    ip6=fd00::21:$(( $i + 101 )):1
    echo "Creating ${x}.zone.unsigned"
    cat>${x}.zone.unsigned<<EOF
${x}. ${TTL} IN SOA ns.${x}. admin.ns.${x} 123 1800 900 6054800 ${TTL}
${x}. ${TTL} IN NS ns.${x}.
ns.${x}. ${TTL} IN A $ip
ns.${x}. ${TTL} IN AAAA $ip6
EOF
   KEYFILE=`ls K${x}*.key`
   KEYBASE=`echo ${KEYFILE} | sed s/.key//`
   echo "Signing ${x}.zone"
   ldns-signzone -f ${x}.zone -e ${EXPIRATION_DATE} -o ${x}. ${x}.zone.unsigned ${KEYBASE}
done