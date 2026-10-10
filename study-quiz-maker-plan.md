# Study Quiz Maker: Project Documents (Images Only)

**Project:** A free web app where a student pastes study notes and gets an AI-generated multiple-choice quiz with answers and explanations.
**Experience:** Single-page site with one full-screen background image per section (Home, Paste Notes, Quiz, Score) + quiz generator. No video. No accounts in v1.
**Rule for every document:** One product, one provider (Claude API only). No marketplace, no teacher/vendor features, no payments in v1. Images only, no video.

---

# 01: Image Prompt Doc

**Journey (last scene = first scene):** Quiet study desk at dawn → notes spread open → glowing quiz cards above the page → golden finished-quiz glow → back to the quiet desk at dawn.

| Field | Content |
|---|---|
| STYLE | Warm cinematic still-life photography, 35mm, shallow depth of field, soft morning light, teal shadows and amber highlights, calm and premium |
| ANCHOR_A | A brass desk lamp with a round green-glass shade, warm bulb glowing softly, on the left of the desk |
| ANCHOR_B | An open spiral notebook with cream pages and faint blue ruled lines, no readable writing |
| ANCHOR_C | A small steel tumbler of chai on a white saucer with a thin curl of steam |
| ANCHOR_D | A small potted tulsi plant in a terracotta pot, back right near a window |
| People rule | No people, no hands, no faces, no body parts |
| Negative prompt | people, faces, hands, readable text, letters, logos, watermark, brand names, clutter, blur, distortion, extra objects |
| Image tool | Google Flow (image generation) |
| Sizes needed | Desktop 16:9 (1920×1080) and mobile 9:16 (1080×1920) for every section |

| # | Section | Image | Safe zone (kept clean for UI) |
|---|---|---|---|
| 01 | Home (hero) | @Image2 | Centre-left third: headline and button |
| 02 | Paste Notes | @Image3 | Right half: notes input panel |
| 03 | Quiz | @Image4 | Centre: question cards |
| 04 | Score | @Image5 | Centre: score and "Try again" button |

### IMAGE 00: @Image1: Anchor Line-up (optional reference)

**Mode**: T2I
**Save Image Name As**: @Image1
**Model**: Google Flow image model (best quality)
**Google Flow Image Uploads**:
- None

[Camera] Locked-off tripod, 35mm lens
[Shot] Wide product line-up
[Angle] Eye level, straight on
[Lighting] Soft even morning light from the window
[Composition] All four anchors in a row on a plain wooden desk, equal spacing

Prompt: Warm cinematic still-life photography, 35mm, shallow depth of field, soft morning light, teal shadows and amber highlights. On a plain wooden desk, from left to right: a brass desk lamp with a round green-glass shade glowing softly; an open spiral notebook with cream pages and faint blue ruled lines and no readable writing; a small steel tumbler of chai on a white saucer with a thin curl of steam; a small potted tulsi plant in a terracotta pot. No people, no text, no logos.

> Note: Use this as the style and anchor reference for every other image.

### IMAGE 01: @Image2: Home

**Mode**: T2I
**Save Image Name As**: @Image2
**Model**: Google Flow image model (best quality)
**Google Flow Image Uploads**:
- `@Image1`: (Anchor Line-up: Style Reference)

[Camera] Locked-off tripod, 35mm lens
[Shot] Medium-wide of the desk
[Angle] Slightly high, looking down at about 30 degrees
[Lighting] Soft dawn light through a window on the right, lamp glow on the left
[Composition] Lamp left, notebook centre, chai front right, tulsi back right
[Subject] The quiet study desk before work begins

Prompt: Warm cinematic still-life photography, 35mm, shallow depth of field, soft morning light, teal shadows and amber highlights. A quiet wooden study desk at dawn. On the left a brass desk lamp with a round green-glass shade glowing softly. In the centre an open spiral notebook with cream pages and faint blue ruled lines, no readable writing. In the front right a small steel tumbler of chai on a white saucer with a thin curl of steam. In the back right a small potted tulsi plant in a terracotta pot near a window. The centre-left third of the frame is kept clean and calm for text overlay. No people, no text, no logos.

### IMAGE 02: @Image3: Paste Notes

**Mode**: R2I
**Save Image Name As**: @Image3
**Model**: Google Flow image model (best quality)
**Google Flow Image Uploads**:
- `@Image2`: (Home: Style Reference)

