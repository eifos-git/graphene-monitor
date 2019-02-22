monitor.monitor module
======================

Abstract Monitor
----------------

A Monitor instance inherits from Abstract Monitor and do_monitoring() is called every monitor cycle.
Each monitor consists of an arbitrary amount of sources, triggers and actions.


.. autoclass:: monitor.monitor.AbstractMonitor
    :members:

Monitor
-------
Monitor class that inherits Abstract Monitor. Currently only one type of monitor is used, therefore monitor and
Abstract monitor are basically the same.


.. autoclass:: monitor.monitor.Monitor
    :members:


Source Trigger Pair
-------------------

Another, less self explanatory attribute of a Monitor is stpair. Stpair is a list of stpairs,
each consisting of a reference to a source and a copy of a trigger.
They are necessary because the user may want to create a trigger that is evaluated only for one source. Additionally
we don't want to spam the user so whenever one stpair fires, it will not fire again for a specified amount of seconds
(downtime in trigger config or general config).


.. autoclass:: monitor.monitor.SourceTriggerPair
    :members:
