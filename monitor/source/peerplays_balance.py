from peerplays.account import Account
from graphenecommon.exceptions import AssetDoesNotExistsException, AccountDoesNotExistsException
from . import AbstractSource
import logging


class PeerplaysBalance(AbstractSource):
    """Retrieves the current balance of an account on peerplays. All available config values are:

        * account_name: <account_name>
        * symbol: <asset>
    """
    def __init__(self, source_config, source_name):
        super().__init__(source_config, source_name)
        self.asset = self.get_asset()
        self.account_name = self.get_account_name()

    def get_asset(self):
        asset = self._get_config_value("symbol")
        if asset is None:
            logging.error("Missing 'symbol' key in config of {0}".format(self.get_source_name()))
            return None
        return asset

    def get_account_name(self):
        account_name = self._get_config_value("account_name")
        if account_name is None:
            logging.error("Missing 'account_name' key in config of {0}".format(self.get_source_name()))
        return account_name

    def retrieve_data(self):
        self.data = None
        if self.account_name is None or self.asset is None:
            logging.error("retrieve data of source Peerplays Balance failed, because of missing information")
            return None

        try:
            self.data = Account(self.account_name).balance(self.asset).amount
        except AssetDoesNotExistsException as e:
            logging.error("Asset does not exist: " + str(e))
        except AccountDoesNotExistsException as e:
            logging.error("Account does not exist: " + str(e))
        except ValueError as e:
            logging.error(str(e) + " -- This usually happens when Peerplays is not set up correctly.")
