.. Monitor documentation master file, created by
   sphinx-quickstart on Wed Feb  6 15:50:21 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Monitor's documentation!
===================================

Monitor is an easy to use framework to monitor any kind of information and to receive a notification
whenever a condition is met.

About this Library
------------------

Monitor is divided into three subpackages:

* source (get data)
* trigger (calculate condition)
* action (send message)

Each subpackages, sometimes referred to as *monitor domain*, takes on it's own individual task.

There are two classes that stitch them together. First and foremost there is the monitor class.
Monitor itself is the framework that is used to do the monitoring and parse data from one module to the other.
Secondly there is source trigger pair. For a closer documentation on why it is necessary to combine two of our modules
have a look at it's documentation.

Getting started
---------------

To get started we highly recommend you to read through Installation and Quickstart. Afterwards you should have
a good understanding on how to use graphene-monitor.

If you want to learn how to modify this tool to your own problem, have a look at the tutorial section.



Contents
========

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   tutorials

API
===

.. toctree::
   :maxdepth: 6

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
