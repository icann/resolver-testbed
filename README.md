# Resolver Testbed

This repo describes a testbed to test various DNS resolvers.
The purpose of the testbed is to allow researchers to set up many resolvers and run tests on each.
For example, a test might see what the resolver emits when it is priming, or when
it is responding to a particular query while using DNSSEC validation.

The project is sponsored by ICANN.

For information on the project, please contact [Paul Hoffman](mailto:paul.hoffman@icann.org).

## Installation and Requirements

The testbed has been tested on Ubuntu workstation (and derivatives like Xubuntu),
as well as MacOS.

Install the testbed by cloning from GitHub at <https://github.com/icann/resolver-testbed>.

You need to have Python 3 installed. Other than the standard library, you also need
a recent version of the [Fabric library](http://www.fabfile.org/). `pip install fabric` will work.

VMs are kept in [VirtualBox](https://www.virtualbox.org/).
On Ubuntu hosts, use `sudo apt install -y virtualbox` instead of installing from the software store.

The VMs are all accessed using the "root" user only.

@@ MORE REQUIREMENTS WILL GO HERE @@

## Other Documents

Please see [the technical plan](technical-plan.md) for an overview of the technical parts of the testbed.

Please see [the setup and running guide](setup-and-running.md) for steps on how to create the testbed and run tests.

The project is still in its early phases. Please see the end of [rt.py](rt.py) for a list of areas known
to be incomplete.

## License

See the [LICENSE file](file:LICENSE).

