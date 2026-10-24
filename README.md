# Transformer-Based Multilingual Speech Recognition and Context-Aware Intent Understanding — Project Builder

A full-stack starter application that turns a topic/specification into a generated source-code project, previews files, downloads a safe ZIP, and publishes to GitHub after OAuth authorization.

## Features
- React + Vite responsive dashboard
- FastAPI backend with real AI provider integration through an OpenAI-compatible chat completions API
- Topic entry and PDF, DOCX, TXT, PNG/JPG upload with server-side text extraction
- Project analysis and multi-file generation
- File tree and source preview
- ZIP download with path validation and sensitive-file exclusion
- GitHub OAuth login, repository listing/creation, branch-aware file publishing, confirmation UI
- Signed session cookie, OAuth state validation, CSRF token for state-changing requests, upload limits and input validation

## Requirements
- Python 3.11+
- Node.js 20+
- An AI provider API key (OpenAI-compatible endpoint)
- A GitHub OAuth App (only needed for GitHub publishing)

## Setup

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `backend/.env`. Set a long random `SESSION_SECRET`, `AI_API_KEY`, and optionally `AI_BASE_URL` / `AI_MODEL`.
Default AI endpoint is OpenAI's `/v1`; other compatible providers can be configured.

For GitHub publishing, create a GitHub OAuth App:
- Homepage URL: `http://localhost:5173`
- Authorization callback URL: `http://localhost:8000/api/github/callback`
- Set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`.
- The app requests `public_repo` for public repositories and `repo` for private repository access; GitHub OAuth scope behavior is account-wide, so review the scope prompt carefully.

```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend
In another terminal:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173.

## Configuration
See `backend/.env.example` and `frontend/.env.example`. Never commit `.env`. Use HTTPS and a strong secret in production. Configure `FRONTEND_ORIGIN` and `BACKEND_PUBLIC_URL` to match your deployed origins. The development session cookie is not marked Secure for localhost; set `COOKIE_SECURE=true` in HTTPS deployments.

## API
- `POST /api/projects/analyze` — analyze topic / upload
- `POST /api/projects/generate` — generate source files
- `GET /api/projects/{project_id}/files` — list file names and sizes
- `GET /api/projects/{project_id}/file?path=...` — read a single generated file
- `GET /api/projects/{project_id}/download` — download ZIP
- `GET /api/github/login` — begin OAuth
- `GET /api/github/callback` — OAuth callback
- `GET /api/github/status` — connection status
- `POST /api/github/logout` — clear GitHub connection
- `GET /api/github/repositories` — list repositories for the connected user
- `POST /api/github/publish` — create/use repository and commit files

## Notes / limitations
- Generated code is AI-produced and should be reviewed, tested, and scanned before deployment.
- The generated project is held in server memory; restarting the backend clears generated projects and GitHub session data.
- OAuth tokens are kept in a server-side in-memory session store; the browser receives only an opaque, signed, HttpOnly session ID. Restarting the backend clears sessions. For production, use Redis/database-backed sessions, HTTPS-only cookies, CSRF controls, rate limiting, audit logs, and a GitHub App installation flow if distributing to organizations.
- Publishing uses GitHub's Contents API one file at a time, creating a commit per file. This is real publishing, but not an atomic single-commit batch; very large projects may take time and hit API limits.
- OCR is not included. Image uploads are supported via OCR when optional Tesseract is installed and available on PATH; otherwise image extraction returns a clear error.
- The backend validates generated paths and blocks common secret files. Never add actual credentials to a project specification.
