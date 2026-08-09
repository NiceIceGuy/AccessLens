# AccessLens

**AccessLens** is an accessibility-focused web application built for **NGN Hacks 2026**. It lets users upload a photo of a real-world space and receive an AI-assisted accessibility assessment with detected barriers, explanations, and practical improvement suggestions.

> **Goal:** Make accessibility barriers easier to notice and understand.

## What AccessLens Does

A user uploads an image of a physical space. AccessLens sends that image to the backend, where a vision-capable model analyzes the scene for potential accessibility concerns.

The application returns structured results such as:

- An overall accessibility score
- Potential accessibility barriers detected in the image
- Explanations of why those barriers may matter
- Practical recommendations for improvement

AccessLens is intended as an awareness and early-assessment tool. It is **not a replacement for a professional accessibility audit or official code-compliance inspection**.

## How It Works

```text
User uploads photo
        ↓
Frontend web app
        ↓
FastAPI /analyze endpoint
        ↓
Image sent to vision model
        ↓
Structured response validated by Pydantic
        ↓
Accessibility results displayed to the user
```

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- python-multipart
- python-dotenv
- OpenAI Python SDK

### AI / Vision

- `google/gemma-4-31B-it`
- Featherless AI
- OpenAI-compatible API

### Data Flow

- Multipart image upload
- Base64 image encoding
- Structured JSON output
- REST API communication

### Development & Deployment

- Git
- GitHub
- Swagger / OpenAPI
- Render

## API

### `GET /`

Basic API health/root endpoint.

### `POST /analyze`

Accepts an uploaded image and returns an accessibility analysis.

Example request:

```bash
curl -X POST "https://accesslens-hm23.onrender.com/analyze" \
  -H "accept: application/json" \
  -F "file=@example.jpg"
```

Example response structure:

```json
{
  "accessibility_score": 78,
  "issues_detected": [
    "Example accessibility barrier"
  ],
  "explanations": [
    "Why the detected barrier may affect accessibility"
  ],
  "recommendations": [
    "Suggested improvement"
  ]
}
```

## Running the Backend Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd AccessLens
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv Backend/.venv
Backend\.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv Backend/.venv
source Backend/.venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r Backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the API credentials required by the model provider.

```env
FEATHERLESS_API_KEY=your_api_key_here
```

Do **not** commit API keys or `.env` files to GitHub.

### 5. Start the API

From the repository root:

```bash
uvicorn Backend.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

FastAPI's interactive Swagger interface can be used to test the `/analyze` endpoint directly.

## Project Structure

```text
AccessLens/
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── README.md
├── LICENSE
└── .gitignore
```

## Why We Built It

Accessibility barriers are often easy to overlook unless they directly affect you.

A staircase without an alternative route, a narrow path, poor signage, or another environmental obstacle can make a space difficult or impossible for someone to use.

AccessLens explores how image analysis can help surface these barriers earlier and make accessibility considerations easier for more people to understand.

## Challenges

Some of the main challenges we worked through included:

- Connecting image upload, backend processing, and model analysis into one complete pipeline
- Returning predictable structured data instead of unstructured model output
- Validating model responses before sending them to the frontend
- Deploying the backend so the frontend could access it remotely
- Keeping the project useful while recognizing that a single image cannot capture every accessibility requirement

## What We Learned

Building AccessLens taught us that an AI application involves much more than simply calling a model.

We had to think about file handling, prompts, API design, structured output, validation, deployment, frontend integration, and the limitations of image-based analysis.

We also learned that accessibility is highly contextual. Measurements, standards, different types of disabilities, and information outside the camera frame can all matter when evaluating a space.

## What's Next

With more time, we would like to add:

- Visual annotations showing detected barriers directly on the image
- Separate accessibility categories such as mobility, vision, hearing, and cognitive accessibility
- Multi-image analysis for a more complete view of a location
- More detailed recommendations
- Accessibility-standard references where appropriate
- Exportable reports for businesses, schools, and public spaces

## Hackathon

Built for **NGN Hacks 2026**.

## Disclaimer

AccessLens provides AI-assisted observations based on visible information in uploaded images. Results may be incomplete or incorrect and should not be treated as a professional accessibility audit, legal opinion, certification, or code-compliance determination.
