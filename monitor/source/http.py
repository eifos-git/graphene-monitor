from source.AbstractSource import AbstractSource
#WARNING do not import anything above source
"""Http can be used to test the availability of a website"""

class Http(AbstractSource):
    def __init__(self, source_config):
        """Gets called before the first monitor iteration starts"""
        super().set_config(source_config)

    def retrieve_data(self):
        pass
