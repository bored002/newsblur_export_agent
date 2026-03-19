# NewsBlur AI Agent 🤖

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An intelligent AI agent built with Python and LangChain that interacts with your [NewsBlur](https://www.newsblur.com/) account. Unlike a static export script, this agent can search, summarize, and categorize your saved stories using natural language.

## ✨ Features

* **Natural Language Interaction:** Ask things like "Summarize my tech stars from this week."
* **Smart Exporting:** Automatically format saved stories into Markdown or JSON.
* **Automated Pagination:** Handles large volumes of "Saved Stories" seamlessly.
* **Contextual Filtering:** Filter stories by content, not just by tags or dates.

## 🛠 Project Structure

```text
newsblur-ai-agent/
├── core/
│   ├── client.py         # NewsBlur API communication logic
│   └── tools.py          # Custom tools for the AI Agent
├── agents/
│   └── news_agent.py     # Agent configuration and LLM setup
├── main.py               # Main entry point (CLI)
├── .env                  # Configuration (API Keys)
└── requirements.txt      # Project dependencies
