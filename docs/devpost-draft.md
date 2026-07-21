# Devpost Draft

## Project name

Arm Memory Agent

## Elevator pitch

A CPU-friendly MemoryAgent that compresses long learning workspaces into small, auditable prompt packs for Arm64 agent deployments.

## About

Arm Memory Agent explores a simple problem: useful agents remember a lot, but long context makes them slower, harder to audit, and more expensive to run.

The project builds a minimal MemoryAgent workflow inspired by LearnBridge. It stores learning notes as structured memory cards, deduplicates repeated context, retrieves the cards relevant to the current question, and emits a compact prompt pack with a deterministic SHA-256 hash. The benchmark reports raw context size, optimized prompt size, compression ratio, selected memory cards, and runtime.

The goal is not to hide complexity behind a chatbot. The goal is to show a deployable pattern for agents that need persistent memory on Arm64 CPU environments: small inputs, deterministic retrieval, auditable outputs, and no GPU-only dependency.

## Built with

Python, Arm64, MemoryAgent, GitHub Actions, Docker, Devpost

## Testing instructions

Run:

```bash
python -m src.memory_agent_benchmark --dataset examples/learning_notes.jsonl
python -m src.generate_learning_dataset --output examples/synthetic_learning_notes.jsonl --count 180
python -m src.memory_agent_benchmark --dataset examples/synthetic_learning_notes.jsonl --queries examples/query_suite.json --markdown-report reports/benchmark.md
```

Expected output is a JSON report with selected cards, compression ratio, timing, and prompt hash.

## Architecture diagram

Use `docs/architecture.md` for the Mermaid architecture diagram.
