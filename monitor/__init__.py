import time
import yaml
import os
import threading
import logging
from .trigger.utils import collapse_triggers
from .monitor import Monitor


class Config():
    """Load and save monitor Configuration"""

    data = []
    general_config = {}

    @staticmethod
    def _load(monitor_config_files, load_type):
        """
        Load the specified configuration into the Config class

        :param monitor_config_files:
        :param str load_type: data --> monitor config
                              general --> general config
        """
        if isinstance(monitor_config_files, str):
            monitor_config_files = [monitor_config_files]
        for file in monitor_config_files:
            with open(file, 'r') as stream:
                if load_type == "data":
                    Config.data.append(yaml.load(stream))
                elif load_type == "general":
                    Config.general_config.update(yaml.load(stream))

    @staticmethod
    def _get_general_config(config):
        try:
            return Config.general_config[config]
        except KeyError:
            return None

    @staticmethod
    def load_monitor_config(monitor_config_files):
        """Load a arbitrary amount of monitor config files.
        Put the config Files in monitor/monitor_config_files
        """
        Config._load(
            os.path.join(
                os.getcwd(),
                monitor_config_files
            ), "data")

    @staticmethod
    def load_general_config():
        """Load general information from monitor/general_config.yaml"""
        Config._load("general_config.yaml", "general")

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


def setup_monitors():
    """Every Monitor gets initiated"""
    monitors = []
    for monitor_config in Config.data:
        # In case multiple monitors are added into one config File:
        for monitor in monitor_config.keys():
            monitors.append(Monitor(monitor_config[monitor], name=monitor))
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
        print("------- Monitor cycle finished. Going to sleep now zZz. ------")
        print("\n")
        time.sleep(Config.get_monitor_cycle_length())


Config.load_general_config()
logging.basicConfig(filename="monitor.log", filemode="w", format="%(message)s")


