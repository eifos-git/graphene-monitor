************
Installation
************

Manual Installation
-------------------

::

    $ git clone git@github.com:blockchainbv/graphene-monitor.git
    $ cd graphene-monitor
    $ virtualenv venv
    $ source venv/bin/activate
    $ python3 setup.py install

To verify that everything is working as intended run:

::

    $ python3 cli.py --config="./examples/test_config.yaml"

A message that the website is reachable should appear every 10 seconds.

