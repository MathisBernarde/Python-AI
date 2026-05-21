# Project Journal

## Step 1 – 24.04

**System Description and Goal**
The `agent_doc_analyzer` is a Python-based software system designed to autonomously process unstructured financial text files. Its primary goal is to extract monetary values, compute financial totals, and normalize currencies into a single base currency (EUR) to provide structured, accurate financial summaries.

**AI/Agent-Based Approach**
The system employs a ReAct (Reasoning and Acting) agent architecture. The agent receives user prompts alongside text files, evaluates the necessary steps, and decides which external tools to invoke to fulfill the objective. It iteratively loops through thought, action, observation, and reflection phases until it derives the final summarized financial result.

**List of Tools**
1. **Calculator Tool**: A mathematical evaluation utility for computing sums, taxes, and net totals from extracted figures without relying on the LLM's internal (and potentially flawed) arithmetic.
2. **Currency Fetcher Tool**: An API connector (with a mock fallback) to retrieve current exchange rates for currency normalization.
3. **File Reader Tool**: A utility to ingest and read the contents of local financial text documents.

**Preliminary List of Programming Concepts**
- **Object-Oriented Programming (OOP)**: Structuring the agent, tools, and memory state as distinct, encapsulated objects.
- **Abstract Classes**: Using Python's `abc` module to define a strict `BaseTool` interface.
- **Regex Parsing**: Applying regular expressions to reliably extract amounts and currency symbols from unstructured text.

---

## Step 2 – 08.05

**Updated System Description**
The `agent_doc_analyzer` implementation has progressed to include the core execution loop and tool integrations. The system can now read sample financial texts, identify differing currencies, and invoke the computation logic. The AI component has been refined to explicitly output JSON-formatted action requests, ensuring deterministic and parseable tool triggering during the ReAct loop.

**Refined List of Applied Programming Concepts**
- **Dependency Injection**: External dependencies and tools are injected into the agent's `ToolRegistry` at runtime rather than hardcoded, allowing for isolated unit testing and easy mocking.
- **Structural Pattern Matching**: Python 3.10+ `match/case` statements are utilized in the main event loop to cleanly handle different agent output states (e.g., ToolRequest, FinalAnswer, ParsingError).
- **Decorators**: Implemented a `@tool_logger` decorator to wrap tool executions, abstracting try-catch blocks, execution timing, and logging away from the core tool logic.

**Tool Integration Strategy**
Tools are integrated using a central `ToolRegistry` class functioning under a Factory/Registry pattern. Each tool inherits from `BaseTool` and implements an `execute` method alongside a `get_schema` method that describes its parameters to the LLM. When the agent decides an action is needed, the registry dynamically maps the requested string to the correct instance, executes the tool with the provided parsed arguments, and feeds the output back into the agent's prompt context as an "Observation".

---

## Step 3 – 15.05

**Testing Process and Scenarios**
The testing process validates the individual tool components (unit testing) and the integrated agent workflow (integration testing) concurrently with the implementation phase. Validation utilizes standard `unittest` modules to assert expected behavior under various conditions.

Specific test scenarios include:
1. **Valid Calculation Scenario**: Verifies that the `CalculatorTool` correctly evaluates a complex string (e.g., `(150 + 25) * 1.2`) without relying on `eval()`. It asserts accurate mathematical precedence, ensuring the tool returns `{"status": "success", "result": 210.0}`.
2. **Missing/Corrupt Tool Parameters**: Tests the `CurrencyFetcherTool` with an incomplete or malformed currency pair (e.g., a single currency code or a misspelled code). It asserts that the tool safely catches the validation error and returns a structured error dictionary rather than throwing an unhandled exception.
3. **Corrupt Data Format Handling**: Tests `transform_payload` by passing malformed semi-structured data (e.g., `key1:val1, key2,,val3`). It verifies that the utility gracefully recovers, parsing valid key-values and grouping unstructured fragments into a fallback `raw_items` list.

**Deployment Preparation**
The system is prepared as a lightweight Command-Line Interface (CLI) application. The execution environment requires a standard Python 3.10+ installation. Dependencies are managed via the `requirements.txt` file, and environment variables/constants (such as API toggles) are isolated in `config/settings.py`. Startup is straightforward, requiring the user to run `python main.py` from the root directory to initiate the interactive loop.

**Data Porting and Consistency**
Since input data can be highly unstructured or semi-structured (e.g., irregular comma-separated string payloads), the `transform_payload` function acts as a dedicated conversion layer. It transforms incoming strings into standard JSON dictionaries prior to processing. To preserve data consistency, the conversion logic defaults to retaining unparseable strings within a `text` or `raw_items` node rather than discarding them. This guarantees no information is lost while standardizing the payload for the agent tools.

---

## Final Submission – 22.05

**Final System Description and Goal**
The completed `agent_doc_analyzer` acts as a resilient AI-supported software agent capable of parsing raw text, orchestrating external tools securely, and returning structured outputs. Its ultimate goal of computing values and unifying currencies into a base Euro (EUR) has been fully achieved through the modular ToolRegistry architecture.

**Final Explanation of Programming Concepts and Usage**
- **OOP & Interfaces**: Enabled easy extension of toolkits (e.g., adding `CurrencyFetcherTool`) without modifying the core agent logic.
- **Dependency Injection**: Allowed injecting tools dynamically during the `AnalysisAgent` initialization, making the unit tests straightforward as tools could be mocked.
- **Regex Parsing & AST Safe Eval**: Ensured that extracting parameters from raw strings was robust and executing mathematical sequences (`ast.parse`) entirely circumvented the severe security risks associated with `eval()`.

**Final Description of Tools and Role in the System**
The tool suite functions as the "acting" layer of the ReAct pattern:
- **Calculator Tool**: Processes strings of mathematics, serving as an exact deterministic fallback for the LLM's inherently flawed internal arithmetic.
- **Currency Fetcher Tool**: Supplies exact conversion factors required by the agent to convert values from distinct locales into the standard EUR baseline.

**Final Testing Results and Conclusions**
All 8 test scenarios defined using the `unittest` framework (testing valid logic, corrupt data handling, missing parameters, and unsupported boundaries) passed successfully. The test suite guarantees that both individual components (Tools) and the integrated pipeline (Agent) behave predictably, handle invalid inputs gracefully via error dictionaries instead of crashes, and fulfill the core requirements.

**Final Deployment Preparation Description**
The repository is completely clean and structured. Required dependencies are documented in `requirements.txt`. Execution configurations reside in `config/settings.py`. To deploy the app locally, a user simply clones the repository, installs the dependencies (`pip install -r requirements.txt`), and executes the entry point (`python main.py`).

**Deployment Strategy Proposal**
While currently built as a Command-Line Tool for local testing and controlled validation, the most viable long-term deployment strategy for this system would be an **API-based microservice architecture** (e.g., wrapping `process_command` in a FastAPI endpoint). This approach allows the agent to ingest JSON payloads continuously, horizontally scale depending on concurrent analysis requests, and interface effortlessly with broader enterprise applications (like ERP dashboards).
