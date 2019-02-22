import copy
import logging


class SourceTriggerPair:
    """Combine one source with a copy of a trigger"""

    def __init__(self, source, trigger):
        self._wanted = SourceTriggerPair._check_if_wanted(source, trigger)
        if self._wanted:
            self.source = source  #: Reference to the source of this stpair
            self.trigger = copy.deepcopy(trigger)  #: Copy of the trigger of this stpair

    def check_if_wanted(self):
        """Test if the pair is wanted for this monitor or not.
        """
        return self._wanted

    def get_trigger(self):
        """Get trigger"""
        return self.trigger

    @staticmethod
    def _check_if_wanted(source, trigger):
        """Only used before initialization to check the triggers config. Look at check_source
        for a better description. Basically it checks the configuration of trigger whether
        this pair should exist or not"""
        source_name = source.get_source_name()
        is_wanted = trigger.check_source(source_name)
        return is_wanted

    def evaluate_trigger_condition(self):
        """Check and return whether the trigger's condition is met"""
        if not self._wanted:
            logging.warning("You tried to check the condition of a trigger with a source"
                            "that is not supposed to be checked")
            return False
        data = self.source.get_data()
        if data is None:
            return False
        cond = self.trigger.evaluate_trigger_condition(data)
        self.trigger.fired_recently()  # sets condition to false if trigger fired recently
        return self.trigger.get_condition()