[Camera] Locked-off tripod, 35mm lens
[Shot] Closer medium shot
[Angle] Looking down at about 40 degrees
[Lighting] Bright window light, lamp glow slightly stronger, a faint amber shimmer above the page
[Composition] Notebook centre-left, empty clean space on the right
[Subject] The notebook with a brass pen beside it, a few soft amber particles rising from the pages

Prompt: Same style as @Image2. The same desk and anchors, closer: the open notebook on the centre-left with a brass pen beside it, the brass desk lamp glowing on the left, the chai tumbler at the front and the tulsi plant softly blurred behind. A few soft amber light particles gently rise from the pages. The right half of the frame is kept clean and calm for a notes input panel. No people, no text, no logos.

### IMAGE 03: @Image4: Quiz

**Mode**: R2I
**Save Image Name As**: @Image4
**Model**: Google Flow image model (best quality)
**Google Flow Image Uploads**:
- `@Image2`: (Home: Style Reference)
- `@Image3`: (Paste Notes: Scene Reference)

[Camera] Locked-off tripod, 35mm lens
[Shot] Medium shot
[Angle] Slightly high
[Lighting] Warm amber glow rising from the notebook, soft teal in the shadows
[Composition] Notebook low in frame, three blank translucent cards floating above it, centre kept clear
[Subject] Blank glowing cards arranged in a gentle arc above the notebook

Prompt: Same style as @Image2. The same desk with the brass lamp on the left, the open notebook low in the frame, the chai tumbler in the front right and the tulsi plant behind. Above the notebook, three soft translucent rounded cards with no writing float in a gentle arc, the middle one glowing slightly brighter. The centre of the frame is kept clean for question cards. No people, no text, no logos.

### IMAGE 04: @Image5: Score

**Mode**: R2I
**Save Image Name As**: @Image5
**Model**: Google Flow image model (best quality)
**Google Flow Image Uploads**:
- `@Image2`: (Home: Style Reference)
- `@Image4`: (Quiz: Scene Reference)

[Camera] Locked-off tripod, 35mm lens
[Shot] Medium-wide of the desk
[Angle] Slightly high
[Lighting] Warm golden glow, calm and satisfied
[Composition] Desk anchors in place, a soft golden halo above the notebook, centre clear
[Subject] The desk after the quiz, glowing softly

Prompt: Same style as @Image2. The same desk with the brass lamp on the left, the open notebook in the centre, the chai tumbler in the front right and the tulsi plant in the back right. A soft golden halo of light rests above the notebook and the cards have dissolved into gentle sparkles. The centre is kept clean for the score and button. No people, no text, no logos.

**Image order:** @Image1 (reference) → @Image2 (Home) → @Image3 (Paste Notes) → @Image4 (Quiz) → @Image5 (Score). Scrolling back to the top returns to @Image2, so the journey loops visually.

**Export (desktop 16:9 and mobile 9:16 versions of each image)**

```bash
# Desktop (1920 wide) and mobile (1080 wide) WebP, from the Google Flow downloads
mkdir -p static/assets/images/desktop static/assets/images/mobile

magick home.png   -resize 1920x -quality 80 static/assets/images/desktop/01_home.webp
magick paste.png  -resize 1920x -quality 80 static/assets/images/desktop/02_paste.webp
magick quiz.png   -resize 1920x -quality 80 static/assets/images/desktop/03_quiz.webp
magick score.png  -resize 1920x -quality 80 static/assets/images/desktop/04_score.webp

magick home_mobile.png   -resize 1080x -quality 75 static/assets/images/mobile/01_home.webp
magick paste_mobile.png  -resize 1080x -quality 75 static/assets/images/mobile/02_paste.webp
magick quiz_mobile.png   -resize 1080x -quality 75 static/assets/images/mobile/03_quiz.webp
magick score_mobile.png  -resize 1080x -quality 75 static/assets/images/mobile/04_score.webp
```

Generate the mobile versions by running each prompt again with a 9:16 aspect ratio and the safe zone moved to the top-centre.

**Checklist**
- [ ] Anchors identical in every image
- [ ] No faces, text or logos
- [ ] Safe zones clean
- [ ] Every image saved under its @ImageN name
- [ ] Desktop and mobile version exported for each section

---

# 02: PRD

