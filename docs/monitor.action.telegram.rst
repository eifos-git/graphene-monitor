monitor.action.telegram module
==============================

The Telegram module provides the possibility sent notifications directly to your mobile device. One possible solution
to achieve this is by installing `telegram-send <https://pypi.org/project/telegram-send/>`_. Here is how to do it:

::

    $ sudo pip3 install telegram-send

Now to configure your personal telegram bot run the following command:

::

    $ telegram-send --configure

You will be asked to contact "BotFather", the bot that creates bots and to copy the token he sends you etc.
Simply follow the instructions. To test whether or not you have successfully installed it run:

::

    $ telegram-send "hello"

If you have received a message you are ready to use this module. Make sure that the environment you installed
telegram-send in is in the same environment monitor is running in.


.. automodule:: monitor.action.telegram
    :members:
    :undoc-members:
    :show-inheritance:
