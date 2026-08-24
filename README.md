# documind-rag

A Retrieval-Augmented Generation (RAG) pipeline that lets a user upload a document, ask questions about it, and get back an answer with citations pointing to the source page. Includes a RAGAS-based evaluation framework for measuring retrieval and answer quality.

## Features

- Document ingestion: load, clean, chunk, embed, and store files
- Semantic search over stored documents using ChromaDB
- Question answering via Gemini, grounded in retrieved context, with source citations
- Fallback handling when no relevant context is found, instead of guessing
- RAGAS evaluation suite (Context Precision, Context Recall, Faithfulness, Answer Relevancy)
- FastAPI endpoints for document upload and querying

## Requirements

- Python 3.13.12
- A Gemini API key (https://ai.google.dev)

## Setup

1. Clone the repository and move into the project folder.

```bash
git clone <repo-url>
cd documind-rag
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate        
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Gemini API key.

```
GEMINI_API_KEY=your_key_here
```

5. Run the FastAPI server.

```bash
uvicorn app.main:app --reload
```

6. Open the interactive API docs to try it out.

```
http://127.0.0.1:8000/docs
```

Use `POST /documents/upload` to upload a file, then `POST /query` to ask questions about it.

## Running the Tests

```bash
python -m tests.test_chunking
python -m tests.testing_ingestion_service
python -m tests.testing_rag_service
```

## Running the Evaluation

The evaluation writes fourteen hand-checked questions against a sample document, runs them through the live pipeline, and scores the results with RAGAS.

```bash
python -m evaluations.run_ragas
```

Results are saved to `evaluation/reports/baseline_scores.csv`.

**Note:** this step calls the Gemini API once per question per metric, so it makes a large number of requests. Running it repeatedly in a short window can hit free-tier rate limits.

## Project Structure

```
app/
  api/            FastAPI route definitions
  core/           config, cleaning, chunking, embeddings, LLM client
  models/         SQLAlchemy models
  repository/     ChromaDB and SQLite data access
  schemas/        Pydantic request/response schemas
  service/        ingestion and RAG orchestration logic
  main.py         FastAPI app entry point
evaluation/
  reports/        output CSVs from evaluation runs  
evaluations/
  dataset.py      hand-written evaluation questions and reference answers
  run_ragas.py    runs the pipeline and scores it with RAGAS
tests/
  test files for chunking, ingestion, and the RAG service
data/
  uploads/        uploaded documents land here
```

## Current Configuration

The pipeline currently uses:

- Chunk size: 800 characters, overlap: 100 characters
- Embedding model: BAAI/bge-small-en-v1.5
- Fallback distance threshold: 1.3

These settings were chosen after comparing three configurations with RAGAS; see the evaluation report for details.

## Known Limitations

- Context Recall stays below 0.5 even in the best tested configuration, meaning the pipeline still misses part of the needed information on some questions.
- Evaluation has only been run against one source document so far.