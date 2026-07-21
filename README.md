# Arm Memory Agent

Arm Memory Agent is a small, reproducible AI-agent optimization project for the Arm AI Optimization Challenge.

It demonstrates a practical pattern for running agent workflows on CPU-constrained Arm64 environments: instead of sending every prior note, source, and instruction back through the model context, the agent keeps a compact memory store, retrieves only relevant evidence, and emits an auditable prompt pack.

## Why this matters

Many education, support, and research agents become slow and expensive because they keep appending conversation history. This prototype measures a lean alternative:

- short-term notes are normalized into memory cards;
- repeated facts are deduplicated;
- the prompt is rebuilt from only the most relevant cards;
- every run reports context bytes, selected memory, and timing.

The target use case is a LearnBridge-style tutoring workspace where the learner accumulates notes, files, questions, and section-by-section explanations over time.

## Track

Track 1: MemoryAgent.

The project focuses on persistent memory, retrieval, and context compression for long-running AI interactions.

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

## Arm64 Validation Plan

The project is designed to run without GPU dependencies. The intended validation path is:

1. Run the benchmark on `linux/amd64`.
2. Run the same benchmark on `linux/arm64`.
3. Compare output hashes and timing.
4. Include GitHub Actions logs or local Arm64 terminal screenshots in the Devpost submission.

## Status

Working prototype. No cloud billing, wallet, KYC, paid trial, or private credential flow is required for local development.
