from peerplays.account import Account
from graphenecommon.exceptions import AssetDoesNotExistsException, AccountDoesNotExistsException
from ..AbstractSource import AbstractSource
import logging


class PeerplaysBalance(AbstractSource):
    def __init__(self, source_config):
        super().__init__(source_config)
        self.asset = self.get_asset()
        self.account_name = self.get_account_name()

    def get_asset(self):
        try:
            return self.get_config("symbol")
        except KeyError:
            logging.error("Key 'symbol' not found in the config file")

    def get_account_name(self):
        try:
            return self.get_config("account_name")
        except KeyError:
            logging.error("Key 'account_name' not found the config file")

    def retrieve_data(self):
        b = None
        if self.account_name is None or self.asset is None:
            logging.error("retrieve data of source Peerplays Balance failed, because of missing information")
            return None

        try:
            b = Account(self.account_name).balance(self.asset).amount
        except AssetDoesNotExistsException as e:
            logging.error("Asset does not exist: " + str(e))
        except AccountDoesNotExistsException as e:
            logging.error("Account does not exist: " + str(e))
        return b
