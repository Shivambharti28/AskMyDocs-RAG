from app.evaluation.dataset import EVALUATION_DATA
from app.evaluation.metrics import keyword_score
from app.services.retrieval.rag_pipeline import ask


def run_evaluation():

    print("=" * 80)
    print("ENTERPRISE RAG EVALUATION")
    print("=" * 80)

    total_score = 0

    for index, item in enumerate(EVALUATION_DATA, start=1):

        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print(f"\nQuestion {index}")
        print("-" * 80)
        print(question)

        # Ask the RAG
        # result = ask(question)
        result = ask(
            question=question,
            verbose=False,
        )

        answer = result["answer"]

        print("\nGenerated Answer")
        print("-" * 80)
        print(answer)

        # Evaluate answer
        evaluation = keyword_score(
            answer,
            expected_keywords,
        )

        print("\nEvaluation")
        print("-" * 80)
        print(f"Score              : {evaluation['score']}%")
        print(f"Matched Keywords   : {evaluation['matched_keywords']}")
        print(f"Missing Keywords   : {evaluation['missing_keywords']}")

        confidence = result.get("confidence")

        if confidence:

            print("\nConfidence")
            print("-" * 80)
            print(f"Level              : {confidence['level']}")
            print(f"Score              : {confidence['score']}%")

        print("\nSources")
        print("-" * 80)

        for source in result["sources"]:

            print(f"- {source['source']} " f"(Page {source['page']})")

        total_score += evaluation["score"]

    average = total_score / len(EVALUATION_DATA)

    print("\n")
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(f"Questions Evaluated : {len(EVALUATION_DATA)}")
    print(f"Average Score       : {average:.2f}%")