| Field | Content |
|---|---|
| App name | Study Quiz Maker |
| Tagline | Paste your notes. Get a quiz. Learn faster. |
| Problem | Students re-read notes passively and have no quick way to test themselves on exactly what they are studying. |
| Value proposition | Turn any notes or syllabus topic into a practice quiz with explanations in seconds, free and with no sign-up. |
| Primary persona | College student preparing for semester exams (e.g. engineering students in India) |
| Secondary persona | School student or self-learner revising a topic |
| Internal persona | Developer/maintainer (you) monitoring errors and API cost |

**Core features (must have)**

| # | Feature |
|---|---|
| 1 | Paste notes or a topic, choose number of questions (3 to 10) and difficulty |
| 2 | Generate multiple-choice questions with 4 options, the correct answer and a short explanation using the Claude API |
| 3 | Interactive quiz: pick an answer, see right/wrong with explanation, final score and "Try again" |

**Nice to have (v2):** Tamil/English language switch; saved quiz history (accounts); export quiz as PDF; upload PDF notes; share a quiz by link.
**Out of scope (v1):** Video or animation, user accounts, payments, teacher dashboards, classrooms, native mobile app, marketplace of quizzes.

**User stories**

| As a… | I want to… | So that… |
|---|---|---|
| Student | paste my notes and get a quiz | I can test myself on exactly what I studied |
| Student | see an explanation for each answer | I learn why I was wrong |
| Student | choose the difficulty | the quiz matches my level |
| Student | retry the quiz | I can improve my score |
| Maintainer | see clear error messages and logs | I can fix problems and control API cost |

**Success metrics (first 90 days):** 100 quizzes generated; 20 unique users (classmates and friends); under 5% failed generations; average API cost under ₹1 per quiz; at least 3 pieces of written feedback.

---

# 03: TRD

| Field | Content |
|---|---|
| Frontend | Plain HTML, CSS and JavaScript (single `index.html`), upgradeable to React + Vite + TypeScript in v2 |
| Image layer | Full-screen section backgrounds using CSS `background-size: cover` with desktop and mobile WebP images (`<picture>` or media queries); gentle fade-in on scroll with IntersectionObserver |
| Backend | Python 3.11+, FastAPI, uvicorn |
| Database | None in v1 (stateless). v2: SQLite or Supabase Postgres |
| Auth | None in v1. v2: Supabase Auth (email or Google) |
| Payments | None |
| Email | None in v1 |
| Bot protection | Per-IP rate limit (e.g. 10 quizzes/hour) via `slowapi`; max notes length 6000 chars; optional Cloudflare Turnstile in v2 |
| Hosting | Render free web service (FastAPI serves the static files), or Vercel (static) + Render (API) |
| Scheduled jobs | None |
| Key libraries | fastapi, uvicorn, anthropic, python-dotenv, slowapi, pydantic |
| Third-party APIs | Anthropic Claude API (Messages) |

**Folder structure**

```
study-quiz-maker/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── static/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── assets/
│       └── images/
│           ├── desktop/
│           │   ├── 01_home.webp
│           │   ├── 02_paste.webp
│           │   ├── 03_quiz.webp
│           │   └── 04_score.webp
│           └── mobile/
│               ├── 01_home.webp
│               ├── 02_paste.webp
│               ├── 03_quiz.webp
│               └── 04_score.webp
└── docs/
    └── 01-07 project documents
```

**Naming conventions:** snake_case for Python files and functions; kebab-case for CSS classes; images named by section order (`01_home.webp`).
**Environment variables:** `ANTHROPIC_API_KEY`, `CLAUDE_MODEL` (default `claude-sonnet-5-5`), `RATE_LIMIT_PER_HOUR` (default 10), `MAX_NOTES_CHARS` (default 6000).
**Constraints:** API key never reaches the browser; all validation server-side; response must be strict JSON; each desktop image under about 400 KB and each mobile image under about 250 KB; works on a free hosting tier and a 4G phone.

---

# 04: App Flow

| Field | Content |
|---|---|
| Public pages | `/` (single page with four sections: Home → Paste Notes → Quiz → Score) |
| Booking / order pages | None |
| Customer pages | None in v1 (v2: `/history`) |
| Admin pages | None in v1 (logs viewed in the hosting dashboard) |
| Navigation | Minimal top bar: logo, "How it works" and "Try it" anchors that scroll to sections |
| First screen | Hero: Home image with headline and "Make my quiz" button |
| Section = Image rule | Each section uses exactly one background image from Doc 01 (Home=@Image2, Paste Notes=@Image3, Quiz=@Image4, Score=@Image5) |
| Auth flow (customer) | None in v1. v2: email/Google sign-in via Supabase |
| Auth flow (admin) | None in v1 |

