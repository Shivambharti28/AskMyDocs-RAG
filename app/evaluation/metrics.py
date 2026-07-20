from typing import Dict, List


def keyword_score(answer: str, expected_keywords: List[str]) -> Dict:

    # Convert answer to lowercase
    answer = answer.lower()

    matched_keywords = []
    missing_keywords = []

    # Check every keyword
    for keyword in expected_keywords:

        if keyword.lower() in answer:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    matched = len(matched_keywords)
    total = len(expected_keywords)

    # Avoid division by zero
    if total == 0:
        score = 100.0
    else:
        score = round((matched / total) * 100, 2)

    return {
        "score": score,
        "matched": matched,
        "total": total,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


if __name__ == "__main__":

    answer = """
    Motivation is an internal psychological process that
    directs human behavior toward goals.
    """

    expected = ["goal", "behavior", "internal", "energy"]

    result = keyword_score(answer, expected)

    print("\nEvaluation Result")
    print("-" * 40)
    print(f"Score: {result['score']}%")
    print(f"Matched: {result['matched']}/{result['total']}")
    print(f"Matched Keywords: {result['matched_keywords']}")
    print(f"Missing Keywords: {result['missing_keywords']}")
