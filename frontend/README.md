# AI Health Coach - Frontend

The frontend for the AI Health Coach application, built with React, Vite, and Tailwind CSS. It provides a WhatsApp-like chat interface for interacting with the AI.

## Features
- **UI**: Clean, responsive interface mimicking WhatsApp.
- **Components**:
  - `ChatWindow`: Main chat container with auto-scroll and history loading.
  - `MessageBubble`: Renders user/AI messages with Markdown support.
  - `TypingIndicator`: Visual cue while the AI is generating a response.
- **State Management**: Simple React state, with LocalStorage for session persistence (user ID).
- **API Client**: Centralized Axios client supporting environment-based configuration.

## Tech Stack
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS, Lucide React (Icons)
- **HTTP Client**: Axios

## Setup Instructions

### 1. Prerequisites
- Node.js (v18+ recommended)
- npm (configures with Node)

### 2. Installation & Run
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Development Server
npm run dev
```
The app will open at `http://localhost:5173`. By default, it proxies API requests to `http://localhost:7000`.

### 3. Environment Configuration

#### Development
No configuration needed. The `vite.config.js` is set up to proxy `/chat` requests to the local backend.

#### Production / Deployment
When deploying (e.g., to Vercel, Netlify), you must tell the frontend where the backend is hosted.

**Set the following environment variable in your hosting dashboard:**
- `VITE_API_URL`: The full URL of your deployed backend (e.g., `https://your-backend-app.com`).

**Note:** You do not need a `.env` file for this in production; use the platform's settings.

## Build for Production
To create an optimized production build:
```bash
npm run build
```
The output will be in the `dist` directory.
