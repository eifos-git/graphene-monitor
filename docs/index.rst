.. Monitor documentation master file, created by
   sphinx-quickstart on Wed Feb  6 15:50:21 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Monitor's documentation!
===================================

Monitor is an easy to use framework you can use to monitor anything on your computer and to receive a notification
whenever some kind of condition is met.

About this Library
------------------

Monitor is divided into three subpackages:

* source
* trigger
* action

Each subpackages, sometimes referred to as *monitor domain* takes on it's own small task.

There are two classes that stitch them together. First and foremost there is the monitor class.
Monitor itself is the framework that is used to do the monitoring and parse data from one module to the other.
Secondly there is source trigger pair. For a closer documentation on why it is necessary to combine two of our modules
have a look at it's documentation.

Contents
========

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   tutorials
   monitor

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
