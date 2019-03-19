Quickstart
==========

After you have installed the application you can start your first monitoring program. To run the program simply type:

::

    $ python3 cli.py --options

If you get a message that the source is unreachable, the installation and running was successful and you have just
witnessed the first feature. It warns you whenever the source you set for the application is unreachable. But more on
this later.

There are a bunch of options you can set that will change the behaviour of the whole program.
The following flags are supported:

* config: Filename of config(default: config.yaml)
* monitor_interval: Seconds between two monitor cycles in seconds (default 2)
* multithreading: Enable multithreading. Only available for multiple monitors. (default False)
* trigger_downtime: Minimum time between two firing of the same trigger. (default 0)
* silent: Doesnt send a message to the console every monitor iteration. (default False)



Configuration
-------------


Let's look at the following example to understand how to configure graphene-monitor.
The basic structure of every config file is:

::

    <monitor_name>:
        sources:
            - <source1>:
                class:

        triggers:
            - <trigger1>:
                class:

        actions:
            - <action1>:
                class:

    (<second_monitor_name>:)

Class is mandatory and is used by the application to import the class you defined.
Everything in between <> can be chosen freely and we highly recommend that you give meaningful names,
as it will increase the readability of the trigger messages.

Level is used to bind triggers to actions. Messages are triggered for every action with a level equal or smaller than
trigger level.
If you ever use one of the predefined monitor domains have a look at their documentation, as they all have
their own different set of config values.

First Monitor
-------------

Now we want to take a look at a working example. Open the file ./examples/quickstart.yaml.
The purpose of this monitor is easy to understand. At first we make an http request to
the url we specified. Then we check whether the http response code is higher or equal to 500. This is, by convention,
used to indicate a server error. Finally we use stdout to print a message. Let's run it:

::

    $ python3 cli.py --config="./examples/quickstart.yaml" --monitor_interval=10

We don't want to dos the server so we tell the monitor to only make a request every 10 seconds.

If you are not seeing anything then Congratulations! We are now monitoring a website and we will receive a notification
as soon as there is a server error. We now know that the site is working as intended.

To verify this, changes the value for "greater_or_equal" to 200. This means that a trigger will fire, every time the
status code is higher than 200.
The problem with that is, that a status code higher than 200 can mean basically anything. Let's change that:

::

        triggers:
            - ServerErrorTrigger:
                class: valuecompare.ValueCompare
                greater_or_equal: 500
                level: 0

            - SuccessResponseCode:
                class: valuecompare.ValueCompare
                greater_or_equal: 200
                less: 300
                downtime: 15
                level: 0

As the trigger name suggests we now created a trigger that notifies us every time the site returns a http success code,
that means the response code is in between the interval [200, 300).

I also sneaked another parameter in. Downtime is used to prevent the application from spamming. Every time
SuccessResponseCode fires it has a downtime of eight seconds. That means it won't fire for eight seconds or in our case
exactly for one cycle.

For a complete list  on all the parameter that are available for every application look :ref:`here <config_keys>`

Unreachable Source
------------------

One case that is particularly interesting is that source is completely unreachable (Not even a status code).
This means that your source module was unable to retrieve any data and therefore every trigger you activated will not
work properly. In this case one messaged will be printed to every action in the first monitor iteration in which source
is not available and one message as soon as it comes back up.

Please keep in mind, that those messages are not considered triggers and therefore trigger downtime doesn't apply to
them.

Examples
--------

A bunch of working example configs are provided in the ./examples folder.

* event_outdated.yaml: Monitor Peerplays Events and get notified when the status of an event
    hasn't changed after a specified time after its' supposed start time.
* event_transition.yaml: Monitor all Peerplays Events and notifies you if none has changed for a
    specified time period
