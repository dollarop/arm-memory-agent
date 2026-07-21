# Arm Create: AI Optimization Challenge - Submission Fields

## Project name

Arm Memory Agent

## Elevator pitch

A CPU-friendly memory layer that compresses long agent workspaces into small, auditable prompt packs for Arm64 cloud deployments.

## Track

Cloud AI

## About the project

Arm Memory Agent is a compact benchmark and reference workflow for making long-running AI agents more efficient on Arm64 cloud infrastructure.

Useful agents need memory: learner notes, uploaded source material, prior questions, feedback, and intermediate explanations. A naive implementation keeps appending that history into the prompt, which increases context size, latency, cost, and audit difficulty. Arm Memory Agent replaces that pattern with a small deterministic memory layer.

The project normalizes learning notes into structured memory cards, deduplicates repeated context, retrieves only the cards relevant to the current query, and emits a compact prompt pack with selected memory IDs, byte counts, runtime, and a SHA-256 audit hash.

The current benchmark uses 180 synthetic learning-memory cards and four representative queries. It achieved an average compression ratio of 0.0275, saved 189,596 bytes versus naive full-context prompts, reached 1.0 average tag recall, and ran in 3.345 ms average runtime.

This fits the Cloud AI track because it optimizes an agent developer workflow for Arm64 cloud runners. The project uses no GPU-only dependency, includes a repeatable benchmark, and validates the same workflow on both ubuntu-24.04 and ubuntu-24.04-arm with GitHub Actions.

## What it does

- Loads learning notes from JSONL.
- Converts notes into structured memory cards.
- Scores cards against a learner query.
- Builds a compact prompt pack from the most relevant cards.
- Compares optimized prompt size against a naive full-context baseline.
- Reports compression ratio, bytes saved, selected card IDs, runtime, tag recall, and prompt hash.
- Generates a Markdown benchmark report for judging.
- Runs the benchmark and tests on x86 and Arm64 GitHub Actions runners.

## Built with

Python, Arm64, Cloud AI, GitHub Actions, Docker, Devpost, agent memory, prompt compression

## Try it out / code repo

https://github.com/dollarop/arm-memory-agent

## GitHub Actions evidence

Latest successful run:

https://github.com/dollarop/arm-memory-agent/actions/runs/29870396731

Successful jobs:

- ubuntu-24.04
- ubuntu-24.04-arm

## Gallery image

Use:

devpost/arm-memory-agent-gallery.png

Repository URL:

https://github.com/dollarop/arm-memory-agent/blob/main/devpost/arm-memory-agent-gallery.png

## Video demo

Local/repo MP4 source:

devpost/arm-memory-agent-demo.mp4

Repository URL:

https://github.com/dollarop/arm-memory-agent/blob/main/devpost/arm-memory-agent-demo.mp4

Important: Devpost requires the demo video to be uploaded publicly to YouTube, Vimeo, or Youku before the final form can accept it. Upload this MP4 to YouTube, then paste the YouTube link in the Video demo field.

## Video title

Arm Memory Agent - Arm64 Cloud AI Optimization Demo

## Video description

Arm Memory Agent is a CPU-friendly memory layer for long-running AI agents on Arm64 cloud infrastructure. It compresses agent workspace context into small, auditable prompt packs and validates the benchmark on both ubuntu-24.04 and ubuntu-24.04-arm through GitHub Actions.

Repo: https://github.com/dollarop/arm-memory-agent

## Testing instructions

No credentials are required.

Run:

```bash
python -m src.memory_agent_benchmark --dataset examples/learning_notes.jsonl
python -m src.generate_learning_dataset --output examples/synthetic_learning_notes.jsonl --count 180
python -m src.memory_agent_benchmark --dataset examples/synthetic_learning_notes.jsonl --queries examples/query_suite.json --markdown-report reports/benchmark.md
python -m unittest discover -s tests
```

Expected result:

- JSON benchmark output in the terminal.
- Markdown report written to `reports/benchmark.md`.
- Unit tests pass.
- GitHub Actions validates the same benchmark on `ubuntu-24.04` and `ubuntu-24.04-arm`.

## If asked whether this is new or existing

Existing project with updates.

## If asked what changed during the submission period

Arm Memory Agent was created as a new Arm-focused extraction from prior LearnBridge work. During the challenge period, I added the standalone benchmark, synthetic dataset generator, query suite, Markdown report output, architecture diagram, Dockerfile, MIT license, README, GitHub Actions validation on x86 and Arm64 runners, and Devpost media assets.

## If asked about license

MIT License

## If asked what optimization is shown

The project optimizes agent context handling for CPU-first Arm64 cloud environments. Instead of sending a full growing workspace into the model prompt, it retrieves a compact memory subset and measures the resulting reduction. The benchmark shows a 0.0275 average compression ratio and 189,596 bytes saved versus naive prompts while preserving 1.0 average tag recall on the query suite.
