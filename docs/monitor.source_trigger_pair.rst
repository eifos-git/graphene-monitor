Source Trigger Pair
-------------------

Stpairs are used to bind each trigger to its corresponding sources.
They are necessary because the user may want to create a trigger that is evaluated only for one source. Additionally
we don't want to spam the user so whenever one stpair fires, it will not fire again for a specified amount of seconds
(downtime in trigger config or general config).


.. autoclass:: monitor.monitor.SourceTriggerPair
    :members: