import logfire


def calculate_confidence(chunks: list[dict]) -> dict:
    """
    Calculate confidence based on retrieval scores.
    """

    if not chunks:
        return {
            "level": "LOW",
            "score": 0,
        }

    scores = [
    chunk["score"]
    for chunk in chunks
    if "score" in chunk
]

    if not scores:
        return {
            "level": "LOW",
            "score": 0,
            "top_score": 0,
            "average_score": 0,
        }

    top_score = max(scores)
    avg_score = sum(scores) / len(scores)

    if top_score >= 0.80:
        level = "HIGH"
    elif top_score >= 0.65:
        level = "MEDIUM"
    else:
        level = "LOW"

    confidence = {
        "level": level,
        "score": round(top_score * 100, 1),
        "top_score": round(top_score, 4),
        "average_score": round(avg_score, 4),
    }

    logfire.info(
        "Confidence calculated",
        **confidence,
    )

    return confidence