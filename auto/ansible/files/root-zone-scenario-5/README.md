This is a setup for RSSAC028 root zone scenario 5, where each root server address is hosted in its own zone.

These zones are named 'a.' to 'm.', and the name of the server addresses is 'ns.<zone>.', e.g. 'ns.a. IN A 192.0.2.1'.

Each zone is signed with a single key, which has a DS record in the root zone.

The keys were manually created, but you can re-create and re-sign the zones with 'create_root_server_zones.sh'.

