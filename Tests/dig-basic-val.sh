#!/usr/bin/env bash
echo "dig @127.0.0.1 research.icann.org"
dig @127.0.0.1 research.icann.org
echo "dig @127.0.0.1 +dnssec research.icann.org"
dig @127.0.0.1 +dnssec research.icann.org
echo "dig @127.0.0.1 +dnssec dnssec-failed.org"
dig @127.0.0.1 +dnssec dnssec-failed.org

