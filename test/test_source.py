import unittest
from . import MockSource
from monitor.source.http import Http
from monitor.source.peerplays_balance import PeerplaysBalance





class TestAbstractSource(unittest.TestCase):
    def setUp(self):
        config = {"class": "test.source_test.mocksource.MockSource"}
        self.source = MockSource(config, "mocksource")

    def test_get_source_name(self):
        self.assertEqual(self.source.get_source_name(), "mocksource")

    def test_get_data(self):
        self.source.retrieve_data()
        self.assertEqual(self.source.get_data(), 0)

    def tearDown(self):
        self.source = None


class TestHttp(unittest.TestCase):
    def setUp(self):
        config = {"class": "monitor.source.http.Http", "url": "https://www.blockchainprojectsbv.com/"}
        self.source = Http(config, "TestHttp")

    def test_get_url(self):
        self.assertEqual(self.source.get_url(), "https://www.blockchainprojectsbv.com/")

    def test_retrieve_data(self):
        self.source.retrieve_data()
        self.assertIsNotNone(self.source.get_data())

    def tearDown(self):
        self.source = None


class TestPeerplaysBalance(unittest.TestCase):
    def setUp(self):
        config = {"class": "monitor.source.peerplays_balance.PeerplaysBalance", "account_name": "init0", "symbol": "TEST"}
        self.source = PeerplaysBalance(config, "PPTest")

    def test_get_asset(self):
        self.assertEqual(self.source.get_asset(), "TEST")

    def test_get_account_name(self):
        self.assertEqual(self.source.get_account_name(), "init0")

    def test_retrieve_data(self):
        self.source.retrieve_data()
        self.assertIsNotNone(self.source.data)

if __name__ == "__main__":
    unittest.main()
