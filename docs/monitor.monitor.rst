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



