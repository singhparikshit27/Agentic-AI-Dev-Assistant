# Agentic AI Software Development Assistant

An autonomous multi-agent AI system designed to generate software solutions from natural language instructions using collaborative AI agents, tool orchestration, and real-time execution monitoring.

## Overview

The Agentic AI Software Development Assistant is an intelligent software engineering platform that combines Large Language Models (LLMs), agent-based reasoning, and automated tool execution to generate code autonomously. The system allows users to provide software requirements in natural language, after which multiple AI agents collaborate to plan, generate, and validate code files.

The project demonstrates modern Agentic AI concepts such as autonomous reasoning, task decomposition, multi-agent collaboration, memory logging, and workflow orchestration through an interactive Streamlit-based interface.

## Features

* Multi-agent AI workflow architecture
* Natural language software requirement processing
* Autonomous code generation
* Planner and Coder agent collaboration
* Tool-based file generation and execution
* Real-time execution logging and audit trail
* Interactive Streamlit dashboard
* SQLite database integration for persistent logs
* Gemini API integration for LLM reasoning
* Visualization of agent activity and execution flow

## System Architecture

The system follows a modular agentic architecture consisting of:

* User Interaction Layer
* Reasoning and Planning Agent
* Tool Execution Layer
* Database Logging and Memory Layer
* Orchestration Module
* Output Generation Module

The agents collaborate to interpret user goals, generate execution plans, invoke tools, create files, and maintain execution history.

## Technologies Used

* Python
* Streamlit
* Gemini API
* LiteLLM
* SQLite
* SQLAlchemy
* Pandas
* dotenv

## Project Workflow

1. User enters a software requirement through the Streamlit UI.
2. The Planner Agent analyses and decomposes the task.
3. The Coder Agent generates required files and code.
4. The system logs all actions into the database.
5. Generated outputs and execution logs are displayed in the dashboard.

## Installation

Clone the repository:

```bash
git clone <your-repository-link>
cd AgenticSoftwareDevAssistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## Example Task

Example user instruction:

```text
Create a Flask API with a /health endpoint returning {'status':'ok'} and generate a requirements.txt file.
```

The AI agents automatically generate the required files and display execution logs in the interface.

## Future Enhancements

* Multi-agent reviewer and testing agents
* Docker container execution
* Retrieval-Augmented Generation (RAG)
* Long-term vector memory integration
* Automated debugging and self-correction
* Cloud deployment support

## Disclaimer

This project depends on external LLM APIs such as Gemini. Temporary API rate limits or service availability issues may occur during high server demand.

## License

This project is intended for educational and research purposes.
