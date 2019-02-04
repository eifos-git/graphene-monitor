from . import AbstractSource
import requests


class Http(AbstractSource):
    def __init__(self, source_config, source_name):
        """Gets called before the first monitor iteration starts"""
        super().__init__(source_config, source_name)

    def get_url(self):
        return self._get_config_value("url")

    def retrieve_data(self):
        """Returns the status code of the http request. """
        try:
            url = self.get_url()
            if url is None:
                return None
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            return None
        return r.status_code

