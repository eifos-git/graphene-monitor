from monitor import *
from monitor.trigger.utils import collapse_triggers
import time
import yaml
from monitor_variations.monitor import Monitor
WAITING_TIME = 2  # in seconds


class Config():
    """Load and save monitor Configuration"""

    data = []

    @staticmethod
    def load(monitor_config_files):
        if type(monitor_config_files) == str:
            monitor_config_files = [monitor_config_files]
        for file in monitor_config_files:
            with open(file, 'r') as stream:
                Config.data.append(yaml.load(stream))



Config.load(["example-config.yaml"])

if __name__ == '__main__':
    # TODO: Multiple monitors doesnt work

    monitors = []
    for monitor_config in Config.data:
        monitors.append(Monitor(monitor_config["monitor"]))

    print("Amount of monitors added: " + str(len(monitors)))

    while True:
        for monitor in monitors:
            monitor.do_monitoring()
        print("------- Monitor cycle finished. Going to sleep now zZz. ------")
        time.sleep(2)
