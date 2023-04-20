KSK_ALGO=8
KSK_SIZE=2048
ZSK_ALGO=8
ZSK_SIZE=2048
NET_ZSK_ALGO=8
NET_ZSK_SIZE=1280

INCEPTION =20230101000000
EXPIRATION=20330101000000

ROOT_SOA_TTL=86400
ROOT_NS_TTL=518400
ROOT_DEL_NS_TTL=172800
ROOT_DEL_DS_TTL=86400
NET_SOA_TTL=900
NET_NS_TTL=172800
NET_DEL_NS_TTL=172800
NET_DEL_DS_TTL=86400
ROOT_SERVERS_SOA_TTL=3600000
ROOT_SERVERS_NS_TTL=3600000
ROOT_SERVERS_DEL_NS_TTL=$(NET_DEL_NS_TTL)
ROOT_SERVERS_DEL_DS_TTL=$(NET_DEL_DS_TTL)

NET_NS_DNAME="a.some-servers.net."
NET_NS_IPv4="185.49.142.30"
NET_NS_IPv6="2a04:b907::30"

DEV_RANDOM=/dev/urandom

KEYS_DIR=keys
KEYS_MKDIR=$(KEYS_DIR)/.mkdir

ROOT_DNAME=
ROOT_DOWNLOAD=downloads/root.zone
ROOT_UNSIGNED=unsigned/root
ROOT_KSK=$(KEYS_DIR)/K$(ROOT_DNAME).ksk
ROOT_ZSK=$(KEYS_DIR)/K$(ROOT_DNAME).zsk
ROOT_KSK_FILES=$(ROOT_KSK).key $(ROOT_KSK).private $(ROOT_KSK).ds
ROOT_ZSK_FILES=$(ROOT_ZSK).key $(ROOT_ZSK).private
ROOT_KEYS=$(ROOT_KSK) $(ROOT_ZSK)
ROOT_KEY_FILES=$(ROOT_KSK_FILES) $(ROOT_ZSK_FILES)

ROOT_SERVERS_NET_DNAME=root-servers.net
ROOT_SERVERS_NET_DOWNLOAD=downloads/$(ROOT_SERVERS_NET_DNAME).zone
ROOT_SERVERS_NET_UNSIGNED=unsigned/$(ROOT_SERVERS_NET_DNAME)
ROOT_SERVERS_NET_KSK=$(KEYS_DIR)/K$(ROOT_SERVERS_NET_DNAME).ksk
ROOT_SERVERS_NET_ZSK=$(KEYS_DIR)/K$(ROOT_SERVERS_NET_DNAME).zsk
ROOT_SERVERS_NET_DS=$(ROOT_SERVERS_NET_KSK).ds
ROOT_SERVERS_NET_KSK_FILES=$(ROOT_SERVERS_NET_KSK).key $(ROOT_SERVERS_NET_KSK).private $(ROOT_SERVERS_NET_DS)
ROOT_SERVERS_NET_ZSK_FILES=$(ROOT_SERVERS_NET_ZSK).key $(ROOT_SERVERS_NET_ZSK).private
ROOT_SERVERS_NET_KEYS=$(ROOT_SERVERS_NET_KSK) $(ROOT_SERVERS_NET_ZSK)
ROOT_SERVERS_NET_KEY_FILES=$(ROOT_SERVERS_NET_KSK_FILES) $(ROOT_SERVERS_NET_ZSK_FILES)

NET_DNAME=net
NET_KSK=$(KEYS_DIR)/K$(NET_DNAME).ksk
NET_ZSK=$(KEYS_DIR)/K$(NET_DNAME).zsk
NET_ZSK2=$(KEYS_DIR)/K$(NET_DNAME).zsk2
NET_DS=$(NET_KSK).ds
NET_KSK_FILES=$(NET_KSK).key $(NET_KSK).private $(NET_DS)
NET_ZSK_FILES=$(NET_ZSK).key $(NET_ZSK).private
NET_ZSK2_FILES=$(NET_ZSK2).key $(NET_ZSK2).private
NET_KEYS=$(NET_KSK) $(NET_ZSK) $(NET_ZSK2)
NET_KEY_FILES=$(NET_KSK_FILES) $(NET_ZSK_FILES) $(NET_ZSK2_FILES)

