# PATI — Permission-Aware Tool Interfaces  
*A structural safety layer for ReAct agents enforcing least‑privilege tool execution.*

https://doi.org/10.5281/zenodo.20679999

## Overview
ReAct agents can call external tools, giving them powerful capabilities — and equally powerful risks.  
Because **LLM outputs directly determine which tools are executed**, traditional safety methods (prompts, alignment, guardrails) cannot reliably prevent:

- jailbreak‑triggered tool calls  
- hallucinated tool execution  
- incorrect reasoning leading to unsafe actions  
- model‑upgrade regressions  

**PATI (Permission‑Aware Tool Interfaces)** introduces a structural safety boundary at the tool‑execution layer.  
Unauthorized tool calls become *impossible*, regardless of what the LLM outputs.

This repository accompanies the research paper:

**“Permission-Aware Tool Interfaces for Safe ReAct Agents”**  
(English & Japanese versions in `/papers/`)

---

## Core Idea
Each tool declares a `required_permission_level`.  
The agent receives a fixed `user_permission_level` from an external system (RBAC / IAM).

Execution flow:

1. LLM proposes a tool call  
2. PATI injects the user’s permission level  
3. The tool checks `user_permission_level` internally  
4. Unauthorized actions return `"Permission denied"`

This ensures:

- no privilege escalation  
- no jailbreak bypass  
- no hallucination‑triggered actions  
- safety independent of the LLM model  

---

## Minimal Example

```python
def delete_file(path, user_permission_level):
    required = 3
    if user_permission_level < required:
        return "Permission denied"
```

The agent injects the permission automatically:

```python
args["user_permission_level"] = agent.permission
```

Full runnable implementation:

```
appendix/pati_minimal_agent.py
```

---

## Quickstart

A minimal, fully working PATI agent is included.

---

### 0. Prerequisite: Ollama + Qwen Model

This example uses **Ollama** with the `qwen3:1.7b` model.

Install Ollama from the official website:

👉 [https://ollama.com](https://ollama.com)

Then download the model:

```bash
ollama pull qwen3:1.7b
```

Ensure the Ollama server is running.

---

### 1. Environment Setup

This project uses `pyproject.toml` and `uv.lock`.

If you use **uv**:

```bash
uv sync
```

---

### 2. Run the Minimal PATI Agent

```bash
python appendix/pati_minimal_agent.py
```

Expected output:

```
LLM Output: delete_file(path="foo.txt")
Permission denied
```

This confirms that:

- the LLM attempted a high‑privilege tool  
- PATI injected the user’s permission  
- the tool rejected the call  

---

## Repository Structure

```
PATI/
 ├── papers/
 │    └── PATI_ReAct_Agent_EN.pdf
 ├── appendix/
 │    └── pati_minimal_agent.py
 ├── diagrams/
 │    └── architecture.png
 ├── .python-version
 ├── pyproject.toml
 ├── uv.lock
 ├── README.md
 └── LICENSE
```

---

## Key Features

- Structural safety independent of model behavior  
- Drop‑in compatible with ReAct / LangChain / LangGraph  
- Minimal implementation (<200 lines)  
- Extensible to any tool‑based agent  
- Works with any LLM (GPT, Claude, Llama, Qwen, etc.)

---

## License
MIT License — free to use, modify, and integrate.

---

## Citation

```
SwayMagpie (2026). Permission-Aware Tool Interfaces for Safe ReAct Agents.
https://github.com/SwayMagpie/PATI-public
```

---

## Contact

This repository is provided as-is.  
Issues and discussions are welcome, but responses or maintenance are not guaranteed.  


---

