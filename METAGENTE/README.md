# Metagente-Inspired Summarization Prototype

## Project Goal
This project is a minimal, file-based prototype for software document summarization, inspired by the "Metagente" architecture (Nguyen et al., 2026). It automates the process of extracting, summarizing, and iteratively optimizing prompt instructions for Large Language Models (LLMs).

## Project State

### What is Fully Implemented
- **Filesystem Architecture**: A clear, four-directory structure (`data/`, `prompts/`, `scripts/`, `runs/`).
- **Core Pipeline Scripts**: The orchestration logic (`consolidate_prompts.py`) accurately mimics the sequential data flow of the Extractor, Summarizer, Teacher, and Prompt Creator.
- **Evaluation Metric**: ROUGE-1, ROUGE-2, and ROUGE-L calculation (`rouge_eval.py`) is fully functional.
- **Data Loading**: File-based text loading (`prepare_sample.py`) successfully handles individual training and reference samples.

### What was Adapted from Nguyen et al.
- **Conceptual Agent Roles**: The prototype uses the exact same four logical roles (Extractor, Summarizer, Teacher, Prompt Creator).
- **Prompt Content**: The core system instructions for the LLMs in `prompts/` are verbatim copies from the Nguyen repository to preserve the original semantic intent.
- **ROUGE Evaluation Strategy**: The evaluation script utilizes the `rouge-score` package with `use_stemmer=True`, matching the academic reference.

### What is Mocked
- **LLM API Calls**: To ensure the prototype runs deterministically out-of-the-box for demonstrations without requiring API keys or network requests, the LLM inferences inside `scripts/consolidate_prompts.py` are mocked. The helper functions perform prompt template substitution but return hardcoded text rather than calling an external LLM.

### Future Work
- **Live Model Integration**: Transitioning this from a prototype to a fully operational tool requires enabling the live execution mode. The orchestrator in `scripts/consolidate_prompts.py` is fully prepared to route prompt strings to a live Mistral AI endpoint via the `mistralai` SDK.
- **Scaling to Batch Data**: Future iterations can expand `scripts/consolidate_prompts.py` to iterate over entire directories in `data/train/` rather than single samples.

## Setup Instructions
Ensure you have Python installed, then install the dependencies:
```powershell
pip install -r requirements.txt
```

## Running the Prototype
To execute a single, end-to-end sequential optimization cycle:
```powershell
python scripts/consolidate_prompts.py
```
You can also run the evaluation script independently:
```powershell
python scripts/rouge_eval.py --reference "Expected text" --candidate "Generated text"
```

## Output Artifacts
When the orchestrator runs, it deterministically generates the following artifacts in the `runs/` directory:
- `runs/logs/extracted_text.txt`
- `runs/candidates/candidate_1.txt`
- `runs/metrics/metrics_1.json`
- `runs/logs/teacher_feedback.txt`
- `runs/summaries/optimized_prompt_1.md`
