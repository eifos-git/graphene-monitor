from . import AbstractSource
import requests


class Http(AbstractSource):
    def get_url(self):
        return self._get_config_value("url")

    def retrieve_data(self):
        """Returns the status code of the http request. """
        self._set_data()
        try:
            url = self.get_url()
            if url is None:
                return
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            return
        self._set_data(r.status_code)

