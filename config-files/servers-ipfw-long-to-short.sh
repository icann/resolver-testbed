ipfw delete 50101 > /dev/null 2>&1
ipfw delete 50102 > /dev/null 2>&1
ipfw delete 50103 > /dev/null 2>&1
ipfw delete 50104 > /dev/null 2>&1
ipfw delete 50105 > /dev/null 2>&1
ipfw delete 50106 > /dev/null 2>&1
ipfw delete 50107 > /dev/null 2>&1
ipfw delete 50108 > /dev/null 2>&1
ipfw delete 50109 > /dev/null 2>&1
ipfw delete 50110 > /dev/null 2>&1
ipfw delete 50111 > /dev/null 2>&1
ipfw delete 50112 > /dev/null 2>&1
ipfw delete 50113 > /dev/null 2>&1
ipfw add 50101 pipe 101 ip from 172.21.101.1 to any
ipfw add 50102 pipe 102 ip from 172.21.102.1 to any
ipfw add 50103 pipe 103 ip from 172.21.103.1 to any
ipfw add 50104 pipe 104 ip from 172.21.104.1 to any
ipfw add 50105 pipe 105 ip from 172.21.105.1 to any
ipfw add 50106 pipe 106 ip from 172.21.106.1 to any
ipfw add 50107 pipe 107 ip from 172.21.107.1 to any
ipfw add 50108 pipe 108 ip from 172.21.108.1 to any
ipfw add 50109 pipe 109 ip from 172.21.109.1 to any
ipfw add 50110 pipe 110 ip from 172.21.110.1 to any
ipfw add 50111 pipe 111 ip from 172.21.111.1 to any
ipfw add 50112 pipe 112 ip from 172.21.112.1 to any
ipfw add 50113 pipe 113 ip from 172.21.113.1 to any
ipfw add 50201 pipe 101 ip6 from fd00::21:101:1 to any
ipfw add 50202 pipe 102 ip6 from fd00::21:102:1 to any
ipfw add 50203 pipe 103 ip6 from fd00::21:103:1 to any
ipfw add 50204 pipe 104 ip6 from fd00::21:104:1 to any
ipfw add 50205 pipe 105 ip6 from fd00::21:105:1 to any
ipfw add 50206 pipe 106 ip6 from fd00::21:106:1 to any
ipfw add 50207 pipe 107 ip6 from fd00::21:107:1 to any
ipfw add 50208 pipe 108 ip6 from fd00::21:108:1 to any
ipfw add 50209 pipe 109 ip6 from fd00::21:109:1 to any
ipfw add 50210 pipe 110 ip6 from fd00::21:110:1 to any
ipfw add 50211 pipe 111 ip6 from fd00::21:111:1 to any
ipfw add 50212 pipe 112 ip6 from fd00::21:112:1 to any
ipfw add 50213 pipe 113 ip6 from fd00::21:113:1 to any
ipfw pipe 101 config delay 1300
ipfw pipe 102 config delay 1200
ipfw pipe 103 config delay 1100
ipfw pipe 104 config delay 1000
ipfw pipe 105 config delay 900
ipfw pipe 106 config delay 800
ipfw pipe 107 config delay 700
ipfw pipe 108 config delay 600
ipfw pipe 109 config delay 500
ipfw pipe 110 config delay 400
ipfw pipe 111 config delay 300
ipfw pipe 112 config delay 200
ipfw pipe 113 config delay 100