ROOT_SERVERS_DNAME=root-servers
ROOT_SERVERS_KSK=$(KEYS_DIR)/K$(ROOT_SERVERS_DNAME).ksk
ROOT_SERVERS_ZSK=$(KEYS_DIR)/K$(ROOT_SERVERS_DNAME).zsk
ROOT_SERVERS_DS=$(ROOT_SERVERS_KSK).ds
ROOT_SERVERS_KSK_FILES=$(ROOT_SERVERS_KSK).key $(ROOT_SERVERS_KSK).private $(ROOT_SERVERS_DS)
ROOT_SERVERS_ZSK_FILES=$(ROOT_SERVERS_ZSK).key $(ROOT_SERVERS_ZSK).private
ROOT_SERVERS_KEYS=$(ROOT_SERVERS_KSK) $(ROOT_SERVERS_ZSK)
ROOT_SERVERS_KEY_FILES=$(ROOT_SERVERS_KSK_FILES) $(ROOT_SERVERS_ZSK_FILES)

LETTERS := a b c d e f g h i j k l m

ROOT_SERVER_KSK_FILES := $(foreach LETTER,$(LETTERS),$(KEYS_DIR)/K$(LETTER).ksk.key $(KEYS_DIR)/K$(LETTER).ksk.private $(KEYS_DIR)/K$(LETTER).ksk.ds)
ROOT_SERVER_ZSK_FILES := $(foreach LETTER,$(LETTERS),$(KEYS_DIR)/K$(LETTER).zsk.key $(KEYS_DIR)/K$(LETTER).zsk.private)

ROOT_SERVER_2_KSK_FILES := $(foreach LETTER,$(LETTERS),$(KEYS_DIR)/K$(LETTER).root-servers.ksk.key $(KEYS_DIR)/K$(LETTER).root-servers.ksk.private $(KEYS_DIR)/K$(LETTER).root-servers.ksk.ds)
ROOT_SERVER_2_ZSK_FILES := $(foreach LETTER,$(LETTERS),$(KEYS_DIR)/K$(LETTER).root-servers.zsk.key $(KEYS_DIR)/K$(LETTER).root-servers.zsk.private)


DOWNLOADS=$(ROOT_DOWNLOAD) $(ROOT_SERVERS_NET_DOWNLOAD) downloads/named.cache
UNSIGNED =$(ROOT_UNSIGNED) $(ROOT_SERVERS_NET_UNSIGNED)
KEYS=$(ROOT_KEYS) $(ROOT_SERVERS_NET_KEYS)

5_1_DIR=.
5_1_MKDIR=
5_1_PREFIX=5.1-
5_1_ROOT=$(5_1_DIR)/$(5_1_PREFIX)root
5_1_NET_UNSIGNED=unsigned/$(5_1_PREFIX)net
5_1_NET=$(5_1_DIR)/$(5_1_PREFIX)net
5_1_ROOT_SERVERS_NET=$(5_1_DIR)/$(5_1_PREFIX)root-servers.net
5_1=$(5_1_ROOT) $(5_1_NET) $(5_1_ROOT_SERVERS_NET)
5_1_FILES=$(5_1) $(5_1_NET_UNSIGNED)

#5_2_DIR=5.2
#5_2_MKDIR=$(5_2_DIR)/.mkdir
5_2_DIR=.
5_2_MKDIR=
5_2_PREFIX=5.2-
5_2_ROOT_UNSIGNED=unsigned/$(5_2_PREFIX)root
5_2_ROOT=$(5_2_DIR)/$(5_2_PREFIX)root
5_2_NET_UNSIGNED=unsigned/$(5_2_PREFIX)net
5_2_NET=$(5_2_DIR)/$(5_2_PREFIX)net
5_2_ROOT_SERVERS_NET_UNSIGNED=unsigned/$(5_2_PREFIX)root-servers.net
5_2_ROOT_SERVERS_NET=$(5_2_DIR)/$(5_2_PREFIX)root-servers.net
5_2=$(5_2_ROOT) $(5_2_NET) $(5_2_ROOT_SERVERS_NET)
5_2_FILES=$(5_2) $(5_2_ROOT_UNSIGNED) $(5_2_NET_UNSIGNED) $(5_2_ROOT_SERVERS_NET_UNSIGNED)

