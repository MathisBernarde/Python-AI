"""
Tool definitions including BaseTool, CalculatorTool, and CurrencyFetcherTool.
"""
import ast
import operator
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool."""
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Execute the tool logic."""
        pass

class CalculatorTool(BaseTool):
    """A safe mathematical calculator tool avoiding eval()."""
    
    @property
    def name(self) -> str:
        return "calculator"
        
    def execute(self, expression: str) -> Dict[str, Any]:
        """
        Safely evaluate a mathematical string expression.
        
        Args:
            expression (str): The math expression to evaluate.
            
        Returns:
            Dict[str, Any]: The evaluation result or error message.
        """
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        def _eval(node: ast.AST) -> Any:
            if isinstance(node, ast.Constant):
                if not isinstance(node.value, (int, float)):
                    raise TypeError("Only numbers are supported")
                return node.value
            elif isinstance(node, ast.BinOp):
                return ops[type(node.op)](_eval(node.left), _eval(node.right))
            elif isinstance(node, ast.UnaryOp):
                return ops[type(node.op)](_eval(node.operand))
            else:
                raise TypeError(f"Unsupported operation: {type(node).__name__}")

        try:
            tree = ast.parse(expression, mode='eval').body
            result = _eval(tree)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"CalculatorTool error processing '{expression}': {str(e)}")
            return {"status": "error", "message": str(e)}

class CurrencyFetcherTool(BaseTool):
    """A tool to fetch exchange rates using static mock data."""
    
    @property
    def name(self) -> str:
        return "currency_fetcher"
        
    def execute(self, base_currency: str, target_currency: str) -> Dict[str, Any]:
        """
        Retrieve exchange rate for a currency pair.
        
        Args:
            base_currency (str): The base currency code (e.g., 'USD').
            target_currency (str): The target currency code (e.g., 'EUR').
            
        Returns:
            Dict[str, Any]: Exchange rate details or error message.
        """
        mock_rates = {
            "USD_EUR": 0.92,
            "GBP_EUR": 1.17,
            "JPY_EUR": 0.0062,
            "EUR_USD": 1.09
        }
        
        pair = f"{base_currency.upper()}_{target_currency.upper()}"
        
        try:
            if pair in mock_rates:
                return {
                    "status": "success", 
                    "pair": pair, 
                    "rate": mock_rates[pair]
                }
            else:
                return {
                    "status": "error", 
                    "message": f"Exchange rate for {pair} not found."
                }
        except Exception as e:
            logger.error(f"CurrencyFetcherTool error: {str(e)}")
            return {"status": "error", "message": "Internal error retrieving rates."}