**Journey 1: Generate and take a quiz**
1. Student lands on the Home section and sees the desk image with the headline.
2. Clicks "Make my quiz" and scrolls to the Paste Notes section.
3. Pastes notes, sets number of questions and difficulty, clicks "Generate quiz".
4. Loading state shows; the Quiz section opens with question 1.
5. Selects an answer, sees correct/wrong and the explanation, clicks Next.
6. After the last question, the Score section shows the result.

**Journey 2: Retry**
1. On the Score section, clicks "Try again" to retake the quiz with shuffled order, or "New notes" to return to the input.

**Journey 3: Invalid input**
1. Student submits notes that are too short or too long.
2. Inline error explains the limit; the text stays in the box.

**Journey 4: API failure**
1. Generation fails (rate limit, network or bad JSON).
2. App shows a friendly error with a "Try again" button; notes are preserved.

**Empty states:** Before generating, the Quiz section shows "Paste notes above to build your quiz."
**Loading states:** Button shows a spinner and "Generating…"; skeleton card in the Quiz section.
**Error states:** Inline red text for validation; toast for server or API errors; offline message if the network is down.
**Modals and drawers:** None in v1.
**Redirects:** Unknown routes redirect to `/`.

---

# 05: UI/UX Design Brief

| Field | Content |
|---|---|
| Aesthetic | Calm, warm, premium study-desk feel; minimal UI over full-screen photographic backgrounds |
| Background | Section images from Doc 01 with a dark teal overlay `rgba(11,31,35,.35)` for readability; fallback `#0B1F23` |
| Primary / CTA | Amber `#F2A33A` button with dark text |
| Secondary | Teal `#1F6F78` |
| Accent | Soft gold `#FFD98A` for highlights and score |
| Text | Cream `#F6EFE3` on dark; ink `#1B1B1B` on cream cards |
| Status colours | Correct `#3FA66B`, wrong `#D9534F`, warning `#E6B422` |
| Fonts | Headings: Fraunces (serif); Body: Inter |
| Type scale | 14 / 16 / 20 / 28 / 40 / 56 px (mobile scales down about 20%) |
| Border radius | 16px cards, 999px buttons |
| Shadows | Soft, wide, low-opacity (`0 12px 40px rgba(0,0,0,.25)`) |
| Glass cards | Semi-transparent cream (`rgba(246,239,227,.12)`) with 16px backdrop blur and a 1px light border |
| Dark / light | Dark by default (image-first); light cards for reading questions |
| Motion | Simple: fade and slide-up on section entry (200–300 ms ease-out); no video, no parallax; respect `prefers-reduced-motion` |
| Images as design | Each section's background is one static image; all UI sits inside the safe zones from Doc 01 |
| Reference sites | Apple product pages (clean image sections), Linear (clean dark UI), Notion (calm study tone) |
| Key UI patterns | Sticky progress bar for question number; large tap-friendly answer buttons; instant feedback colours; calm score reveal |
| Mobile | Mobile-first layout; 1080px mobile images; answer buttons at least 48px tall; textarea grows with content |
| Accessibility | WCAG AA contrast (use the overlay); keyboard navigation for answers (1–4 keys, Enter); aria-live for feedback; background images are decorative (no alt needed, content stays in HTML text) |
| Copy tone | Friendly, encouraging, short sentences ("Nice! Here's why.") |

---

# 06: Backend Schema

v1 is stateless, so no tables are required. The schema below is for v2 (saved history) and should not be built in v1.

**Enums:** `difficulty` = easy, medium, hard; `user_role` = student, admin

| Table | Columns |
|---|---|
| profiles | id (uuid, pk, = auth user id), display_name (text), role (user_role, default student), created_at (timestamptz) |
| quizzes | id (uuid, pk), user_id (uuid, fk profiles.id, nullable), title (text), notes_excerpt (text), difficulty (difficulty), num_questions (int), model (text), created_at (timestamptz) |
| questions | id (uuid, pk), quiz_id (uuid, fk quizzes.id), position (int), question (text), options (jsonb, 4 strings), answer_index (int 0–3), explanation (text) |
| attempts | id (uuid, pk), quiz_id (uuid, fk quizzes.id), user_id (uuid, fk profiles.id), score (int), total (int), created_at (timestamptz) |