#5_3_DIR=5.3
#5_3_MKDIR=$(5_3_DIR)/.mkdir
5_3_DIR=.
5_3_MKDIR=
5_3_PREFIX=5.3-
5_3_ROOT_UNSIGNED=unsigned/$(5_3_PREFIX)root
5_3_ROOT=$(5_3_DIR)/$(5_3_PREFIX)root
5_3=$(5_3_ROOT)
5_3_FILES=$(5_3) $(5_3_ROOT_UNSIGNED)

#5_3_1_DIR=5.3
#5_3_1_MKDIR=$(5_3_1_DIR)/.mkdir
5_3_1_DIR=.
5_3_1_MKDIR=
5_3_1_PREFIX=5.3.1-
5_3_1_ROOT_UNSIGNED=unsigned/$(5_3_1_PREFIX)root
5_3_1_ROOT=$(5_3_1_DIR)/$(5_3_1_PREFIX)root
5_3_1=$(5_3_1_ROOT)
5_3_1_FILES=$(5_3_1) $(5_3_1_ROOT_UNSIGNED)

#5_4_DIR=5.4
#5_4_MKDIR=$(5_4_DIR)/.mkdir
5_4_DIR=.
5_4_MKDIR=
5_4_PREFIX=5.4-
5_4_ROOT_UNSIGNED=unsigned/$(5_4_PREFIX)root
5_4_ROOT=$(5_4_DIR)/$(5_4_PREFIX)root
5_4_ROOT_SERVERS_UNSIGNED=unsigned/$(5_4_PREFIX)root-servers
5_4_ROOT_SERVERS=$(5_4_DIR)/$(5_4_PREFIX)root-servers
5_4=$(5_4_ROOT) $(5_4_ROOT_SERVERS)
5_4_FILES=$(5_4) $(5_4_ROOT_UNSIGNED) $(5_4_ROOT_SERVERS_UNSIGNED)

#5_5_DIR=5.5
#5_5_MKDIR=$(5_5_DIR)/.mkdir
5_5_DIR=.
5_5_MKDIR=
5_5_PREFIX=5.5-
5_5_ROOT_SERVERS:=$(foreach LETTER,$(LETTERS),$(5_5_DIR)/$(5_5_PREFIX)$(LETTER))
5_5_ROOT_UNSIGNED=unsigned/$(5_5_PREFIX)root
5_5_ROOT=$(5_5_DIR)/$(5_5_PREFIX)root
5_5=$(5_5_ROOT) $(5_5_ROOT_SERVERS)
5_5_FILES=$(5_5) $(5_5_ROOT_UNSIGNED)

#5_5_1_DIR=5.5.1
#5_5_1_MKDIR=$(5_5_1_DIR)/.mkdir
5_5_1_DIR=.
5_5_1_MKDIR=
5_5_1_PREFIX=5.5.1-
5_5_1_ROOT_SERVERS:=$(foreach LETTER,$(LETTERS),$(5_5_1_DIR)/$(5_5_1_PREFIX)$(LETTER).root-servers)
5_5_1_ROOT_UNSIGNED=unsigned/$(5_5_1_PREFIX)root
5_5_1_ROOT=$(5_5_1_DIR)/$(5_5_1_PREFIX)root
5_5_1=$(5_5_1_ROOT) $(5_5_1_ROOT_SERVERS)
5_5_1_FILES=$(5_5_1) $(5_5_1_ROOT_UNSIGNED)

#5_6_DIR=5.6
#5_6_MKDIR=$(5_6_DIR)/.mkdir
5_6_DIR=.
5_6_MKDIR=
5_6_PREFIX=5.6-
5_6_ROOT_UNSIGNED=unsigned/$(5_6_PREFIX)root
5_6_ROOT=$(5_6_DIR)/$(5_6_PREFIX)root
5_6=$(5_6_ROOT)
5_6_FILES=$(5_6) $(5_6_ROOT_UNSIGNED)

