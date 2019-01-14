import yaml
from monitor_class.monitor import Monitor

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



if __name__ is '__main__':
    #TODO: Files as input instead
    print("okay")
    Config.load("monitor-config.yaml")

    for monitor_config in Config.data:
        m1 = Monitor(monitor_config["monitor"])
        print(m1.get_config("triggers", "level", ["trigger2"]))









