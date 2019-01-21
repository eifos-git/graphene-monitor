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


def do_monitoring(monitor):
    data = monitor.source.retrieve_data()
    if data is not None:
        triggers = []
        for trigger in monitor.triggers:
            if trigger.check_condition(data):
                triggers.append(trigger)

        triggers = collapse_triggers(triggers)  # list of all the triggers with the correct conditon
        # as trigger[i].get_condition
        for trigger in triggers:
            if trigger.get_condition() is False:
                continue
            message = trigger.prepare_message()
            for action in monitor.actions:
                try:
                    trigger_level = trigger.get_config("level")
                except KeyError:
                    raise KeyError("A level needs to be provided for every trigger")
                if trigger_level >= action.level:
                    action.fire(message)
    else:
        # Data is None
        # TODO: Refactoring. Move this to Monitor class
        for action in monitor.actions:
            action.fire("Trigger: UnreachableSourceTrigger\n"
                        "The source {0} is unreachable.".format(monitor.source.config))



Config.load(["example-config.yaml"])

if __name__ == '__main__':
    # TODO: Multiple monitors doesnt work

    monitors = []
    for monitor_config in Config.data:
        monitors.append(Monitor(monitor_config["monitor"]))

    print("Amount of monitors added: " + str(len(monitors)))

    while True:
        for monitor in monitors:
            do_monitoring(monitor)
        time.sleep(2)
