"""
Tests for API module
"""

import unittest
from unittest.mock import Mock, patch
from rest_client import load_options_from_rest, get_btc_spot_rest


class TestRestClient(unittest.TestCase):
    """Test cases for REST client"""

    @patch("rest_client.requests.get")
    def test_load_options_success(self, mock_get):
        """Test successful options loading"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": [
                {
                    "id": 1,
                    "symbol": "BTC-30DEC21-50000-CE",
                    "strike_price": 50000,
                    "contract_type": "call_options",
                    "underlying_asset": "BTC",
                    "settlement_time": "2021-12-30",
                }
            ]
        }
        mock_get.return_value = mock_response

        options = load_options_from_rest()
        self.assertEqual(len(options), 1)
        self.assertEqual(options[0]["strike"], 50000)

    @patch("rest_client.requests.get")
    def test_load_options_empty(self, mock_get):
        """Test empty response handling"""
        mock_response = Mock()
        mock_response.json.return_value = {"result": []}
        mock_get.return_value = mock_response

        options = load_options_from_rest()
        self.assertEqual(len(options), 0)


if __name__ == "__main__":
    unittest.main()