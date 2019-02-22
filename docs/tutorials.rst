Tutorials
=========

AMonitor is implemented as a framework. That means we want you to spend as little time as possible with the actual
module and the only struggle you should have to do with your specific problem.
Nevertheless there will be two major changes you have to make in order to work with this module.

Change Config
-------------

The most important thing you need to know to work with AMonitor is to understand how the config files work.
In our quickstart guide we already showed you how to work with the config files but there is a lot more to discuss,
simply because there are some features we haven't talked about yet.
Here is every parameter you can specify in config and it's purpose:

As a quick reminder, this is the config.yaml file structure:

::

    <monitor_name>
        sources:
            - <source1>:
                class: path.to.class
        triggers:
            - <trigger1>:
                class: path.to.class
            - <trigger2>:
                class: path.to.class
        actions:
            - <action1>:
                class: path.to.class

* Everything inside of angle brackets can and should be named to create meaningful messages.
* An arbitrary amount of triggers can be added in every monitor (same goes for source and action)
* class Indicates the path to the class of your monitor domain instance (see example below).
* trigger can have a source argument with the name of a source, in this case source1. It will only be evaluated for the source specified.
* trigger can also have a downtime argument that indicates the time in seconds it should not fire after it was activated the last time.
* trigger and action need a level to specify what action should be used for each trigger.

Finally there are also keywords specific to your problem, e.g url in http.Http. In python they are implemented as
dictionaries so they are actually pretty easy to implement in case you want an own keyword to work with. Look at
http.Http.get_url() for an example and implement your key accordingly.


Add Monitor Domain
------------------

Now that you know the basics of this Module you can start working on your own problems.
As I previously mentioned there are three kinds of classes you might want to add.

Add Source
..........

Firstly there is source. In order to use a new source, all we need is a python script that retrieves the data.
As soon as you have implemented a method that automatically reads the information you are set.

* Create new_source.py as a submodule inside of source.
* Add a class NewSource that inherits AbstractSource.
* Add an implementation for the abstract retrieve data function that gets called once every monitor cycle.
* Change the source.class attribute in config to monitor.source.new_source.NewSource

Add Trigger
...........

Trigger or rather the methods it needs to implement are a little more complicated.
Make sure that it is really necessary to add a new trigger, as most
problems can be solved by the small amount of triggers we already implemented.

* Create new_trigger.py as a submodule inside of trigger.
* Add a new class NewTrigger that inherits AbstractTrigger.
* Add an implementation for check_condition(data). Has to return boolean
* (optional, but recommended) Add an implementation for prepare_message(). Has to return string.
* Change the trigger.class attribute in config to monitor.trigger.new_trigger.NewTrigger


Add Action
..........

Specify how you want to receive a notification in case on of your triggers fires. Action gets called with a message
as a string to be sent.

* Create new_action.py as a submodule inside of action.
* Add a new class NewAction that inherits AbstractAction.
* Implement the method fire(message) that receive a message as string and is supposed to be sent to the user in any way.
* Change the action.class attribute in config to monitor.action.new_action.NewAction



