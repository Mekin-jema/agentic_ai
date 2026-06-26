# LangChain & LangGraph Agentic AI Engineering

## Overview

This project is part of the **Agentic AI Engineering with LangChain & LangGraph** roadmap. It demonstrates a basic LLM application using LangChain and OpenRouter.

The goal is to build toward agentic AI systems, including tools, memory, RAG, and multi-agent workflows.

---

## Current Stage

* Prompt-based LLM application
* Single-chain workflow
* No tools, memory, or RAG yet

---

## Features

* LangChain prompt chaining (LCEL)
* OpenRouter API integration
* Structured prompt templates
* Environment variable configuration
* SSL support for restricted networks

---

## Project Structure

```text
langchain-course/
├── main.py
├── .env
├── README.md
└── .venv/
```

---

## Setup

### Install dependencies

```bash
pip install langchain langchain-openai python-dotenv truststore
```

### Configure environment

```env
OPENROUTER_API_KEY=your_api_key
```

---

## Run

```bash
python main.py
```

---

## Architecture

```text
Input → PromptTemplate → ChatOpenAI (OpenRouter) → Response
```

---

## LLM Configuration

```python
llm = ChatOpenAI(
    model="openai/gpt-4.1-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=300,
)
```

---

## Roadmap

* Prompt engineering and chains
* Tool integration
* Memory systems
* RAG with vector databases
* LangGraph agent workflows
* Multi-agent systems

---

## Tech Stack

* Python
* LangChain
* OpenRouter API
* dotenv
* truststore

---

## Author

Mekin Jemal


