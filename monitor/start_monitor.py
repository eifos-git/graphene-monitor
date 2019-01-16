from monitor import *
import yaml
from monitor_variations.monitor import Monitor

class Config():
    """Load and save monitor Configuration"""

    data = []

    @staticmethod
    def load(monitor_config_files):
        if type(monitor_config_files == str):
            monitor_config_files = [monitor_config_files]
        for file in monitor_config_files:
            with open(file, 'r') as stream:
                Config.data.append(yaml.load(stream))


Config.load("monitor-config.yaml")

if __name__ == '__main__':
    #TODO: Files as input instead

    for monitor_config in Config.data:
        m1 = Monitor(monitor_config["monitor"])
        print(m1.get_config("triggers", "level", ["trigger2"]))

