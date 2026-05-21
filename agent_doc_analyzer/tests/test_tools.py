"""
Unit tests for external tools.
"""
import unittest
from src.tools import CalculatorTool, CurrencyFetcherTool

class TestTools(unittest.TestCase):
    def setUp(self):
        self.calc_tool = CalculatorTool()
        self.currency_tool = CurrencyFetcherTool()

    def test_calculator_valid_expression(self):
        result = self.calc_tool.execute("(150 + 25) * 1.2")
        self.assertEqual(result["status"], "success")
        self.assertAlmostEqual(result["result"], 210.0)

    def test_calculator_malformed_expression(self):
        result = self.calc_tool.execute("150 + ")
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)

    def test_calculator_invalid_characters(self):
        result = self.calc_tool.execute("import os")
        self.assertEqual(result["status"], "error")
        
    def test_currency_fetcher_valid(self):
        result = self.currency_tool.execute("USD", "EUR")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["pair"], "USD_EUR")
        self.assertIsInstance(result["rate"], float)

    def test_currency_fetcher_invalid(self):
        result = self.currency_tool.execute("XYZ", "ABC")
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"])

if __name__ == "__main__":
    unittest.main()
