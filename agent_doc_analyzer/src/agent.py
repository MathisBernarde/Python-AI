"""
Core AI Agent implementation.
"""
import re
from typing import List, Dict, Any
from .tools import BaseTool

class AnalysisAgent:
    """Agent class that processes user input and delegates to tools."""
    
    def __init__(self, tools: List[BaseTool]) -> None:
        """
        Initialize the agent with a list of available tools.
        
        Args:
            tools (List[BaseTool]): List of tool instances.
        """
        self.tools = {tool.name: tool for tool in tools}

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Identify the appropriate tool based on keywords and execute it.
        
        Args:
            user_input (str): The raw input command from the user.
            
        Returns:
            Dict[str, Any]: Structured output from the tool execution.
        """
        input_lower = user_input.lower()
        
        try:
            if "calculate" in input_lower or "math" in input_lower or any(op in input_lower for op in ['+', '-', '*', '/']):
                if "calculator" not in self.tools:
                    return {"status": "error", "message": "Calculator tool not available."}
                
                # Extract math expression using a basic regex
                match = re.search(r'([\d\s\+\-\*\/\(\)\.]+)', user_input)
                if match:
                    expression = match.group(1).strip()
                    # Fallback check to ensure it actually contains digits
                    if not any(char.isdigit() for char in expression):
                        raise ValueError("No valid numbers found in expression.")
                    return self.tools["calculator"].execute(expression)
                else:
                    return {"status": "error", "message": "Could not parse math expression."}
                    
            elif "rate" in input_lower or "currency" in input_lower or "exchange" in input_lower:
                if "currency_fetcher" not in self.tools:
                    return {"status": "error", "message": "Currency tool not available."}
                
                # Extract potential currency codes (3 uppercase letters)
                currencies = re.findall(r'\b[A-Z]{3}\b', user_input.upper())
                if len(currencies) >= 2:
                    return self.tools["currency_fetcher"].execute(currencies[0], currencies[1])
                else:
                    return {"status": "error", "message": "Could not parse currency pair. Please specify two 3-letter currency codes."}
            else:
                return {"status": "error", "message": "No suitable tool found for the given command."}
                
        except Exception as e:
            return {"status": "error", "message": f"Agent processing failed: {str(e)}"}
