# Arm Memory Agent

Arm Memory Agent is a small, reproducible AI-agent optimization project for the Arm Create: AI Optimization Challenge.

It demonstrates a practical pattern for running agent workflows on CPU-constrained Arm64 environments: instead of sending every prior note, source, and instruction back through the model context, the agent keeps a compact memory store, retrieves only relevant evidence, and emits an auditable prompt pack.

## Why This Matters

Many education, support, and research agents become slow and expensive because they keep appending conversation history. This prototype measures a lean alternative:

- short-term notes are normalized into memory cards;
- repeated facts are deduplicated;
- the prompt is rebuilt from only the most relevant cards;
- every run reports context bytes, selected memory, timing, and a deterministic prompt hash.

The target use case is a LearnBridge-style tutoring workspace where the learner accumulates notes, files, questions, and section-by-section explanations over time.

## Challenge Track

Cloud AI.

The project focuses on Arm64 cloud and CPU-friendly agent infrastructure: persistent memory, retrieval, context compression, reproducible benchmarking, and developer workflows that do not require GPU-only dependencies.

## Quick Start

```bash
python -m src.memory_agent_benchmark --dataset examples/learning_notes.jsonl
```

Generate a larger synthetic dataset and run a query suite:

```bash
python -m src.generate_learning_dataset --output examples/synthetic_learning_notes.jsonl --count 180
python -m src.memory_agent_benchmark --dataset examples/synthetic_learning_notes.jsonl --queries examples/query_suite.json --markdown-report reports/benchmark.md
python scripts/render_architecture.py
```

## Outputs

The benchmark prints:

- raw context size;
- naive full-prompt size;
- compressed context size;
- compression ratio;
- bytes saved against the naive full-prompt baseline;
- selected memory cards;
- execution time;
- prompt pack hash.

When `--queries` is used, the benchmark also reports average compression, total bytes saved, average tag recall, and a Markdown report suitable for a submission README or Devpost evidence section.

Current benchmark evidence:

- 180 memory cards
- 4 benchmark queries
- average compression ratio: `0.0275`
- total bytes saved vs naive prompts: `189596`
- average tag recall: `1.0`
- average runtime: `3.345 ms`

## Arm64 Validation

The project is designed to run without GPU dependencies. The repository includes a GitHub Actions workflow that runs the same benchmark on both `ubuntu-24.04` and `ubuntu-24.04-arm`:

1. Generate the synthetic learning-memory dataset.
2. Run the query-suite benchmark.
3. Rebuild the Markdown benchmark report.
4. Run the unit tests.

This makes the optimization evidence repeatable on standard x86 runners and Arm64 runners.

## Status

Working prototype. No cloud billing, wallet, KYC, paid trial, or private credential flow is required for local development.
