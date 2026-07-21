from __future__ import annotations

import argparse
import json
from pathlib import Path


TOPICS = [
    ("energy", "grid storage", "Compare batteries, transmission, nuclear firming, and demand response."),
    ("healthcare", "AI triage", "Track evidence, risk, privacy, population, and clinical supervision."),
    ("history", "author biography", "Connect dates, works, influences, historical context, and quotes."),
    ("math", "calculus formula", "Explain notation, assumptions, worked examples, and common mistakes."),
    ("climate", "adaptation plan", "Balance hazards, costs, local governance, and measurable resilience."),
    ("language", "bilingual practice", "Store vocabulary, pronunciation notes, examples, and teach-back checks."),
]


def build_note(index: int) -> dict[str, object]:
    topic, theme, instruction = TOPICS[index % len(TOPICS)]
    lesson = index // len(TOPICS) + 1
    return {
        "id": f"synthetic-{index + 1:03d}",
        "text": (
            f"Lesson {lesson} on {theme}: {instruction} "
            f"The learner preference is concise explanation, proof, practice, audio review, "
            f"and a final teach-back artifact. Keep source notes auditable and reusable."
        ),
        "tags": [topic, theme.replace(" ", "-"), "memory", "learning"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("examples/synthetic_learning_notes.jsonl"))
    parser.add_argument("--count", type=int, default=180)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for index in range(args.count):
            handle.write(json.dumps(build_note(index), ensure_ascii=True) + "\n")

    print(f"wrote {args.count} memory cards to {args.output}")


if __name__ == "__main__":
    main()
