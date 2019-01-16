def collapse_triggers(triggers):
    """This util is supposed to enable trigger grouping.
    When the triggers conditions are evaluated we cannot simply cross out all the false ones,
    because for grouped triggers all its members have to be True.
    """
    trig_copy = triggers.copy()
    for trigger in trig_copy:
        if not trigger["fire_condition_met"]:
            # Delete all the group members as well
            group = None
            triggers.remove(trigger)
            try:
                group_indicator = trigger["group"]
            except KeyError:
                # Not part of a group
                continue
            for group_trigger in trig_copy:
                try:
                    if group_trigger["group"] == group_indicator:
                        triggers.remove(group_trigger)
                except Exception:
                    continue

    return triggers




