from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


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


@app.get("/")
def root():
    return {"status": "AccessLens backend running"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    validate_image_file(file)

    # Read image data (not saved permanently)
    await file.read()

    # Mock analysis response
    mock_issues = [
        Issue(
            title="Step-only entrance",
            severity="high",
            category="mobility",
            description="The visible entrance appears to require stairs.",
            recommendation="Provide or clearly identify a step-free route."
        ),
        Issue(
            title="Narrow pathway",
            severity="medium",
            category="mobility",
            description="Path width appears below 36 inches in sections.",
            recommendation="Widen path to at least 36 inches for wheelchair access."
        ),
        Issue(
            title="Low contrast signage",
            severity="medium",
            category="vision",
            description="Sign text has insufficient contrast against background.",
            recommendation="Use high-contrast colors (4.5:1 ratio minimum)."
        ),
    ]

    return AnalysisResponse(
        score=62,
        summary="Several possible accessibility barriers were found.",
        issues=mock_issues
    )