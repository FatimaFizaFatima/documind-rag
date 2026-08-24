import os
import time

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

from evaluations.datasets import EVALUATION_QUESTIONS
from app.service.rag_service import answer_question
from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


def collect_pipeline_results():
    """Runs the live pipeline once per question, filling in answer + contexts fresh."""
    for i, entry in enumerate(EVALUATION_QUESTIONS, start=1):
        print(f"Processing question {i}/{len(EVALUATION_QUESTIONS)}: {entry['question'][:60]}...")

        result = answer_question(entry["question"])

        entry["answer"] = result["answer"]
        entry["contexts"] = [source["snippet"] for source in result["sources"]]

        print(f"  Answer: {result['answer'][:80]}...")
        print(f"  Contexts retrieved: {len(entry['contexts'])}")

        time.sleep(2)

    return EVALUATION_QUESTIONS


def build_ragas_dataset(entries):
    """Converts our list of dicts into the Dataset shape RAGAS expects."""
    return Dataset.from_dict({
        "question": [e["question"] for e in entries],
        "answer": [e["answer"] for e in entries],
        "contexts": [e["contexts"] for e in entries],
        "ground_truth": [e["reference_answer"] for e in entries],
    })


def get_evaluator_llm_and_embeddings():
    """Configures RAGAS to use Gemini as its judge, instead of the OpenAI default."""
    evaluator_llm = LangchainLLMWrapper(
        ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY)
    )
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    return evaluator_llm, evaluator_embeddings


def run_evaluation(dataset, evaluator_llm, evaluator_embeddings):
    results = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )
    return results


def save_results(results, path="evaluation/reports/2nd_new_baseline_scores.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = results.to_pandas()
    df.to_csv(path, index=False)
    print(f"\nSaved scores to {path}")


if __name__ == "__main__":
    print("Step 1: Running pipeline on all questions...")
    entries = collect_pipeline_results()

    print("\nStep 2: Building RAGAS dataset...")
    dataset = build_ragas_dataset(entries)

    print("\nStep 3: Configuring Gemini as evaluator...")
    evaluator_llm, evaluator_embeddings = get_evaluator_llm_and_embeddings()

    print("\nStep 4: Running RAGAS metrics (this will take a while — many LLM calls)...")
    results = run_evaluation(dataset, evaluator_llm, evaluator_embeddings)
    print(results)

    print("\nStep 5: Saving results...")
    save_results(results)