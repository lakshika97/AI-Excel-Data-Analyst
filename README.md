# AI-Excel-Data-Analyst

Project Description: Autonomous Local Data Analyst
This repository contains a production-ready Streamlit web application that allows users to upload unstructured Excel files (.xlsx, .xls) and perform conversational, natural language data analysis.

Instead of writing manual code or scripts to group, filter, and aggregate datasets, users simply chat with their data. The application converts the raw file dynamically into an optimized, transient SQL environment in memory, leveraging an advanced open-weights Large Language Model via Groq to automatically write, execute, and translate SQL queries back into human-readable insights.

🏗️ Technical Architecture & Workflow
The application operates through three distinct decoupled data handling layers:

[User Excel File] 
       │
       ▼ (Ingestion Layer)
[Pandas DataFrame] ──► (Column Sanitization)
       │
       ▼ (Storage Layer)
[SQLAlchemy SQLite In-Memory Engine] (`uploaded_data` table)
       │
       ▼ (Cognitive Agent Layer)
[LangChain SQL Toolkit] ◄──► [Groq API: Llama 3.3 70B]
       │
       ▼
[Streamlit Chat Interface Response]
1. Ingestion & Pre-processing Layer (Pandas & Streamlit)
File Upload UI: Ingests spreadsheets directly using Streamlit’s native st.file_uploader stream buffer.

Schema Cleansing: Converts spreadsheet sheets into a memory-efficient pandas.DataFrame. To protect SQL query compilers from breaking, a list comprehension implicitly sanitizes raw column headers by stripping out periods (.) and mapping whitespaces to clean underscores (_).

2. Transient Database Layer (SQLAlchemy & SQLite)
Volatile DB Engine: To prevent system clutter and avoid storage overhead, the app establishes an isolated virtual database within system RAM using SQLAlchemy's create_engine("sqlite:///:memory:").

Relational Mapping: The cleansed data collection is exported as a temporary table index named uploaded_data. LangChain's SQLDatabase wrapper targets this engine instance, acting as a metadata proxy that maps schemas, tables, and datatypes without exposing local system directories.

3. Cognitive Agent & LLM Orchestration Layer (LangChain & Groq)
Deterministic Inference Engine: Initializes the high-reasoning Llama 3.3 (70B parameters) model over Groq's high-speed API. The model's sampling configuration is bound to temperature=0 to ensure strict, factual, and repeatable code generation rather than creative text paths.

ReAct Execution Engine: Constructs an autonomous create_sql_agent executing a Zero-Shot Reason-Action-Observation chain. When a prompt is submitted, the model dynamically examines the table schemas, designs syntactic SQL code, executes it natively against the RAM-stored SQLite matrix, reads the raw response rows, and synthesizes the data context into plain English.

Fault Handling: Includes handle_parsing_errors=True, which intercepts any minor structural output or syntax formatting slips, instructing the engine to correct itself automatically in real-time instead of breaking the running thread interface.

🛠️ Core Technology Stack
Frontend Dashboard UI: Streamlit

Core Language Framework: Python 3.x

Data Processing: Pandas & OpenPyXL

Object-Relational Mapping (ORM): SQLAlchemy

Database Driver Engine: SQLite3

AI Core Framework: LangChain (Groq Integration Community Core)

Cognitive Processing Model: Llama-3.3-70b-versatile via Groq Cloud

🚀 Key Functional Features
Zero-Configuration UI: No pre-existing databases or fixed configurations required. Just drop any standard table sheet in and begin asking questions immediately.

Contextual Persistence: Built around Streamlit's st.session_state to retain full operational conversation context history, allowing for multi-step data follow-up questions.

Enterprise-Level Safety: Fully compatible with .streamlit/secrets.toml tracking configurations to safely extract private developer authorization headers out of production source code blocks.
