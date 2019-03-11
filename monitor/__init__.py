import time
import yaml
import os
import threading
from .monitor import Monitor


class Config:
    """Load and save monitor Configuration"""

    data = []
    general_config = {}

    @staticmethod
    def _load(monitor_config_files):
        """
        Load the configuration file into Config.data

        :param monitor_config_files:
        """
        if isinstance(monitor_config_files, str):
            monitor_config_files = [monitor_config_files]
        for file in monitor_config_files:
            with open(file, 'r') as stream:
                Config.data.append(yaml.load(stream))

    @staticmethod
    def _get_general_config(key):
        """This should not fail. If it does, define a default value for the configuration
        as click option in cli."""
        return Config.general_config[key]

    @staticmethod
    def add_general_config(general_config):
        Config.general_config = general_config

    @staticmethod
    def load_monitor_config(monitor_config=None):
        """Loads the configuration file you specified in cli.py and saves it
        in data
        """
        if monitor_config:
            Config.data.append(monitor_config)
        else:
            Config._load(
                os.path.join(
                    os.getcwd(),
                    Config._get_general_config("config")
                ))

    @staticmethod
    def get_monitor_cycle_length():
        """
        :return: monitor cycle length as defined in general_config.yaml as "monitor_interval"
        """
        monitor_interval = Config._get_general_config("monitor_interval")
        if monitor_interval is None:
            return 2
        return int(monitor_interval)

    @staticmethod
    def get_bool_multithreading():
        multithreading = Config._get_general_config("multithreading")
        return False if multithreading is None else multithreading

    @staticmethod
    def get_trigger_downtime():
        return Config._get_general_config("trigger_downtime")


def setup_monitors():
    """Every Monitor gets initiated"""
    monitors = []
    for monitor_config in Config.data:
        # In case multiple monitors are added into one config File:
        for monitor in monitor_config.keys():
            monitors.append(Monitor(monitor_config[monitor], name=monitor, general_config=Config.general_config))
    return monitors


def get_monitor_keys(monitor_config):
    return monitor_config.keys()
    """Return the keys of all monitors in a config file as a list of str"""
    monitor_names = []
    for name, monitor in monitor_config.items():
        monitor_names.append(name)
    return monitor_names


def start_working(monitors):
    """Starts the monitor cycle in the given interval
    Enable multithreading by setting it true in general_config.yaml

    :param monitors: list of Monitor objects
    """

    while True:
        if Config.get_bool_multithreading():
            threads = []
            for monitor in monitors:
                threads.append(threading.Thread(target=monitor.do_monitoring))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
            threads.clear()
        else:
            for monitor in monitors:
                monitor.do_monitoring()
        time.sleep(Config.get_monitor_cycle_length())