#5_6_1_DIR=5.6.1
#5_6_1_MKDIR=$(5_6_1_DIR)/.mkdir
5_6_1_DIR=.
5_6_1_MKDIR=
5_6_1_PREFIX=5.6.1-
5_6_1_ROOT_UNSIGNED=unsigned/$(5_6_1_PREFIX)root
5_6_1_ROOT=$(5_6_1_DIR)/$(5_6_1_PREFIX)root
5_6_1=$(5_6_1_ROOT)
5_6_1_FILES=$(5_6_1) $(5_6_1_ROOT_UNSIGNED)

#5_9_DIR=5.9
#5_9_MKDIR=$(5_9_DIR)/.mkdir
5_9_DIR=.
5_9_MKDIR=
5_9_PREFIX=5.9-
5_9_NET_UNSIGNED=unsigned/$(5_9_PREFIX)net
5_9_NET=$(5_9_DIR)/$(5_9_PREFIX)net
5_9=$(5_9_NET)
5_9_FILES=$(5_9) $(5_9_NET_UNSIGNED)

all: 5.1 5.2 5.3 5.3.1 5.4 5.5 5.5.1 5.6 5.6.1 5.9
5.1: $(5_1)
5.2: $(5_2)
5.3: $(5_3)
5.3.1: $(5_3_1)
5.4: $(5_4)
5.5: $(5_5)
5.5.1: $(5_5_1)
5.6: $(5_6)
5.6.1: $(5_6_1)
5.9: $(5_9)

.PHONY: all 5.1 5.2 5.3 5.4 5.5 5.5.1 5.6 5.6.1

$(DOWNLOADS):
	@mkdir downloads 2>/dev/null || true
	wget -O $@ https://www.internic.net/domain/$(patsubst downloads/%,%,$@)

$(UNSIGNED):
	@mkdir unsigned 2>/dev/null || true
	ldns-read-zone -s $(patsubst unsigned/%,downloads/%.zone,$@) \
	| egrep -v '^[0-9a-ZA-Z.-]+[[:space:]]+[0-9]+[[:space:]]IN[[:space:]]+DNSKEY[[:space:]]' \
	> $@

$(5_2_MKDIR) $(5_3_MKDIR) $(5_4_MKDIR) $(5_5_MKDIR) $(5_5_1_MKDIR) $(5_6_MKDIR) $(5_6_1_MKDIR) $(KEYS_MKDIR):
	@mkdir $(patsubst %/.mkdir,%,$@) 2>/dev/null || true
	touch $@

$(5_1_ROOT): $(5_2_ROOT)
	cp -p $< $@ 

$(5_1_NET_UNSIGNED): $(5_2_NET_UNSIGNED)
	egrep -iv '^root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+DS[[:space:]]' $< > $@

$(5_1_ROOT_SERVERS_NET): $(ROOT_SERVERS_NET_UNSIGNED)
	cp -p $< $@ 

$(5_1_NET): $(5_1_NET_UNSIGNED) $(NET_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_1_NET_UNSIGNED) $(NET_KEYS)

$(5_2_ROOT_UNSIGNED): $(ROOT_UNSIGNED) $(NET_DS)
	egrep -vi '^net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+[DN]S[[:space:]]' $(ROOT_UNSIGNED) > $@
	awk '{printf("%s\t$(ROOT_DEL_DS_TTL)\tIN\tDS\t%s %s %s %s\n",$$1,$$(NF-3),$$(NF-2),$$(NF-1),$$(NF))}' $(NET_DS) >> $@
	printf "net.\t$(ROOT_DEL_NS_TTL)\tIN\tNS\t$(NET_NS_DNAME)\n" >> $@
	printf "$(NET_NS_DNAME)\t$(ROOT_DEL_NS_TTL)\tIN\tA\t$(NET_NS_IPv4)\n" >> $@
	printf "$(NET_NS_DNAME)\t$(ROOT_DEL_NS_TTL)\tIN\tAAAA\t$(NET_NS_IPv6)\n" >> $@

