# Study Quiz Maker

> **Paste your notes. Get a quiz. Learn faster.**

A focused, single-page web app where students paste study notes or syllabus topics and receive an AI-generated multiple-choice quiz with four options, answers, and clear explanations.

---

## 📖 Overview

- **Provider**: Google Gemini API via the official `google-genai` Python SDK (`GEMINI_MODEL`, e.g., `gemini-3.5-flash-lite` or `gemini-3.8-flash`).
- **Offline Demo Fallback**: When no API key is configured, an interactive sample quiz is automatically served with a small "Demo mode" indicator.
- **Stateless (v1)**: Fast, free, and zero-friction for students—no sign-up or database required.
- **Atmospheric Visual Design**: Warm cinematic study-desk aesthetic with dedicated full-screen background imagery for each section (Home, Paste Notes, Quiz, Score).

---

## 🏗️ Architecture & Technical Stack

- **Backend**: Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **AI Engine**: [Google Gemini API](https://ai.google.dev/) using the official `google-genai` Python SDK with strict JSON schema enforcement (server-side only; keys are never exposed to the client)
- **Rate Limiting**: [SlowAPI](https://github.com/laurentS/slowapi) (per-IP rate limiting, default 10 quizzes/hour)
- **Frontend**: Clean Vanilla HTML5, CSS3, and JavaScript (single page)
- **Visuals**: Section background photography optimized for Desktop (16:9 WebP) and Mobile (9:16 WebP)

---

## 📝 Architectural Decisions (Doc 07)

### Phase 2: Database Decision
- **v1**: **Skipped (Stateless)**. The app generates quizzes on-the-fly and scores them client-side. No user state or data persistence is required for v1, minimizing hosting complexity and privacy overhead.
- **v2 Roadmap**: SQLite or Supabase Postgres will be introduced for saved quiz history and attempt metrics. The proposed schema is documented in `docs/01-07_project_documents.md`.

### Phase 3: Authentication Decision
- **v1**: **Skipped**. Complete zero-friction access without account creation or login walls.
- **v2 Roadmap**: Supabase Auth (Email / Google) will be added when user accounts and history tracking are introduced.

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone and Setup
```bash
git clone <repo-url> study-quiz-maker
cd study-quiz-maker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your Gemini API key:
```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key | *Required for live generation; fallback demo mode used if unset* |
| `GEMINI_MODEL` | Gemini model identifier | `gemini-3.5-flash-lite` |
| `RATE_LIMIT_PER_HOUR` | Max quiz requests per IP per hour | `10` |
| `MAX_NOTES_CHARS` | Maximum character length for pasted notes | `6000` |
| `PORT` | Local server port | `8000` |

### 4. Run the Application
```bash
uvicorn main:app --reload
```
Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Health check is available at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) (reports provider name, model name, and `gemini_api_configured` boolean status, never the key).

---

## 💡 Future Ideas

- **Adding a Claude option**: Provide multi-provider support with an option to generate quizzes using Anthropic Claude models alongside Gemini.
- **Saved History**: Optional local storage or database persistence for reviewing past quizzes and tracking revision progress over time.
- **Flashcard Export**: Export generated quizzes and explanations to Anki decks or printable study sheets.

---

## 📂 Repository Structure

```
study-quiz-maker/
├── main.py                     # FastAPI application & Gemini API endpoints
├── requirements.txt           # Python dependencies (google-genai, fastapi, etc.)
├── .env.example               # Template environment configuration (placeholders only)
├── .gitignore                 # Git ignore rules (.env, venv, caches)
├── LICENSE                    # MIT License
├── README.md                  # Project documentation & status
├── docs/                      # Specification & architectural documents
│   └── 01-07_project_documents.md
└── static/                    # Frontend assets
    ├── index.html
    ├── style.css
    ├── app.js
    └── assets/
        └── images/
            ├── desktop/
            └── mobile/
```

---

## 🧭 Implementation Status (Doc 07)

- [x] **Phase 1: Setup** — Virtual environment, FastAPI app, dependencies, configuration, skeleton & health check.
- [x] **Phase 0: Visual Assets** — Section images (Home, Paste Notes, Quiz, Score) for Desktop (16:9) & Mobile (9:16).
- [x] **Phase 4: Image Frontend** — Section layout with dark teal overlay & smooth scroll transitions.
- [x] **Phase 5: Homepage & Navigation** — Hero, How it works, responsive layout inside safe zones.
- [x] **Phase 6: Quiz Flow** — Server-side Gemini generation endpoint, question player, instant feedback, scoring & retry.
- [x] **Phase 10: UI Polish** — Typography (Fraunces & Inter), accessibility (WCAG AA, ARIA landmarks, keyboard 1-4 & Enter), error states, demo mode indicators.
- [x] **Phase 11: Testing & Validation** — Input edge cases, validation error handling, end-to-end browser verification.
- [ ] **Phase 12: Deployment** — Production setup on Render / Vercel.

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
