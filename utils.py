def get_classname_for_config(path_to_class):
    """Returns class name and module name for class seperated.

    Example: config.yaml should have an entry in every S/T/A giving the path to
    your implementaion e.g.: source_class:monitor.source.http.Http
    To properly import it in python we separate monitor.source.http from Http
    """
    for i in range(len(path_to_class)-1, -1, -1):
        if path_to_class[i] is '.':
            return path_to_class[0:i], path_to_class[i+1:]

