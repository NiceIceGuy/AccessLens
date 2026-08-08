# AccessLens — Product Requirements

## Original problem statement
> I need to make a website that can have an image uploaded to it, preview it. Then it sends the image to a backend which a friend of mine is already working on, we plan to connect the 2 using simple API. The website sends the backend a picture and it will analyze it, the whole idea is to get a picture and the AI will find accessibility points for people with disabilities and send a json file back to the front end to show the user.

## User choices (Feb 2026)
- Project name: **AccessLens**
- Design vibe: clean & professional (Swiss high-contrast)
- Upload options: drag-drop + browse + camera capture + multi-file (all of them)
- Results: BOTH overlay pins on image AND cards below
- No login
- Include an "About us" page

## Architecture
- **Frontend**: React 19 + React Router 7 + Tailwind + Shadcn UI + Phosphor icons
  - Fonts: Space Grotesk (display) + IBM Plex Sans (body) + IBM Plex Mono (labels)
  - Colors: blue `#0055FF` primary, yellow `#FFD600` warning accent, red/green severity
  - Sharp corners, hard black shadows, dashed dropzone, animated scanning laser
- **Backend**: FastAPI at `/api/*`, mock analyzer that returns 3–5 findings per image
  - Env var `ANALYZER_URL` — when set, `/api/analyze` proxies to friend's real backend
  - Findings schema: `{id, x, y, severity, category, title, description, recommendation}`

## Personas
- **Hackathon judge** — visits the site, wants to see a polished demo in under a minute
- **Accessibility advocate** — uploads street/venue photos and gets an actionable checklist
- **The teammate building the backend** — needs a stable JSON contract to plug into

## What's implemented (2026-02-07)
- Home hero, three-step "How it works", scanner section, About page, sticky header, footer
- Drag-and-drop, browse (multi-file), and live-camera capture upload
- Thumbnails strip with per-image status badges (idle / scanning / done)
- Image canvas with animated scan overlay and numbered severity-colored markers
- Results panel: accessibility score, summary, category + severity filters, JSON + text report downloads
- Backend `/api/analyze` mock analyzer + `ANALYZER_URL` proxy fallback
- All interactive elements have `data-testid`
- Testing agent iteration 1: 100% backend + frontend pass

## Backlog / next
- **P1**: Wire real analyzer once teammate ships the endpoint (set `ANALYZER_URL` in `/app/backend/.env`, restart backend)
- **P2**: Shareable result links (persist analysis to Mongo, share URL to open pinned view)
- **P2**: Side-by-side "before/after" comparison for two images
- **P2**: Language toggle (EN + user locale) for improved judging reach
- **P3**: Export PDF report with company logo
- **P3**: WCAG references linked per finding
