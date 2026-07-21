# Devpost Draft

## Project name

Arm Memory Agent

## Elevator pitch

A CPU-friendly memory layer that compresses long agent workspaces into small, auditable prompt packs for Arm64 cloud deployments.

## About

Arm Memory Agent explores a simple problem: useful agents remember a lot, but long context makes them slower, harder to audit, and more expensive to run on CPU-first infrastructure.

The project builds a minimal MemoryAgent workflow inspired by LearnBridge. It stores learning notes as structured memory cards, deduplicates repeated context, retrieves the cards relevant to the current question, and emits a compact prompt pack with a deterministic SHA-256 hash. The benchmark reports raw context size, optimized prompt size, compression ratio, selected memory cards, and runtime.

The goal is not to hide complexity behind a chatbot. The goal is to show a deployable pattern for agents that need persistent memory on Arm64 CPU environments: small inputs, deterministic retrieval, auditable outputs, and no GPU-only dependency.

This fits the Cloud AI track because it optimizes an agent developer workflow for Arm64 cloud runners. The same benchmark runs on x86 and Arm64 through GitHub Actions, making the optimization measurable and repeatable.

## Track

Cloud AI

## Repository

https://github.com/dollarop/arm-memory-agent

## Demo / evidence

Use the repository README, `reports/benchmark.md`, and `docs/architecture.png` as the first evidence package. The GitHub Actions workflow runs the benchmark on `ubuntu-24.04` and `ubuntu-24.04-arm`.

## Built with

Python, Arm64, Cloud AI, GitHub Actions, Docker, Devpost, agent memory, prompt compression

## Testing instructions

Run:

```bash
python -m src.memory_agent_benchmark --dataset examples/learning_notes.jsonl
python -m src.generate_learning_dataset --output examples/synthetic_learning_notes.jsonl --count 180
python -m src.memory_agent_benchmark --dataset examples/synthetic_learning_notes.jsonl --queries examples/query_suite.json --markdown-report reports/benchmark.md
```

Expected output is a JSON report with selected cards, compression ratio, timing, and prompt hash.

Current benchmark result:

- 180 memory cards
- 4 benchmark queries
- Average compression ratio: 0.0275
- Total bytes saved vs naive prompts: 189596
- Average tag recall: 1.0
- Average runtime: 3.345 ms

## Architecture diagram

Upload `docs/architecture.png` or use `docs/architecture.md` for the Mermaid architecture diagram.
