Tutorials
=========

Now that you know the basics of this Module you can start working on your own problems.
As I previously mentioned there are three kinds of classes you might want to add.

Add Source
----------

Firstly there is source. In order to use a new source, all we need is a python script that retrieves the data.
As soon as you have implemented a method that automatically reads the information you are set.

* Create new_source.py as a submodule inside of source.
* Add a class NewSource that inherits AbstractSource.
* Add an implementation for the abstract retrieve data function that gets called once every monitor cycle.
* Change the source.class attribute in config to monitor.source.new_source.NewSource

Add Trigger
-----------

Trigger or rather the methods it needs to implement are a little more complicated.
Make sure that it is really necessary to add a new trigger, as most
problems can be solved by the small amount of triggers we already implemented.

* Create new_trigger.py as a submodule inside of trigger.
* Add a new class NewTrigger that inherits AbstractTrigger.
* Add an implementation for check_condition(data). It takes data from source needs to call super().check_condition(),
    has to change



Add Action
----------

Specify how you want to receive a notification in case on of your triggers fires. Action gets called with a message
as a string to be sent.

TODO: HowTo