$(5_2_NET_UNSIGNED): $(ROOT_UNSIGNED) $(ROOT_SERVERS_NET_DS)
	printf "net.\t$(NET_SOA_TTL)\tIN\tSOA\t$(NET_NS_DNAME) nstld.verisign-grs.com. %d 1800 900 604800 86400\n" `date +%s` > $@
	printf "net.\t$(NET_NS_TTL)\tIN\tNS\t$(NET_NS_DNAME)\n" >> $@
	egrep '^\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]]' $(ROOT_UNSIGNED) \
	| awk '{printf("root-servers.net.\t$(NET_DEL_NS_TTL)\tIN\tNS\t%s\n", $$5)}' >> $@
	awk '{printf("%s\t$(NET_DEL_DS_TTL)\tIN\tDS\t%s %s %s %s\n",$$1,$$(NF-3),$$(NF-2),$$(NF-1),$$(NF))}' $(ROOT_SERVERS_NET_DS) >> $@
	printf "$(NET_NS_DNAME)\t$(NET_NS_TTL)\tIN\tA\t$(NET_NS_IPv4)\n" >> $@
	printf "$(NET_NS_DNAME)\t$(NET_NS_TTL)\tIN\tAAAA\t$(NET_NS_IPv6)\n" >> $@
	egrep -i '^[a-z]+\.root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+(A|AAAA)[[:space:]]'  $(ROOT_UNSIGNED) \
	| awk '{printf("%s\t$(NET_NS_TTL)\tIN\t%s\t%s\n", $$1, $$4, $$5)}' >> $@
	dig @a.gtld-servers.net. example.net NS +norec +dnssec \
	| egrep -v '(^;)|(^$$)|[[:space:]]RRSIG[[:space:]]' >> $@
	dig @a.gtld-servers.net. iana-servers.net NS +norec +dnssec \
	| egrep -v '(^;)|(^$$)|[[:space:]]RRSIG[[:space:]]' >> $@

$(5_2_ROOT): $(5_2_MKDIR) $(5_2_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_2_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_2_NET): $(5_2_MKDIR) $(5_2_NET_UNSIGNED) $(NET_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_2_NET_UNSIGNED) $(NET_KEYS)

