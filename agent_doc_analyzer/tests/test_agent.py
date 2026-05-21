"""
Unit tests for the Agent.
"""
import unittest
from src.agent import AnalysisAgent
from src.tools import CalculatorTool, CurrencyFetcherTool
from src.utils import transform_payload

class TestDocAnalyzerAgent(unittest.TestCase):
    def setUp(self):
        self.tools = [CalculatorTool(), CurrencyFetcherTool()]
        self.agent = AnalysisAgent(self.tools)

    def test_full_workflow_calculator(self):
        # 1. Input String
        raw_input = "Please calculate this for me: 10 * (5 + 2)"
        
        # 2. Data Transformation
        formatted_data = transform_payload(raw_input)
        self.assertIn("text", formatted_data)
        
        # 3. Agent Tool Selection & Execution
        result = self.agent.process_command(formatted_data["text"])
        
        # 4. Structured Output
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"], 70)

    def test_full_workflow_currency(self):
        # 1. Input String
        raw_input = "What is the exchange rate for USD to EUR?"
        
        # 2. Data Transformation
        formatted_data = transform_payload(raw_input)
        
        # 3. Agent Tool Selection & Execution
        result = self.agent.process_command(formatted_data["text"])
        
        # 4. Structured Output
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["pair"], "USD_EUR")

    def test_error_boundary_invalid_command(self):
        # Invalid command that doesn't map to any tool keywords
        result = self.agent.process_command("Hello agent, how are you today?")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "No suitable tool found for the given command.")
        
if __name__ == "__main__":
    unittest.main()
