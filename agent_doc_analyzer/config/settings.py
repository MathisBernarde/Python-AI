"""
Configuration settings and execution constants for the Agent Document Analyzer.
"""
import os
from pathlib import Path

# Application Metadata
APP_NAME = "Agent Doc Analyzer"
APP_VERSION = "0.1.0"

# Path Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Agent Execution Constants
MAX_AGENT_ITERATIONS = 5
LLM_TEMPERATURE = 0.2
DEFAULT_MODEL_NAME = "gemini-3.1-pro"

# Tool Settings
CALCULATOR_PRECISION = 2
USE_MOCK_API = os.getenv("USE_MOCK_API", "True").lower() in ("true", "1", "yes")

# API Configuration
CURRENCY_API_BASE_URL = os.getenv("CURRENCY_API_BASE_URL", "https://api.exchangerate.host")
MOCK_EXCHANGE_RATES = {
    "USD_TO_EUR": 0.92,
    "GBP_TO_EUR": 1.17,
    "JPY_TO_EUR": 0.0062
}