$(5_2_ROOT_SERVERS_NET): $(5_2_MKDIR) $(ROOT_SERVERS_NET_UNSIGNED) $(ROOT_SERVERS_NET_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o $(ROOT_SERVERS_NET_DNAME) -f $@ $(ROOT_SERVERS_NET_UNSIGNED) $(ROOT_SERVERS_NET_KEYS)

$(5_3_ROOT_UNSIGNED): $(ROOT_UNSIGNED)
	sed 's/\b\([a-z]\)\.root-servers\.net.\B/\1.root-servers./g' $(ROOT_UNSIGNED) > $@

$(5_3_ROOT): $(5_3_MKDIR) $(5_3_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_3_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_3_1_ROOT_UNSIGNED): $(ROOT_UNSIGNED)
	sed 's/\b\([a-z]\)\.root-servers\.net.\B/\1./g' $(ROOT_UNSIGNED) > $@

$(5_3_1_ROOT): $(5_3_1_MKDIR) $(5_3_1_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_3_1_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_4_ROOT_SERVERS_UNSIGNED): $(ROOT_SERVERS_NET_UNSIGNED)
	sed 's/\broot-servers\.net.\B/root-servers./g' $(ROOT_SERVERS_NET_UNSIGNED) > $@

$(5_4_ROOT_UNSIGNED): $(5_3_ROOT_UNSIGNED) $(5_4_ROOT_SERVERS_UNSIGNED) $(ROOT_SERVERS_DS)
	egrep -i '^root-servers\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]]' $(5_4_ROOT_SERVERS_UNSIGNED) \
	| awk '{printf("%s\t$(ROOT_DEL_NS_TTL)\tIN\tNS\t%s\n",$$1,$$5)}' \
	| cat $(5_3_ROOT_UNSIGNED) - > $@
	awk '{printf("%s\t$(ROOT_DEL_DS_TTL)\tIN\tDS\t%s %s %s %s\n",$$1,$$(NF-3),$$(NF-2),$$(NF-1),$$(NF))}' $(ROOT_SERVERS_DS) >> $@

$(5_4_ROOT): $(5_4_MKDIR) $(5_4_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_4_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_4_ROOT_SERVERS): $(5_4_MKDIR) $(5_4_ROOT_SERVERS_UNSIGNED) $(ROOT_SERVERS_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o $(ROOT_SERVERS_DNAME) -f $@ $(5_4_ROOT_SERVERS_UNSIGNED) $(ROOT_SERVERS_KEYS)

$(5_5_ROOT_UNSIGNED): $(ROOT_UNSIGNED) $(ROOT_SERVER_KSK_FILES) $(ROOT_SERVER_ZSK_FILES)
	sed 's/\b\([a-z]\)\.root-servers\.net.\B/root.\1./g' $(ROOT_UNSIGNED) > $@
	for LETTER in $(LETTERS); do \
		printf "%s.\t$(ROOT_DEL_NS_TTL)\tIN\tNS\troot.%s.\n" $$LETTER $$LETTER >> $@; \
		awk '{printf("%s\t$(ROOT_DEL_DS_TTL)\tIN\tDS\t%s %s %s %s\n",$$1,$$(NF-3),$$(NF-2),$$(NF-1),$$(NF))}' $(KEYS_DIR)/K$${LETTER}.ksk.ds >> $@; done

$(5_5_ROOT): $(5_5_MKDIR) $(5_5_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_5_ROOT_UNSIGNED) $(ROOT_KEYS)

bla:
	echo $(5_5_ROOT_SERVERS)

$(5_5_ROOT_SERVERS): $(5_5_MKDIR) $(ROOT_SERVER_KSK_FILES) $(ROOT_SERVER_ZSK_FILES) $(ROOT_SERVERS_NET_UNSIGNED)
	awk -vfqdn=$(patsubst $(5_5_PREFIX)%,%.,$@) '\
		/[A-Za-z.-]+[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+SOA[[:space:]]/{printf("%s\t%s\tIN\tSOA\troot.%s hostmaster.%s %s %s %s %s %s\n",fqdn,$$2,fqdn,fqdn,$$(NF-4),$$(NF-3),$$(NF-2),$$(NF-1),$$NF)}\
		/^$(patsubst $(5_5_PREFIX)%,%,$@)\.root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+(A|AAAA)[[:space:]]/{printf("root.%s\t%s\tIN\t%s\t%s\n",fqdn,$$2,$$(NF-1),$$NF)} \
		/^root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]]+$(patsubst $(5_5_PREFIX)%,%,$@)\.root-servers\.net\.$$/{printf("%s\t%s\tIN\tNS\troot.%s\n",fqdn,$$2,fqdn)} \
		' $(ROOT_SERVERS_NET_UNSIGNED) \
	| ldns-signzone  -i $(INCEPTION) -e $(EXPIRATION) -o $(patsubst $(5_5_PREFIX)%,%,$@) -f $@ - \
		$(KEYS_DIR)/K$(patsubst $(5_5_PREFIX)%,%,$@).ksk $(KEYS_DIR)/K$(patsubst $(5_5_PREFIX)%,%,$@).zsk

$(5_5_1_ROOT_UNSIGNED): $(ROOT_UNSIGNED) $(ROOT_SERVER_2_KSK_FILES) $(ROOT_SERVER_2_ZSK_FILES)
	sed 's/\b\([a-z]\)\.root-servers\.net.\B/ns.\1.root-servers./g' $(ROOT_UNSIGNED) > $@
	for LETTER in $(LETTERS); do \
		printf "%s.\t$(ROOT_DEL_NS_TTL)\tIN\tNS\tns.%s.\n" $${LETTER}.root-servers $${LETTER}.root-servers >> $@; \
		awk '{printf("%s\t$(ROOT_DEL_DS_TTL)\tIN\tDS\t%s %s %s %s\n",$$1,$$(NF-3),$$(NF-2),$$(NF-1),$$(NF))}' $(KEYS_DIR)/K$${LETTER}.root-servers.ksk.ds >> $@; done

$(5_5_1_ROOT): $(5_5_1_MKDIR) $(5_5_1_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_5_1_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_5_1_ROOT_SERVERS): $(5_5_1_MKDIR) $(ROOT_SERVER_2_KSK_FILES) $(ROOT_SERVER_2_ZSK_FILES) $(ROOT_SERVERS_NET_UNSIGNED)
	awk -vfqdn=$(patsubst $(5_5_1_PREFIX)%,%.,$@) '\
		/[A-Za-z.-]+[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+SOA[[:space:]]/{printf("%s\t%s\tIN\tSOA\tns.%s hostmaster.%s %s %s %s %s %s\n",fqdn,$$2,fqdn,fqdn,$$(NF-4),$$(NF-3),$$(NF-2),$$(NF-1),$$NF)}\
		/^$(patsubst $(5_5_1_PREFIX)%,%,$@)\.root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+(A|AAAA)[[:space:]]/{printf("ns.%s\t%s\tIN\t%s\t%s\n",fqdn,$$2,$$(NF-1),$$NF)} \
		/^root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]]+$(patsubst $(5_5_1_PREFIX)%,%,$@)\.root-servers\.net\.$$/{printf("%s\t%s\tIN\tNS\tns.%s\n",fqdn,$$2,fqdn)} \
		' $(ROOT_SERVERS_NET_UNSIGNED) \
	| ldns-signzone  -i $(INCEPTION) -e $(EXPIRATION) -o $(patsubst $(5_5_1_PREFIX)%,%,$@) -f $@ - \
		$(KEYS_DIR)/K$(patsubst $(5_5_1_PREFIX)%,%,$@).ksk $(KEYS_DIR)/K$(patsubst $(5_5_1_PREFIX)%,%,$@).zsk

$(5_6_ROOT_UNSIGNED): $(ROOT_UNSIGNED)
	egrep -iv '^\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]][b-z]+\.root-servers\.net\.\B'  $(ROOT_UNSIGNED) \
	| sed -e 's/\b[a-z]\.root-servers\.net.\B/root-servers./g' \
	> $@

$(5_6_ROOT): $(5_6_MKDIR) $(5_6_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_6_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_6_1_ROOT_UNSIGNED): $(ROOT_UNSIGNED)
	egrep -iv '^\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]+NS[[:space:]][b-z]+\.root-servers\.net\.\B'  $(ROOT_UNSIGNED) \
	| sed -e 's/\b[a-z]\.root-servers\.net.\B/all-root-servers./g' \
	> $@

$(5_6_1_ROOT): $(5_6_1_MKDIR) $(5_6_1_ROOT_UNSIGNED) $(ROOT_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_6_1_ROOT_UNSIGNED) $(ROOT_KEYS)

$(5_9_NET_UNSIGNED): $(5_2_NET_UNSIGNED)
	egrep -iv '^([a-z]\.)?root-servers\.net\.[[:space:]]+[0-9]+[[:space:]]+IN[[:space:]]' $< > $@

$(5_9_NET): $(5_9_NET_UNSIGNED) $(NET_KEY_FILES)
	ldns-signzone -i $(INCEPTION) -e $(EXPIRATION) -o . -f $@ $(5_9_NET_UNSIGNED) $(NET_KEYS)


$(ROOT_KSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(KSK_ALGO) -k -b $(KSK_SIZE) -r $(DEV_RANDOM) -sf . \
	&& (cd ..; rm -f $(ROOT_KSK_FILES)) \
	&& mv .ds K.ksk.ds \
	&& mv .key K.ksk.key \
	&& mv .private K.ksk.private

$(ROOT_ZSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(ZSK_ALGO) -b $(ZSK_SIZE) -r $(DEV_RANDOM) -sf . \
	&& (cd ..; rm -f $(ROOT_ZSK_FILES)) \
	&& mv .key K.zsk.key \
	&& mv .private K.zsk.private

$(NET_KSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(KSK_ALGO) -k -b $(KSK_SIZE) -r $(DEV_RANDOM) -sf $(NET_DNAME) \
	&& (cd ..; rm -f $(NET_KSK_FILES)) \
	&& mv .ds K$(NET_DNAME).ksk.ds \
	&& mv .key K$(NET_DNAME).ksk.key \
	&& mv .private K$(NET_DNAME).ksk.private

$(NET_ZSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(NET_ZSK_ALGO) -b $(NET_ZSK_SIZE) -r $(DEV_RANDOM) -sf $(NET_DNAME) \
	&& (cd ..; rm -f $(NET_ZSK_FILES)) \
	&& mv .key K$(NET_DNAME).zsk.key \
	&& mv .private K$(NET_DNAME).zsk.private

$(NET_ZSK2_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(NET_ZSK_ALGO) -b $(NET_ZSK_SIZE) -r $(DEV_RANDOM) -sf $(NET_DNAME) \
	&& (cd ..; rm -f $(NET_ZSK2_FILES)) \
	&& mv .key K$(NET_DNAME).zsk2.key \
	&& mv .private K$(NET_DNAME).zsk2.private

$(ROOT_SERVERS_NET_KSK_FILES) $(ROOT_SERVERS_KSK_FILES) $(ROOT_SERVER_KSK_FILES) $(ROOT_SERVER_2_KSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(KSK_ALGO) -k -b $(KSK_SIZE) -r $(DEV_RANDOM) -sf \
	 $(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@)))) \
	&& (cd ..; rm -fr            $(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@))).ds \
	                             $(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@))).key \
	                             $(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@))).private ) \
	&& mv .ds \
	K$(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@)))).ksk.ds \
	&& mv .key \
	K$(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@)))).ksk.key \
	&& mv .private \
	K$(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.ksk.private,%,$(patsubst %.ksk.key,%,$(patsubst %.ksk.ds,%,$@)))).ksk.private

