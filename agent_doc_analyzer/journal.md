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
