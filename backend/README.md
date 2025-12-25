# AI Health Coach - Backend

The backend service for the AI Health Coach application, built with FastAPI and Google Gemini.

## Features
- **API**: RESTful endpoints for chat initialization, message handling, and history retrieval.
- **Context Awareness**: Remembers recent conversation history.
- **Medical Protocols**: Automatically detects symptoms and injects relevant medical protocols into the LLM context.
- **Long-term Memory**: Uses `memori` to recall user details across sessions (isolated per user).
- **Robustness**: Handles LLM failures, network issues, and safety filters gracefully.

## Tech Stack
- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite (via SQLAlchemy & AsyncPG/Aiosqlite) - Swappable for PostgreSQL
- **LLM**: Google Gemini (`gemini-2.5-flash`)
- **Memory**: Memori Platform Integration

## Setup Instructions

### 1. Prerequisites
- Python 3.12+
- Google Cloud API Key
- **`uv` Package Manager** (Recommended):
    -   **Install Guide:** [docs.astral.sh/uv](https://docs.astral.sh/uv/)
    -   **Via Pip:** `pip install uv`
    -   **Windows:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
    -   **macOS/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Installation & Run

We recommend using `uv` for fast and reliable dependency management, but standard `pip` is also fully supported.

#### Using `uv` (Recommended)
```bash
# Navigate to backend
cd backend

# Install dependencies and sync
uv sync

# Run the server
uv run main.py
```

#### Using Standard Pip
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
# Activate: 
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### 3. Environment Configuration
Create a `.env` file in the `backend` directory (copy from `.env.sample`):
```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./curelink.db

# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here
MEMORI_API_KEY=your_memori_api_key_here
```

The server will start at `http://localhost:7000`.

## Architecture Overview

### Structure
- **`app/routes`**: API endpoints (`/chat/*`).
- **`app/services`**: Business logic.
    - `ChatService`: Orchestrates chat flow.
    - `ProtocolService`: Injects medical safety protocols.
    - `HistoryService`: Manages chat context.
- **`app/models`**: SQLAlchemy database models.
- **`app/helper`**: External integrations (`llm_helper`).

### Design Decisions
- **Process Isolation**: Each user gets a unique `disha_chat_{user_id}` process ID in Memori to prevent data leakage between sessions.
- **Protocol Injection**: Keyword-based injection ensures that specific medical advice (e.g., for fever) is always part of the context when relevant.
- **Async**: Built fully async using `asyncio` and `aiosqlite`/`asyncpg` for high concurrency.
