These are the files to set up the servers for scenario 2, where root-servers.net is signed.

Instead of root-servers.net, it uses some-servers.p53.

Compared to the original scenario, this contains the following changes:
- The root zone contains a signed delegation to the p53 zone, but apart from glue records, none of its contents.
- The p53 contains a signed delegation (with glue) to some-servers.p53.
- some-servers.p53 is now a separate signed zone
