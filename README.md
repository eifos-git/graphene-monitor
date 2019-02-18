AMonitor
========

AMonitor provides an easy to use framework to monitor any kind of data and getting messaging the user, depending on
the result.

Monitor divides this process into three different submodules, namely source, trigger and action.
They provide the interface for the actual methods and a bunch of examples to enable the user to easily 
add own methods of retrieving data, processing data or sending the data to the user.
Additionally there are two classes 'stitching' those modules together, firstly monitor and secondly source_trigger_pair.
For a closer documentation on them look at monitor.py


How to use a Monitor
====================

Although AMonitor already provides a bunch of classes to work with the main purpose of this module is not to give you an
application for your specific problem, but to provide a framework you can easily adjust to your problem. 
For a closer documentation on how to proceed have a look add quickstart.rst.



