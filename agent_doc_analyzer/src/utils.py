"""
Utility functions for data conversion and ingestion.
"""
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def transform_payload(raw_data: str) -> Dict[str, Any]:
    """
    Normalizes irregular string inputs into a standard JSON/dictionary format.
    Handles comma-separated values, semi-structured key-value text, or valid JSON.
    
    Args:
        raw_data (str): The raw input string.
        
    Returns:
        Dict[str, Any]: A normalized dictionary containing the extracted data.
    """
    raw_data = raw_data.strip()
    
    # Try parsing as JSON first
    try:
        if raw_data.startswith('{') and raw_data.endswith('}'):
            return json.loads(raw_data)
    except json.JSONDecodeError:
        pass
    
    normalized_data = {}
    
    # Handle CSV or semi-structured formats (e.g., "key: value, key2: value2" or "key=value, key2=value2")
    if ',' in raw_data:
        pairs = raw_data.split(',')
        for pair in pairs:
            pair = pair.strip()
            if ':' in pair:
                k, v = pair.split(':', 1)
                normalized_data[k.strip()] = v.strip()
            elif '=' in pair:
                k, v = pair.split('=', 1)
                normalized_data[k.strip()] = v.strip()
            else:
                # If no clear key-value pair, treat as a list item in 'raw_items'
                normalized_data.setdefault('raw_items', []).append(pair)
    else:
        # Fallback for plain unstructured text
        normalized_data["text"] = raw_data
        
    return normalized_data
