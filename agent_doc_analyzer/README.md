# Agent Document Analyzer

An AI-assisted, modular agent system designed to ingest unstructured financial text files, compute mathematical values safely, and normalize monetary values to a base currency (EUR) via a tool-chain architecture.

## Architecture & Data Conversion
The system relies on a `ToolRegistry` pattern where an intelligent agent loops through inputs and delegates tasks to specific tools:
- **CalculatorTool**: Safely parses and computes mathematical strings via Python's Abstract Syntax Trees (`ast`) without relying on the vulnerable `eval()` function.
- **CurrencyFetcherTool**: Standardizes multi-regional financial data into a standard currency structure.

### Data Ingestion Layer (`src/utils.py`)
All inputs are piped through the `transform_payload` function prior to processing. It handles irregular inputs by parsing semi-structured text (like loose CSV formats or key-value structures) into strict JSON dictionaries. Any unstructured fragments are bundled into a `raw_items` list or `text` fallback node, ensuring absolute data preservation across the pipeline.

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MathisBernarde/Python-AI.git
   cd Python-AI/agent_doc_analyzer
   ```

2. **Initialize a Virtual Environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Basic execution variables are located in `config/settings.py`. You can adjust:
- `MAX_AGENT_ITERATIONS`: The limits for the agent's reasoning loop.
- `LLM_TEMPERATURE`: Configuration for future LLM integration.
- `USE_MOCK_API`: Toggle whether the `CurrencyFetcherTool` should use mock dictionaries or real API connections.

*(Optional)* You may set environment variables on your system:
```bash
export USE_MOCK_API=True
export CURRENCY_API_BASE_URL="https://api.exchangerate.host"
```

## Execution Example

Launch the interactive CLI by running:
```bash
python main.py
```

**Example Session:**
```text
Welcome to the Agent Document Analyzer CLI
Type 'exit' or 'quit' to stop.

Enter command or data > What is the exchange rate for USD to EUR?
Transforming input...
Processing with Agent...

--- Agent Result ---
{
  "status": "success",
  "pair": "USD_EUR",
  "rate": 0.92
}
--------------------
```

## System Deployment Strategy

### Phase 1: CLI Staging (Current)
The system is currently deployed as a local Command-Line Interface. This controlled staging environment allows engineers to safely validate the deterministic logic of the `CalculatorTool`, the `CurrencyFetcherTool`, and the `transform_payload` pipeline in real-time. It eliminates network latency issues and provides immediate console feedback.

### Phase 2: Microservice API Containerization
For long-term production deployment, wrapping the core `AnalysisAgent` in a lightweight web framework (like FastAPI) and containerizing it with Docker is highly recommended. This approach turns the agent into a scalable, headless microservice that can be continuously polled by front-end dashboards, securely isolated from the host OS (a necessity for tools parsing external text), and orchestrated horizontally using Kubernetes based on incoming text volume.
