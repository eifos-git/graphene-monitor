from source.AbstractSource import AbstractSource
import requests
from urllib3.exceptions import MaxRetryError
#WARNING do not import anything above source
"""Http can be used to test the availability of a website"""


class Http(AbstractSource):
    def __init__(self, source_config):
        """Gets called before the first monitor iteration starts"""
        super().set_config(source_config)

    def retrieve_data(self):
        print("Retreiving Data")
        r = requests.get(self.get_config("url"))
        return r.status_code

