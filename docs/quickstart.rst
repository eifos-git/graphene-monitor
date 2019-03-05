Quickstart
==========

After you have installed the application you can start your first monitoring program. To run the program simply type:

::

    $ python3 cli.py --options

There are a bunch of options you can set. For more information have a look at the cli.py documentation.
Alternatively, if you are using an IDE, you can also run the main function in cli.py.

If you get a message that the source is unreachable, the installation and running was successful and you have just
witnessed the first feature. It warns you whenever the source you set for the application is unreachable. But more on
this later.

Configuration
-------------

One of the options you can set in main is <config>. It is the backbone of the application and for most of the use cases
it is enough to change some parameters in config. We also provide some default config files for you to get a feeling how
AMonitor works.

At first have a look at quickstart.yaml in the main directory. This is the most basic config you can possibly set for
your application. The basic structure of every yaml file is:

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

The - in front of the paramter, e.g. source1, indicates that we can add multiple different sources. Class is mandatory
and is used by the application to import the class you defined. Everything in between <> is arbitrary and we highly
recommend that you give meaningful names, as it will increase the readability of the trigger messages.

Level is used to bind triggers to actions. Messages are triggered for every action with a level equal or smaller than
trigger level.

First Monitor
-------------

Have a look at quickstart.yaml. The purpose of this monitor is easy to understand. At first we make an http request to
the url we specified. Then we check whether the http response code is higher or equal to 500. This is, by convention,
used to indicate a server error. Finally we use stdout to print a message. Let's run it:

::

    $ python3 cli.py --config="quickstart.yaml" --monitor_interval=5

We don't want to dos the server so we set the interval in which the response cone is checked to five seconds
(Default 1s).

If you are not seeing anything then Congratulations! We are now monitoring a website and we will receive a notification
as soon as there is a server error. We now know that the site is working as intended.

Now this might seem like another boring example because you can't actually see that the monitor is doing anything.
Let's change that. Go to the quickstart.yaml file and add another trigger:

::

        triggers:
            - ServerErrorTrigger:
                class: monitor.trigger.valuecompare.ValueCompare
                greater_or_equal: 500
                level: 0

            - SuccessResponseCode:
                class: monitor.trigger.valuecompare.ValueCompare
                greater_or_equal: 200
                less: 300
                downtime: 8
                level: 0

As the trigger name suggests we now created a trigger that notifies us every time the site returns a http success code,
that means the response code is in between the interval [200, 300).

I also sneaked another parameter in. Downtime is used to prevent the application from spamming. Every time
SuccessResponseCode fires it has a downtime of eight seconds. That means it won't fire for eight seconds or in our case
exactly for one cycle.

Examples
--------

A bunch of working example configs are provided in the ./examples folder.

* event_outdated.yaml: Monitor all Peerplays events and get notified when the status
    of an event hasn't changed after a specified time
