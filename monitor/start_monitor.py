from monitor import *
import time
import yaml
from monitor_variations.monitor import Monitor
WAITING_TIME = 2 # in seconds

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


def do_monitoring(monitor):
    data = monitor.source.retrieve_data()
    if data is None:
        raise Exception("Data is none, therefore it cant be used as input for trigger")
    print("Data received: " + str(data))
    triggers_fired = []
    for trigger in monitor.triggers:
        trigger_status = trigger.check_condition(data)
        if trigger_status:
            triggers_fired.append(trigger_status)

    if triggers_fired is not []:
        for action in monitor.actions:
            #Hier sollte Monitor comparison stattfinden
            #action.shoot(triggers_fired)

            print("The following triggers are supposed to fire now!")
            print(triggers_fired)
        triggers_fired = []


Config.load("monitor-config.yaml")

if __name__ == '__main__':
    #TODO: Files as input instead

    monitors = []
    for monitor_config in Config.data:
        monitors.append(Monitor(monitor_config["monitor"]))

    print("Amount of monitors added: " + str(len(monitors)))

    while True:
        for monitor in monitors:
            do_monitoring(monitor)
        time.sleep(2)
