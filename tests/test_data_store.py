"""
Tests for data_store module
"""

import unittest
import data_store


class TestDataStore(unittest.TestCase):
    """Test cases for data store"""

    def setUp(self):
        """Set up test fixtures"""
        data_store.clear_option_data()
        data_store.set_spot_price(None)
        data_store.set_selected_expiry(None)

    def test_set_and_get_option_data(self):
        """Test setting and getting option data"""
        opt_data = {
            "symbol": "BTC-30DEC21-50000-CE",
            "strike": 50000,
            "type": "CE",
            "expiry": "30-Dec-2021",
            "ltp": 1000,
            "oi": 100,
            "iv": 0.5,
        }

        data_store.set_option_data("BTC-30DEC21-50000-CE", opt_data)
        retrieved = data_store.get_option_data("BTC-30DEC21-50000-CE")

        self.assertEqual(retrieved["symbol"], "BTC-30DEC21-50000-CE")
        self.assertEqual(retrieved["strike"], 50000)

    def test_spot_price(self):
        """Test spot price operations"""
        data_store.set_spot_price(45000.0)
        self.assertEqual(data_store.get_spot_price(), 45000.0)

    def test_selected_expiry(self):
        """Test expiry selection"""
        data_store.set_selected_expiry("30-Dec-2021")
        self.assertEqual(data_store.get_selected_expiry(), "30-Dec-2021")

    def test_get_options_by_expiry(self):
        """Test filtering options by expiry"""
        opt1 = {
            "symbol": "BTC-30DEC21-50000-CE",
            "strike": 50000,
            "type": "CE",
            "expiry": "30-Dec-2021",
        }
        opt2 = {
            "symbol": "BTC-31JAN22-50000-CE",
            "strike": 50000,
            "type": "CE",
            "expiry": "31-Jan-2022",
        }

        data_store.set_option_data(opt1["symbol"], opt1)
        data_store.set_option_data(opt2["symbol"], opt2)

        results = data_store.get_options_by_expiry("30-Dec-2021")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["expiry"], "30-Dec-2021")


if __name__ == "__main__":
    unittest.main()