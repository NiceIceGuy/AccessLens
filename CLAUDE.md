# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AccessLens** - An AI-powered accessibility analysis tool that analyzes photos of public spaces to identify accessibility barriers (stairs, narrow paths, blocked entrances, poor signage) and suggests improvements.

## Current State

- **Backend**: Python/FastAPI (in `Backend/`)
- **Frontend**: Not yet created
- **Virtual environment**: `Backend/.venv/` exists but dependencies not installed

## Development Setup

### Backend (FastAPI)

**Location**: `Backend/`

**Activate venv**:
```powershell
cd Backend
.\.venv\Scripts\Activate.ps1
```

**Install dependencies** (run after adding to requirements.txt/pyproject.toml):
```bash
pip install fastapi uvicorn
```

**Run dev server**:
```bash
uvicorn main:app --reload
```
Server runs at `http://localhost:8000` with auto-reload.

**API docs**: `http://localhost:8000/docs` (Swagger UI)

### Project Structure

```
AccessLens/
├── Backend/
│   ├── .venv/           # Python virtual environment
│   ├── main.py          # FastAPI entry point
│   └── (add: requirements.txt, pyproject.toml, app/ modules)
├── CLAUDE.md
├── LICENSE
└── README.md
```

## Architecture Notes

- **API**: REST (FastAPI)
- **ML integration**: TBD (local models vs cloud APIs)
- **Image processing**: TBD (Pillow, OpenCV, etc.)
- **Data storage**: TBD (if needed for analysis history)

## Important Files

- `Backend/main.py` - FastAPI app entry point
- `Backend/.venv/` - Virtual environment (not committed)

## Git Workflow

- Main branch: `main`
- Use conventional commits
- PRs required for changes to main
- `.venv/` is gitignored

## License

MIT License - see LICENSE file for details.