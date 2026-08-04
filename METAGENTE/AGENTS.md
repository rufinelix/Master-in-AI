# Metagente Prototype - Agent Instructions

This project implements a prototype inspired by Metagente from Nguyen et al. for software document summarization. When working in this workspace, AI agents must adhere to the following rules and guidelines:

## Architecture and Roles
- The project uses four logical roles: **extractor**, **summarizer**, **teacher**, and **prompt creator**.

## Directory Structure
- Prompts live under `prompts/`.
- Scripts live under `scripts/`.
- Generated outputs live under `runs/`.
- **Do not create files outside the existing project structure.**

## Workflows and Metrics
- The optimization workflow must use **training samples**.
- The evaluation workflow must use **eval samples**.
- **ROUGE-L** must be used during optimization.

## Agent Behavior
- The agent must always explain the plan before writing multiple files.
- Prefer small, reviewable edits.
