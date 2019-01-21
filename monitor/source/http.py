from source.AbstractSource import AbstractSource
import requests


class Http(AbstractSource):
    def __init__(self, source_config):
        """Gets called before the first monitor iteration starts"""
        super().set_config(source_config)

    def retrieve_data(self):
        """Returns the status code of the http request. """
        try:
            r = requests.get(self.get_config("url"))
        except requests.exceptions.ConnectionError:
            return None
        return r.status_code

