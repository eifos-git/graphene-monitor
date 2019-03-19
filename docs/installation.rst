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

Test if the programm is running:

::

    $ python3 cli.py --config="./examples/test_config.yaml"
