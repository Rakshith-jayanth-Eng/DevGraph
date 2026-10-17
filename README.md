# DevGraph — An AI Coding Assistant with Project Memory

**DevGraph** is a graph-powered developer assistant that connects technical decisions, software components, dependencies, historical bugs, and fixes to help developers investigate new issues using their project's stored history.

Built for the **Neo4j Developer Assistant with Project Memory** hackathon challenge.

## The Problem

Developers often have to rediscover why code was changed, which components depend on one another, and how previous bugs were resolved. Without structured project memory, important context can be lost between debugging sessions.

## The Solution

DevGraph stores connected project knowledge in **Neo4j Aura** and uses Cypher queries to retrieve relevant historical context. **Gemini** then generates an explanation and suggests investigation steps based on the retrieved records.

### Key Features

- Graph-based project memory using Neo4j nodes and relationships.
- Retrieval of technical decisions, dependencies, historical bugs, and fixes.
- Gemini-powered debugging explanations grounded in retrieved evidence.
- Interactive Streamlit interface.
- Knowledge graph visualization based on relationships retrieved from Neo4j.
- Evidence tables so users can inspect the records supporting an answer.

## Technology Stack

- Python
- Neo4j Aura
- Cypher query language
- Neo4j Python Driver
- Streamlit
- Google Gemini API
- python-dotenv

## Architecture

1. **Knowledge storage:** Project components, decisions, bugs, and fixes are stored as nodes in Neo4j.
2. **Relationship modeling:** Directed relationships capture connections between components and historical records.
3. **Context retrieval:** Cypher queries retrieve connected project information.
4. **AI analysis:** Gemini receives the user's question and the retrieved graph evidence.
5. **Presentation:** Streamlit displays the generated analysis, supporting records, and knowledge graph.

## Project Structure

```text
devgraph/
├── app.py
├── db.py
├── seed.py
├── retrieve.py
├── gemini_test.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or newer
- A running Neo4j Aura database
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd devgraph
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root:

```dotenv
NEO4J_URI=neo4j+s://<your-database-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD="your-database-password"
NEO4J_DATABASE=neo4j
GEMINI_API_KEY="your-gemini-api-key"
```

Replace the example values with your own credentials. Never commit your `.env` file or publish your API keys.

### 5. Seed the demo graph

```powershell
python seed.py
```

This creates or updates the sample ShopAPI project records in Neo4j.

### 6. Run the application

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Demo Scenario

The sample ShopAPI project includes a JWT authentication migration, a historical bug involving a missing Authorization header, and a recorded fix.

A developer can ask whether an HTTP 401 error might be related to the authentication change. DevGraph retrieves relevant project history from Neo4j and asks Gemini to explain the evidence and recommend what to investigate.

## Important Limitations

- The ShopAPI records are simulated demonstration data, not real production incident history.
- The current prototype uses seeded project knowledge; it does not automatically inspect arbitrary repositories or source code.
- Gemini's recommendations are investigative suggestions, not proof of a root cause.
- Database credentials and API keys must be configured locally.
- The project is a hackathon prototype and has not been established as a production-ready developer tool.

## Future Improvements

- Import project architecture and technical decisions directly from repositories.
- Add project-specific memory ingestion and updating.
- Improve retrieval for more complex multi-hop debugging questions.
- Add tests, repository integration, and deployment support.

## Acknowledgment

Built as a prototype for the Neo4j Build Sprint, Bengaluru, under the Developer Assistant with Project Memory challenge.

**DevGraph — Remember the decisions. Connect the history. Debug with context.**