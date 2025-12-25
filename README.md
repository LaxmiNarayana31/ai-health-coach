# AI Health Coach

A WhatsApp-like AI Health Coach. Simple, intuitive chat interface with long-term memory and personalized medical protocols powered by Google Gemini.

## Tech Stack

- **Backend:** Python (FastAPI), SQLAlchemy (Async), Pydantic
- **Frontend:** React (Vite), Tailwind CSS
- **Database:** SQLite (for development/ease of setup)
- **LLM:** Google Gemini (`gemini-2.5-flash`) via `google-genai` SDK
- **Package Manager:** `uv` (Backend), `npm` (Frontend)

## Setup Instructions

### Prerequisites
-   Git installed on your machine.
-   Python 3.12+ installed.
-   Node.js and npm installed.
-   **`uv` Package Manager** (Recommended):
    -   Standard Pip works, but `uv` is faster.
    -   **Install Guide:** [docs.astral.sh/uv](https://docs.astral.sh/uv/)
    -   **Via Pip:** `pip install uv`
    -   **Windows:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
    -   **macOS/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/LaxmiNarayana31/ai-health-coach.git
cd ai-health-coach
```

### 2. Backend Setup

1.  Navigate into the backend folder from the project root:
    ```bash
    cd backend
    ```

2.  Create a virtual environment and install dependencies. This project uses `uv` for package management, but standard pip works too.
    ```bash
    # Using uv (Recommended)
    uv sync
    
    # OR using standard pip
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  Configure Environment Variables:
    - Copy `.env.sample` to `.env`:
        ```bash
        cp .env.sample .env
        ```
    - Edit `.env` and provide the following keys:
        - `DATABASE_URL`: Connection string for the database.
          - For SQLite (easiest): `sqlite+aiosqlite:///./curelink.db`
        - `GOOGLE_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/api-keys).
        - `MEMORI_API_KEY`: Get from [Memori Platform](https://app.memorilabs.ai/). This is used for long-term memory management.

4.  Run the server:
    ```bash
    # Using uv
    uv run main.py
    
    # OR standard python
    python main.py
    ```
    The backend will start at `http://127.0.0.1:7000`. Database tables are automatically created on startup.

### 3. Frontend Setup

1.  Open a new terminal window.
2.  Navigate into the project root (if not already there) and then to the frontend directory:
    ```bash
    cd ai-health-coach
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will typically start at `http://localhost:5173`.

## Deployment

To deploy the application to production (e.g., Vercel, Netlify):

1.  **Frontend**:
    -   Set the `VITE_API_URL` environment variable to your deployed backend URL (e.g., `https://your-backend-api.com`).
    -   The build command is `npm run build`.
    -   The output directory is `dist`.

2.  **Backend**:
    -   Deploy as a standard Python/FastAPI application (e.g., on Render, Railway).
    -   Ensure typical environment variables are set (`DATABASE_URL`, `GOOGLE_API_KEY`, `MEMORI_API_KEY`).

## Architecture Overview

The backend is structured into clean layers for maintainability:

-   **`app/routes`**: API endpoints (`/chat/init`, `/chat/message`, `/chat/history`). Handles HTTP requests and responses.
-   **`app/services`**: Business logic.
    -   `ChatService`: Orchestrates the chat flow, saves messages, manages prompt construction.
    -   `HistoryService`: Efficiently retrieves chat history for the UI and LLM context.
    -   `ProtocolService`: Logic to inject specific medical protocols based on user queries.
-   **`app/models`**: Database schema definitions using SQLAlchemy (`User`, `Message`).
-   **`app/helper`**: External integrations, specifically the `llm_helper` for Gemini interaction.

### Design Decisions

-   **Memory Management**:
    -   **Short-term**: We explicitly fetch the last N messages from the database and feed them into the LLM context window for every request. This ensures immediate conversation continuity.
    -   **Isolation**: Used a unique process ID (`disha_chat_{user_id}`) for the memory module to ensure no context leakage between different users.
-   **Protocol Injection**: Before sending the user's query to the LLM, the `ProtocolService` scans the input. If it matches certain health topics, relevant medical protocols are injected into the system prompt. This guides the AI to follow safe and standard advice.
-   **Single Session UX**: The backend is designed to support multiple users, but the frontend currently simulates a "single persistent session" per browser (via LocalStorage), matching the requirements of a WhatsApp-like personal chat.

## LLM Notes

-   **Provider**: Google Gemini.
-   **Model**: `gemini-2.5-flash` (Chosen for balance of speed/latency and reasoning capability).
-   **Prompting Strategy**:
    -   **System Prompt**: Defined in `disha_system.txt`, establishing the persona of "Disha", a friendly and empathetic health coach.
    -   **Context Injection**: Dynamic injection of recent conversation history and specific medical protocols into the generation request ensures the model stays relevant and safe.

## Trade-offs & "If I had more time..."

-   **Database**: Used SQLite for this take-home to make it "run anywhere" without infrastructure setup. For production, simply changing the `DATABASE_URL` would switch this to PostgreSQL.
-   **Authentication**: Currently, user identity is "trust-on-first-use" generated by the backend and stored in the frontend's LocalStorage. A real app would need secure authentication (OTP/OAuth).
-   **Vector Search**: The protocol matching is currently basic. With more time, I would implement RAG (Retrieval-Augmented Generation) using a vector database (like `pgvector` or `Chroma`) to semantically search through a large knowledge base of medical protocols instead of keyword/heuristic matching.
-   **Streaming**: The chat currently waits for the full response. Implementing streaming responses (Server-Sent Events) would significantly improve the "WhatsApp-like" feel by showing the message typing out in real-time.
