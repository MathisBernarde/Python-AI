"""
Main CLI application entry point for the Agent Document Analyzer.
"""
import sys
import json
from src.agent import AnalysisAgent
from src.tools import CalculatorTool, CurrencyFetcherTool
from src.utils import transform_payload

def main():
    print("Welcome to the Agent Document Analyzer CLI")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Initialize tools and agent
    tools = [CalculatorTool(), CurrencyFetcherTool()]
    agent = AnalysisAgent(tools)
    
    while True:
        try:
            user_input = input("Enter command or data > ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("Exiting...")
                break
                
            if not user_input:
                continue
                
            print("Transforming input...")
            formatted_data = transform_payload(user_input)
            
            # Using the raw input or the formatted text field if available for command logic
            command_text = formatted_data.get("text", user_input)
            
            print("Processing with Agent...")
            result = agent.process_command(command_text)
            
            print("\n--- Agent Result ---")
            print(json.dumps(result, indent=2))
            print("--------------------\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n[!] An error occurred: {e}\n")

if __name__ == "__main__":
    main()
