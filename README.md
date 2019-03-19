# Graphene-Monitor

Graphene monitor provides an easy to use framework to monitor data, by sending you a message every time 
some kind of condition is met. 

## Installation

    $ git clone git@github.com:blockchainbv/graphene-monitor.git
    $ cd graphene-monitor
    $ virtualenv venv
    $ source venv/bin/activate
    $ python3 setup.py install

To verify that everything is working as intended run:

    $ python3 cli.py --config="./examples/test_config.yaml"

A message that a website is reachable should appear every 10 seconds.

## Getting Started

The Quickstart section in our documentation is a good place to 
learn about the application and get your first monitor running.
Afterwards you may want to have a look at the tutorial section to modify 
it to your own problems.

