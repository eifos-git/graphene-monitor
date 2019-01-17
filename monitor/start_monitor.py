from monitor import *
from monitor.monitor.trigger.utils import collapse_triggers
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
    triggers = []
    for trigger in monitor.triggers:
        trigger_status = trigger.check_condition(data)
        if trigger_status:
            triggers.append(trigger_status)

    triggers = collapse_triggers(triggers) # remove all false conditions

    #TODO:
    """Triggers should only fire once per group, with the highest defined level and all the
    trigger information in one action
    
    The way messages work is bad. We should use a message function in trigger to define how the message is printed for each trigger
    not the other way around. messages should be part of trigger not action.
    
    Add implementation for one trigger. 
    
    Execute the actions for every trigger."""
    if triggers is not []:
        for action in monitor.actions:
            #Hier sollte Monitor comparison stattfinden
            #action.shoot(triggers_fired)

            print("The following triggers are supposed to fire now!")
            print(triggers)
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
