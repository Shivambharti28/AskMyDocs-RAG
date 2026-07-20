import logfire
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.retrieval.rag_pipeline import ask

# Configure Logfire
logfire.configure(service_name="enterprise-rag-api")

# FastAPI app
app = FastAPI(
    title="Enterprise RAG API",
    description="Enterprise Document Question Answering API",
    version="1.0.0",
)


# -----------------------------
# Request Model
# -----------------------------
class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Source Model
# -----------------------------
class Source(BaseModel):
    source: str
    page: int | None = None
    score: float | None = None


# -----------------------------
# Response Model
# -----------------------------
class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Enterprise RAG API",
        "version": "1.0.0",
    }


# -----------------------------
# Ask Endpoint
# -----------------------------
@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    try:

        logfire.info(
            "Received Question",
            question=request.question,
        )

        result = ask(request.question)

        logfire.info(
            "Returning Answer",
            sources=len(result["sources"]),
        )

        return QuestionResponse(
            answer=result["answer"],
            sources=[
                Source(
                    source=chunk.get("source", "Unknown"),
                    page=chunk.get("page"),
                    score=chunk.get("score"),
                )
                for chunk in result["sources"]
            ],
        )

    except Exception as e:

        logfire.error(
            "API Error",
            error=str(e),
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health():

    return {"status": "healthy"}
