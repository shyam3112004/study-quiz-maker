import json
import logging
import os
import re
from pathlib import Path
from typing import List, Literal, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

try:
    from google import genai
    from google.genai import errors as genai_errors
    from google.genai import types as genai_types
except ImportError:
    genai = None
    genai_errors = None
    genai_types = None

try:
    import httpx
except ImportError:
    httpx = None

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("study-quiz-maker")

# Load environment variables
load_dotenv()

RATE_LIMIT_PER_HOUR = os.getenv("RATE_LIMIT_PER_HOUR", "10")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
MAX_NOTES_CHARS = int(os.getenv("MAX_NOTES_CHARS", "6000"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI App
app = FastAPI(
    title="Study Quiz Maker",
    description="Turn study notes into multiple-choice practice quizzes with explanations using Google Gemini API",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware for development safety
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path definitions
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Mount static files directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# Pydantic Schemas
class QuizRequest(BaseModel):
    notes: str = Field(
        ...,
        min_length=20,
        description="Pasted study notes or syllabus text",
    )
    num_questions: int = Field(
        default=5,
        ge=3,
        le=10,
        description="Number of multiple-choice questions to generate (3 to 10)",
    )
    difficulty: Literal["easy", "medium", "hard"] = Field(
        default="medium",
        description="Difficulty level of questions",
    )


class QuestionItem(BaseModel):
    id: int
    question: str
    options: List[str]
    answer_index: int
    explanation: str


class QuizResponse(BaseModel):
    quiz_id: str
    title: str
    num_questions: int
    difficulty: str
    questions: List[QuestionItem]
    is_demo: bool = False


# Schema models for strict structured output with google-genai SDK
class GeminiQuestion(BaseModel):
    id: int = Field(description="Question number starting from 1")
    question: str = Field(description="The question prompt")
    options: List[str] = Field(description="Exactly 4 distinct plausible options")
    answer_index: int = Field(description="Integer index (0 to 3) of the correct option")
    explanation: str = Field(description="Concise 1-3 sentences explaining why the correct answer is right and correcting misconceptions")


class GeminiQuizPayload(BaseModel):
    title: str = Field(description="Brief quiz title based on the notes")
    questions: List[GeminiQuestion] = Field(description="List of multiple-choice questions")


def clean_json_text(text: str) -> str:
    """Strip markdown code fences and whitespace from model output."""
    if not text:
        return ""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def generate_fallback_demo_quiz(notes: str, num_questions: int, difficulty: str) -> List[QuestionItem]:
    """
    Fallback demo quiz generator used strictly when GEMINI_API_KEY is not configured
    or during offline testing, allowing immediate interactive evaluation of the UI.
    """
    sample_pool = [
        {
            "question": "Based on the provided notes, what is the primary concept or mechanism described?",
            "options": [
                "The core principle described in the opening section",
                "An unrelated external theoretical model",
                "A secondary corollary without empirical validation",
                "An obsolete hypothesis superseded by modern research",
            ],
            "answer_index": 0,
            "explanation": "The opening notes highlight this foundational principle as the central mechanism.",
        },
        {
            "question": "Which of the following factors plays a critical role in the processes mentioned?",
            "options": [
                "Random fluctuations without specific direction",
                "Key environmental and structural conditions cited in the text",
                "Solely static equilibrium states",
                "Variables completely excluded from the problem scope",
            ],
            "answer_index": 1,
            "explanation": "Specific conditions and structured inputs cited in the notes govern how the process behaves.",
        },
        {
            "question": "How does increasing difficulty or complexity affect the analysis according to standard study guidelines?",
            "options": [
                "It eliminates the need for foundational formulas",
                "It demands synthesis of multiple sub-principles and deeper active recall",
                "It reduces the problem to trivial inspection",
                "It has no measurable influence on the outcome",
            ],
            "answer_index": 1,
            "explanation": f"At {difficulty} level, questions test synthesis across interconnected concepts rather than isolated facts.",
        },
        {
            "question": "What is the recommended approach for validating results derived from these study notes?",
            "options": [
                "Passive memorization of raw definitions without testing",
                "Active self-testing, problem solving, and error review",
                "Ignoring edge cases and conflicting evidence",
                "Assuming initial assumptions are always without error",
            ],
            "answer_index": 1,
            "explanation": "Active recall and explanation review strengthen memory pathways and clarify misconceptions.",
        },
        {
            "question": "Which conclusion best synthesizes the key takeaway of the provided notes?",
            "options": [
                "The subject matter lacks structured relationships",
                "Systematic understanding of definitions and mechanics enables rapid problem solving",
                "Only rote memorization leads to long-term mastery",
                "The concepts cannot be applied in practice",
            ],
            "answer_index": 1,
            "explanation": "A structured understanding of the core notes provides the foundation for mastery and problem solving.",
        },
        {
            "question": "When examining boundary conditions in these notes, which consideration is paramount?",
            "options": [
                "Ensuring constraints and prerequisites are satisfied before applying general rules",
                "Disregarding initial baseline values",
                "Assuming infinite limits apply universally",
                "Bypassing verification steps",
            ],
            "answer_index": 0,
            "explanation": "Boundary constraints determine whether the primary rules and theorems apply.",
        },
        {
            "question": "What distinguishes the primary subject from adjacent topics?",
            "options": [
                "Distinct functional characteristics and specific behavioral rules outlined in the text",
                "Zero measurable differences",
                "Arbitrary naming conventions without functional distinction",
                "Complete divergence with no shared principles",
            ],
            "answer_index": 0,
            "explanation": "The text defines distinct functional properties that characterize the subject.",
        },
        {
            "question": "Why is active explanation of correct and incorrect answers beneficial?",
            "options": [
                "It reveals the rationale behind distractors and confirms true understanding",
                "It is purely decorative with no pedagogical value",
                "It replaces the need to understand underlying theorems",
                "It confuses the learner by introducing too much detail",
            ],
            "answer_index": 0,
            "explanation": "Reviewing explanations exposes why distractors are invalid and reinforces correct principles.",
        },
        {
            "question": "In standard evaluation criteria, what indicates mastery of this topic?",
            "options": [
                "Inability to explain the reasoning to a peer",
                "Accurately selecting the correct answer and articulating the underlying mechanism",
                "Guessing without justification",
                "Relying solely on external hints",
            ],
            "answer_index": 1,
            "explanation": "True mastery involves both correct selection and the ability to articulate why it holds.",
        },
        {
            "question": "What next step is most effective after completing this practice set?",
            "options": [
                "Reviewing missed questions, re-reading troublesome notes, and retrying",
                "Immediately discarding all notes",
                "Assuming 100% retention indefinitely",
                "Avoiding further practice",
            ],
            "answer_index": 0,
            "explanation": "Targeted review of missed concepts closes knowledge gaps and cements retention.",
        },
    ]

    selected = sample_pool[:num_questions]
    result = []
    for idx, item in enumerate(selected, start=1):
        result.append(
            QuestionItem(
                id=idx,
                question=item["question"],
                options=item["options"],
                answer_index=item["answer_index"],
                explanation=item["explanation"],
            )
        )
    return result


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    api_key_configured = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")
    return {
        "status": "healthy",
        "app": "Study Quiz Maker",
        "version": "1.0.0",
        "provider": "Google Gemini",
        "model": GEMINI_MODEL,
        "max_notes_chars": MAX_NOTES_CHARS,
        "rate_limit_per_hour": RATE_LIMIT_PER_HOUR,
        "gemini_api_configured": api_key_configured,
    }


@app.post("/quiz", response_model=QuizResponse, tags=["Quiz"])
@limiter.limit(f"{RATE_LIMIT_PER_HOUR}/hour")
async def generate_quiz(request: Request, payload: QuizRequest):
    """
    Generate multiple-choice practice quiz with 4 options, answer index, and explanations.
    All AI generation happens securely on the server via Google Gemini API.
    """
    # Validate notes length against server MAX_NOTES_CHARS
    notes_clean = payload.notes.strip()
    if len(notes_clean) > MAX_NOTES_CHARS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Notes exceed the maximum allowed length of {MAX_NOTES_CHARS} characters (current: {len(notes_clean)}).",
        )

    # Check if Gemini API key is configured
    api_key_configured = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")

    # Offline sample-quiz fallback only for when no key is set
    if not api_key_configured:
        logger.warning("GEMINI_API_KEY not configured. Falling back to structured demo quiz for local preview.")
        demo_questions = generate_fallback_demo_quiz(
            notes=notes_clean,
            num_questions=payload.num_questions,
            difficulty=payload.difficulty,
        )
        return QuizResponse(
            quiz_id=f"demo-{os.urandom(4).hex()}",
            title="Study Practice Quiz (Demo Mode)",
            num_questions=len(demo_questions),
            difficulty=payload.difficulty,
            questions=demo_questions,
            is_demo=True,
        )

    if not genai:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The google-genai package is not installed on the server.",
        )

    # System prompt enforcing pedagogical quality and strict JSON schema
    system_prompt = (
        "You are an expert pedagogical study quiz maker. Your job is to transform a student's study notes "
        "into high-quality multiple-choice questions for active recall practice.\n\n"
        "Guidelines:\n"
        f"- Generate exactly {payload.num_questions} multiple-choice questions based on the notes.\n"
        f"- Target difficulty level: {payload.difficulty.upper()}.\n"
        "- For each question, provide exactly 4 distinct plausible options (A, B, C, D).\n"
        "- Only ONE option must be clearly correct.\n"
        "- The 'answer_index' must be an integer from 0 to 3 corresponding to the correct option index.\n"
        "- The 'explanation' must be concise (1-3 sentences) explaining why the correct answer is right and correcting common misconceptions.\n"
        "- Respond ONLY with valid, parseable JSON conforming to the schema. Do NOT include markdown commentary outside the JSON structure."
    )

    user_prompt = (
        f"Generate {payload.num_questions} multiple-choice questions ({payload.difficulty} difficulty) "
        f"from these study notes:\n\n---\n{notes_clean}\n---"
    )

    client = genai.Client(api_key=GEMINI_API_KEY)
    config = genai_types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=GeminiQuizPayload,
    )

    # Strict JSON output with retry once on bad JSON / invalid schema
    last_parse_error = None
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=user_prompt,
                config=config,
            )

            raw_output = getattr(response, "text", "") or ""
            if not raw_output:
                raise ValueError("Model returned an empty response")

            cleaned_json = clean_json_text(raw_output)
            data = json.loads(cleaned_json)

            quiz_title = data.get("title", "Study Practice Quiz")
            raw_questions = data.get("questions", [])

            if not isinstance(raw_questions, list) or len(raw_questions) == 0:
                raise ValueError("Response does not contain a valid questions list")

            validated_questions: List[QuestionItem] = []
            for idx, q in enumerate(raw_questions, start=1):
                q_text = str(q.get("question", "")).strip()
                options = q.get("options", [])
                try:
                    answer_idx = int(q.get("answer_index", 0))
                except (ValueError, TypeError):
                    continue
                explanation = str(q.get("explanation", "")).strip()

                if not q_text or len(options) != 4 or answer_idx not in (0, 1, 2, 3):
                    logger.warning("Skipping invalid question item: %s", q)
                    continue

                validated_questions.append(
                    QuestionItem(
                        id=idx,
                        question=q_text,
                        options=[str(opt).strip() for opt in options],
                        answer_index=answer_idx,
                        explanation=explanation or "The selected answer directly corresponds to the notes.",
                    )
                )

            if not validated_questions:
                raise ValueError("No valid questions could be extracted from Gemini response")

            return QuizResponse(
                quiz_id=f"quiz-{os.urandom(4).hex()}",
                title=quiz_title,
                num_questions=len(validated_questions),
                difficulty=payload.difficulty,
                questions=validated_questions,
                is_demo=False,
            )

        except (json.JSONDecodeError, ValueError) as exc:
            last_parse_error = exc
            if attempt == 0:
                logger.warning("Failed to parse Gemini output as JSON on attempt 1, retrying once: %s", exc)
                continue
            logger.error("Failed to parse Gemini output as JSON after retry: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The AI model generated an invalid quiz format. Please try again or rephrase your notes.",
            )
        except genai_errors.APIError as exc:
            code = getattr(exc, "code", None)
            status_val = getattr(exc, "status", None)
            msg = getattr(exc, "message", str(exc))
            details = getattr(exc, "details", {})
            logger.error("Gemini API error (code: %s, status: %s)", code, status_val)

            # Friendly error handling
            # Missing or invalid API key
            if code in (400, 401, 403) and (
                "api_key" in str(msg).lower()
                or "api key" in str(msg).lower()
                or "api_key_invalid" in str(details).lower()
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Gemini API key. Please check GEMINI_API_KEY in your .env configuration.",
                )

            # Rate limit
            if code == 429 or status_val == "RESOURCE_EXHAUSTED" or "quota" in str(msg).lower() or "rate limit" in str(msg).lower():
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Gemini API rate limit reached. Please wait a minute before generating again.",
                )

            # Model not found
            if code == 404 or status_val == "NOT_FOUND" or "not found" in str(msg).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The requested Gemini model '{GEMINI_MODEL}' was not found. Please check GEMINI_MODEL in your environment variables.",
                )

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Gemini API returned an error ({code or 'unknown'}): {msg}",
            )
        except Exception as exc:
            # Check for network or connection errors
            exc_name = type(exc).__name__
            is_network = False
            if httpx and isinstance(exc, (httpx.RequestError, httpx.TimeoutException)):
                is_network = True
            elif "ConnectionError" in exc_name or "Timeout" in exc_name or "Network" in exc_name or "socket" in str(type(exc)).lower():
                is_network = True

            if is_network:
                logger.error("Network error reaching Gemini API: %s", exc_name)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Could not reach the Gemini API. Please check your network connection and retry.",
                )

            logger.exception("Unexpected error during quiz generation: %s", exc_name)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while generating your quiz. Please try again.",
            )


@app.get("/", response_class=HTMLResponse, tags=["Home"])
@limiter.limit(f"{RATE_LIMIT_PER_HOUR}/hour")
async def read_root(request: Request):
    """
    Root endpoint serving the single page application.
    Serves static/index.html when present.
    """
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

    return HTMLResponse(
        content="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Study Quiz Maker</title>
</head>
<body style="background:#0B1F23;color:#F6EFE3;font-family:sans-serif;padding:2rem;">
  <h1>Study Quiz Maker</h1>
  <p>Please build the static frontend in static/index.html.</p>
</body>
</html>"""
    )
