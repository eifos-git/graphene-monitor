Monitor
========

Monitor is an easy to use framework for retrieving data, processing it and sending a message depending
on the result. 
There are three different submodules in this package, namely source, trigger and action. 
They provide the interface for the actual methods and a bunch of examples to enable the user to easily 
add own methods of said activities.
There are two Classes 'stitching' thoses modules together. For a closer documentation on them look at monitor.py



Add and use a new Source from scratch:
======================================

    1. Create a new source that inherits from monitor.source.AbstractSource\
       and implements all necessary methods in monitor/source/<new_source>.    
    2. Change the class parameter (or add a new source) to the path to your new source File


Add and use new Triggers/Actions from scratch:
==============================================

Use the steps described for source but interchange every source with trigger/action.


sphinx-apidoc -d 6 -e -f -o docs monitor
