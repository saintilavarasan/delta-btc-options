"""
Tests for engine module
"""

import unittest
from engine import OptionEngine


class TestOptionEngine(unittest.TestCase):
    """Test cases for option engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.options = [
            {
                "symbol": "BTC-30DEC21-50000-CE",
                "strike": 50000,
                "option_type": "call_options",
                "expiry": "30-Dec-2021",
            },
            {
                "symbol": "BTC-30DEC21-50000-PE",
                "strike": 50000,
                "option_type": "put_options",
                "expiry": "30-Dec-2021",
            },
        ]
        self.engine = OptionEngine(self.options, 50000)

    def test_chain_building(self):
        """Test option chain building"""
        self.assertIn(50000, self.engine.chain)
        self.assertIn("CE", self.engine.chain[50000])
        self.assertIn("PE", self.engine.chain[50000])

    def test_atm_calculation(self):
        """Test ATM strike calculation"""
        atm = self.engine._atm_strike()
        self.assertEqual(atm, 50000)

    def test_tick_update(self):
        """Test tick update"""
        self.engine.update_tick("BTC-30DEC21-50000-CE", ltp=1000, oi=100, iv=0.5)

        ce = self.engine.chain[50000]["CE"]
        self.assertEqual(ce["ltp"], 1000)
        self.assertEqual(ce["oi"], 100)
        self.assertEqual(ce["iv"], 0.5)


if __name__ == "__main__":
    unittest.main()