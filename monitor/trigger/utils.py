def collapse_triggers(triggers):
    """This util is supposed to enable trigger grouping.
    When the triggers conditions are evaluated we cannot simply cross out all the false ones,
    because for grouped triggers all its members have to be True.
    """
    for trigger in triggers:
        if not trigger.get_condition():
            # Delete all the group members as well
            group = trigger.get_config("group", ignore=True)
            if group is None:
                continue

            for group_trigger in triggers:
                if group_trigger.get_config("group", ignore=True) == group:
                    group_trigger.deactivate_trigger()
    return triggers




