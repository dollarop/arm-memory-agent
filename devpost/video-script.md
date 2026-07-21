# Arm Memory Agent Demo Script

Arm Memory Agent is a CPU-friendly memory layer for long-running AI agents on Arm64 cloud infrastructure.

Instead of appending every prior note and source into context, it converts learner notes into structured memory cards, removes repeated facts, retrieves only relevant evidence, and emits a compact prompt pack.

The benchmark is reproducible: it generates 180 synthetic learning memory cards and runs four representative queries.

The current result shows a 0.0275 average compression ratio, 189,596 bytes saved against naive prompts, 1.0 average tag recall, and millisecond-level runtime.

Every prompt pack includes selected memory IDs, byte counts, timing, and a SHA-256 hash so the output is small and auditable.

The GitHub Actions workflow validates the same benchmark on ubuntu-24.04 and ubuntu-24.04-arm, making the Cloud AI optimization evidence repeatable.