$(ROOT_SERVERS_NET_ZSK_FILES) $(ROOT_SERVERS_ZSK_FILES) $(ROOT_SERVER_ZSK_FILES) $(ROOT_SERVER_2_ZSK_FILES): $(KEYS_MKDIR)
	cd $(KEYS_DIR) \
	&& ldns-keygen -a $(ZSK_ALGO) -b $(ZSK_SIZE) -r $(DEV_RANDOM) -sf \
	 $(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.zsk.private,%,$(patsubst %.zsk.key,%,$@))) \
	&& (cd ..; rm -fr            $(patsubst %.zsk.private,%,$(patsubst %.zsk.key,%,$@)).key \
	                             $(patsubst %.zsk.private,%,$(patsubst %.zsk.key,%,$@)).private ) \
	&& mv .key \
	K$(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.zsk.private,%,$(patsubst %.zsk.key,%,$@))).zsk.key \
	&& mv .private \
	K$(patsubst $(KEYS_DIR)/K%,%,$(patsubst %.zsk.private,%,$(patsubst %.zsk.key,%,$@))).zsk.private

clean-5.9:
	rm -f $(5_9_FILES)
	[ "$(5_9_DIR)" = "." ] || rmdir $(5_9_DIR) || true

clean-5.6.1:
	rm -f $(5_6_1_FILES)
	[ "$(5_6_1_DIR)" = "." ] || rmdir $(5_6_1_DIR) || true

