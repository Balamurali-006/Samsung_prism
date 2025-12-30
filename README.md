🚀 Competitor Intelligence System (CrewAI)

Welcome to the Competitor Intelligence System, a multi-agent AI application built using CrewAI
.
This project leverages collaborating AI agents to automatically discover competitors, collect market data, analyze strategies, and generate structured competitive insights for any given company.

The system is designed to simulate a real-world business intelligence workflow, where each agent focuses on a specialized task and collectively produces a comprehensive competitor analysis report.

🧠 Project Overview

This project performs end-to-end competitor intelligence through four core phases:

Discovery Agent – Identifies key competitors of a given company

Collection Agent – Gathers structured data from competitor websites

Strategic Analysis Agent – Performs SWOT-style strategic evaluation

Aggregation Agent – Combines all outputs into a final report

The output is saved as a structured JSON report, suitable for dashboards, research, or further analysis.

🛠️ Installation
Prerequisites

Python >= 3.10 and < 3.14

Internet connection (for API calls & scraping)

This project uses UV for dependency management.

Install UV
pip install uv

Install Project Dependencies

From the project root directory:

crewai install

🔐 Environment Configuration

Create a .env file in the project root and add the following:

# Groq (Primary LLM)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL_NAME=llama-3.1-8b-instant

# Optional (fallbacks)
OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE=https://api.openai.com/v1

# CrewAI Tracing (optional)
CREWAI_TRACING_ENABLED=true

📁 Project Structure
latest_ai_development/
│
├── src/latest_ai_development/
│   ├── agents/          # Agent definitions
│   ├── crews/           # Crew orchestration logic
│   ├── tools/           # Custom tools (scrapers, token counter, search)
│   ├── schemas/         # JSON output schemas
│   ├── config/          # Agent & task configuration (YAML)
│   ├── main.py          # Entry point
│   └── crew.py          # Crew composition
│
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
├── competitor_report.json
└── README.md

▶️ Running the Project

To generate competitor intelligence for a company (example: Samsung):

python main.py Samsung

📄 Output

After execution, the system generates:

Console logs showing agent execution

A structured file:

competitor_report.json

Report Includes:

Identified competitors

Features, pricing & offerings

Strategic insights:

Strengths

Weaknesses

Opportunities

Threats

📊 Token Usage & Tracing

If tracing is enabled:

setx CREWAI_TRACING_ENABLED true   # Windows


CrewAI automatically logs:

Agent execution flow

Task-level LLM calls

Structured traces via CrewAI dashboard

Custom token tracking can be implemented via:

tools/token_counter.py

🎯 Why CrewAI?

Modular agent architecture

Easy task orchestration

LLM-agnostic (Groq, OpenAI, Gemini)

Real-world business intelligence simulation

🧪 Example Use Cases

Market research

Startup competitor analysis

Product positioning studies

Academic / internship projects

Business strategy prototyping