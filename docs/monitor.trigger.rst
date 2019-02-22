monitor.trigger package
=======================

Trigger is the part of monitor that needs to do the most of the work. It receives data from source.
The user is supposed to make sure that the data the trigger receives is actually parsed in such a way that trigger is
able to handle it. Then it needs to calculate whether or not its condition according to the config file is met.
If the condition is met trigger is also responsible for the message that is parsed to action.

The good news is that most of the problems can be transformed in such a way that we only need to compare numbers or the
state of the data. Therefore the two modules we provide are already sufficient for most of the use cases.

Submodules
----------

.. toctree::

   monitor.trigger.data_changed
   monitor.trigger.utils
   monitor.trigger.valuecompare

Module contents
---------------

.. automodule:: monitor.trigger
    :members:
    :undoc-members:
    :show-inheritance:
