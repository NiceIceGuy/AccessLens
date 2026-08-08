import os
import base64
import json
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

app = FastAPI()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Featherless configuration
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_MODEL = os.getenv("FEATHERLESS_MODEL", "google/gemma-4-31B-it")
FEATHERLESS_BASE_URL = os.getenv("FEATHERLESS_BASE_URL", "https://api.featherless.ai/v1")

# Create OpenAI-compatible client for Featherless
featherless_client = None
if FEATHERLESS_API_KEY:
    featherless_client = OpenAI(
        base_url=FEATHERLESS_BASE_URL,
        api_key=FEATHERLESS_API_KEY
    )


class Issue(BaseModel):
    title: str = Field(..., description="Short title of the accessibility issue")
    severity: str = Field(..., description="Severity level: high, medium, low")
    category: str = Field(..., description="Category: mobility, vision, hearing, cognitive")
    description: str = Field(..., description="Detailed description of the issue")
    recommendation: str = Field(..., description="Suggested improvement")


class AnalysisResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Accessibility score 0-100")
    summary: str = Field(..., description="Human-readable summary")
    issues: List[Issue] = Field(..., description="List of detected accessibility issues")


def validate_image_file(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: JPG, JPEG, PNG"
        )

    filename = file.filename or ""
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension. Allowed: .jpg, .jpeg, .png"
        )


def image_to_base64(image_bytes: bytes, content_type: str) -> str:
    """Convert image bytes to base64 data URL with correct MIME type."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    if content_type in ("image/jpeg", "image/jpg"):
        mime = "image/jpeg"
    elif content_type == "image/png":
        mime = "image/png"
    else:
        mime = "image/jpeg"  # fallback
    return f"data:{mime};base64,{encoded}"


ACCESSIBILITY_PROMPT = """You are an accessibility analyst for AccessLens. Analyze this photo of a public space for visible accessibility barriers.

Look for issues such as:
- Stairs or step-only entrances (mobility)
- Narrow pathways or corridors (mobility)
- Blocked or obstructed paths (mobility)
- Unclear, low-contrast, or missing signage (vision)
- Difficult-to-reach controls (buttons, intercoms, keypads) (mobility)
- Navigation issues like unclear routes or missing tactile indicators (vision/mobility)
- Poor lighting (vision)
- Slippery or uneven surfaces (mobility)

Guidelines:
- Do NOT claim exact measurements from a photo (e.g., "path is 32 inches wide")
- Do NOT claim legal or accessibility-code violations
- If something cannot be confirmed visually, use wording like "appears", "may", or "requires physical measurement to confirm"
- Only report issues that are actually supported by what you see in the image
- Be specific about what you observe

Return ONLY valid JSON matching this exact structure. EVERY issue MUST have all 5 fields (title, severity, category, description, recommendation):
{
  "score": <integer 0-100>,
  "summary": "<human-readable summary string>",
  "issues": [
    {
      "title": "<short title>",
      "severity": "<high|medium|low>",
      "category": "<mobility|vision|hearing|cognitive>",
      "description": "<detailed description>",
      "recommendation": "<suggested improvement>"
    }
  ]
}

Example of valid issue object:
{
  "title": "Step-only entrance",
  "severity": "high",
  "category": "mobility",
  "description": "The visible entrance appears to require stairs with no ramp alternative.",
  "recommendation": "Install a ramp or clearly identify a step-free route."
}"""


@app.get("/")
def root():
    return {"status": "AccessLens backend running"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    validate_image_file(file)

    # Check if Featherless client is configured
    if featherless_client is None:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Featherless API key not configured"
        )

    # Read image data
    image_bytes = await file.read()

    # Convert to base64 with correct MIME type
    image_base64 = image_to_base64(image_bytes, file.content_type)

    try:
        # Call Featherless API
        response = featherless_client.chat.completions.create(
            model=FEATHERLESS_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ACCESSIBILITY_PROMPT},
                        {"type": "image_url", "image_url": {"url": image_base64}}
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=2000
        )

        # Extract response content
        content = response.choices[0].message.content

        # Parse JSON from response
        try:
            # Try to extract JSON if wrapped in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            analysis_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse AI response as JSON: {str(e)}"
            )

        # Validate against Pydantic model
        try:
            return AnalysisResponse(**analysis_data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"AI response does not match expected schema: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )