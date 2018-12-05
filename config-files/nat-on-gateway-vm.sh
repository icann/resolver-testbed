# Be sure forwarding is on
sysctl -q net.ipv4.ip_forward=1

# Clear old settings
iptables -F
iptables -t nat -F
iptables -t mangle -F
iptables -X

# Be sure lo is allowed
iptables -A INPUT -i lo -j ACCEPT

# Set the forwarding
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i enp0s10 -o enp0s8 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i enp0s10 -o enp0s9 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i enp0s8 -o enp0s10 -j ACCEPT
iptables -A FORWARD -i enp0s9 -o enp0s10 -j ACCEPT

# Turn on NAT
iptables -t nat -A POSTROUTING -o enp0s10 -j MASQUERADE