**Relationships:** profiles 1–N quizzes; quizzes 1–N questions; quizzes 1–N attempts; profiles 1–N attempts.
**Indexes:** quizzes(user_id, created_at desc); questions(quiz_id, position); attempts(user_id, created_at desc).
**Availability / business logic:** Max 10 quizzes per hour per IP (anonymous) or 30 per day per user; notes 20–6000 chars; num_questions 3–10; answer_index must be 0–3 and options length exactly 4 (validated before saving).

| Field | Content |
|---|---|
| Auth provider | None in v1; Supabase Auth in v2 |
| Row level security | v2: users read/write only rows where `user_id = auth.uid()`; admin can read all |
| User roles | student (default), admin |
| File storage | None in v1; v2 optional bucket for uploaded PDF notes |
| Sensitive fields | `notes_excerpt` (may contain personal notes: store minimal text, allow delete); API keys only in server env vars |
| Webhooks / triggers | None |
| API endpoints | `GET /` serves the page; `POST /quiz` generates a quiz (body: notes, num_questions, difficulty); `GET /health` health check; v2: `GET /quizzes`, `POST /attempts` |

---

# 07: Implementation Plan

| Phase | Tasks | Done criteria |
|---|---|---|
| 0: Visual assets | Generate @Image1–@Image5 in Google Flow (desktop and mobile versions); convert to WebP with the export commands in Doc 01 | All 8 WebP files exist in `static/assets/images/` under the right names and size limits |
| 1: Setup | Create repo and virtual environment; install FastAPI, anthropic, python-dotenv, slowapi; add `.env.example`, `.gitignore`, LICENSE and README skeleton | `uvicorn main:app --reload` serves a "hello" page locally |
| 2: Database | Skipped in v1 (stateless); keep the v2 schema in `docs/` only | Decision recorded in README |
| 3: Auth | Skipped in v1 | Decision recorded in README |
| 4: Image frontend | Build the four full-screen sections with background images (desktop and mobile), overlay, fade-in on scroll and reduced-motion fallback | All sections show the correct image on desktop and phone, text is readable |
| 5: Homepage + catalogue | Hero, "How it works" text, top nav; responsive layout inside safe zones | Home and navigation match Doc 05 on desktop and mobile |
| 6: Quiz flow (replaces orders + enquiries) | `POST /quiz`, input form, validation, quiz UI, score screen, retry | A full quiz can be generated and completed end to end |
| 7: Payments | Skipped (free product) | n/a |
| 8: Customer account | Skipped in v1 | n/a |
| 9: Admin dashboard | Skipped; use hosting logs; add `/health` | Errors visible in the Render logs |
| 10: UI polish | Typography, colours, focus states, loading and error states, copy review | Passes the accessibility items in Doc 05 |
| 11: Testing | Test 10 sample note sets (including Tamil/English mix and very short/long text); malformed-JSON retry; rate limit; test on a real phone | No crashes; JSON failures handled; rate limit gives a friendly message |
| 12: Deploy | Deploy to Render; set env vars; test the live URL; add link to README | Live URL works on mobile data; API key not exposed |

**Final done criteria:** A stranger can open the live link on a phone, paste notes, finish a quiz and see a score with explanations, with no errors and under about ₹1 API cost per quiz.

---

## Kickoff prompt for AI coding agent

> Here are my 7 project documents for **Study Quiz Maker**. Treat them as the single source of truth. This is one product using one provider (Claude API only), with no accounts, payments, video or marketplace features in v1. Build strictly phase by phase following Doc 07, and stop for my review at the end of each phase. The design uses one static full-screen background image per section (Home, Paste Notes, Quiz, Score) from `/static/assets/images/{desktop|mobile}/`, with all UI inside the safe zones from Doc 01 and a dark overlay for readability. All validation, rate limiting and the Claude API call must happen server-side, and the API key must never reach the browser. Start with Phase 1.

## Check before going live

- [ ] `.env` is in `.gitignore` and no API key exists anywhere in the git history
- [ ] Rate limit and input length limits are working
- [ ] Spending limit is set in the Claude Console
- [ ] Image files are within the size limits and load fast on mobile data
- [ ] Tested on a real phone
- [ ] README has the live link, a screenshot and setup steps
