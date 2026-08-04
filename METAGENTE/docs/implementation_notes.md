# Implementation Notes

This document highlights the design decisions made when adapting the original Metagente repository (Nguyen et al.) into this minimal prototype.

## Preserving the Conceptual Architecture
The academic validity of this prototype relies on preserving the *conceptual* architecture of Metagente. The following elements were preserved and carefully adapted:
1. **Agent Roles**: The logical sequence of Extractor -> Summarizer -> Teacher -> Prompt Creator (Combine) remains fully intact.
2. **Prompts**: The exact wording and Python template injection variables (`$extracted_text`, `$description`, etc.) from the original `prompt/prompt.py` were transferred verbatim.
3. **Evaluation Metric**: The ROUGE calculation logic using `rouge-score` with `use_stemmer=True` was replicated.
4. **Sequential Optimization Loop**: The behavioral flow from the original `optimizer/sequential_optimizer.py` dictates the orchestrator's logic.

## Simplifying the Physical Structure
While the conceptual logic was preserved, the *physical* repository structure was significantly simplified. 

The original implementation was a deeply nested Python package relying on monolithic CSV data loading and MongoDB tracking. We flattened the architecture into four distinct, filesystem-backed root directories (`data/`, `prompts/`, `scripts/`, `runs/`). 

**Why this matters:** 
This structural simplification makes the prototype thesis-friendly and highly accessible. By abandoning databases and CSVs in favor of plain text files (`.txt` and `.md`), individual data samples, LLM prompts, and generated logs can be easily inspected, version-controlled, and audited manually. Furthermore, this decoupled structure is perfectly suited for AI coding assistants (like Antigravity agents), which excel at navigating and modifying flat, file-based workspaces.

## Omitted Subsystems
To keep the scope strictly to a minimal prototype, several complex subsystems were intentionally excluded:
- **Parallel Optimization**: Only the sequential optimization loop was implemented. Parallel batch processing was deemed out-of-scope.
- **MongoDB Tracking**: Tracking outputs in a local database was replaced with deterministically writing artifacts to the `runs/` directory.
- **Pandas / CSV Data Loading**: Replaced with standard Python file I/O against the `data/` directory.