clean-5.6:
	rm -f $(5_6_FILES)
	[ "$(5_6_DIR)" = "." ] || rmdir $(5_6_DIR) || true

clean-5.5.1:
	rm -f $(5_5_1_FILES)
	[ "$(5_5_1_DIR)" = "." ] || rmdir $(5_5_1_DIR) || true

clean-5.5:
	rm -f $(5_5_FILES)
	[ "$(5_5_DIR)" = "." ] || rmdir $(5_5_DIR) || true

clean-5.4:
	rm -f $(5_4_FILES)
	[ "$(5_4_DIR)" = "." ] || rmdir $(5_4_DIR) || true

clean-5.3.1:
	rm -f $(5_3_1_FILES)
	[ "$(5_3_1_DIR)" = "." ] || rmdir $(5_3_1_DIR) || true

clean-5.3:
	rm -f $(5_3_FILES)
	[ "$(5_3_DIR)" = "." ] || rmdir $(5_3_DIR) || true

clean-5.2:
	rm -f $(5_2_FILES)
	[ "$(5_2_DIR)" = "." ] || rmdir $(5_2_DIR) || true

clean-5.1:
	rm -f $(5_1_FILES)
	[ "$(5_1_DIR)" = "." ] || rmdir $(5_1_DIR) || true

clean-scenarios: clean-5.1 clean-5.2 clean-5.3 clean-5.3.1 clean-5.4 clean-5.5 clean-5.5.1 clean-5.6 clean-5.6.1 clear-5.9

clean-keys:
	rm -fr keys

clean-unsigned:
	rm -fr unsigned

clean-downloads:
	rm -fr downloads

clean: clean-downloads clean-unsigned clean-keys clean-scenarios

$(ROOT_UNSIGNED): $(ROOT_DOWNLOAD)
$(ROOT_SERVERS_NET_UNSIGNED): $(ROOT_SERVERS_NET_DOWNLOAD)

