from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import time
from dataclasses import dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


@dataclass(frozen=True)
class MemoryCard:
    id: str
    text: str
    tags: tuple[str, ...]


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def load_cards(path: Path) -> list[MemoryCard]:
    cards: list[MemoryCard] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        cards.append(
            MemoryCard(
                id=str(row["id"]),
                text=str(row["text"]).strip(),
                tags=tuple(str(tag).lower() for tag in row.get("tags", [])),
            )
        )
    return cards


def dedupe_cards(cards: list[MemoryCard]) -> list[MemoryCard]:
    seen: set[str] = set()
    unique: list[MemoryCard] = []
    for card in cards:
        signature = hashlib.sha256(card.text.lower().encode("utf-8")).hexdigest()
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(card)
    return unique


def retrieve(cards: list[MemoryCard], query: str, limit: int) -> list[MemoryCard]:
    query_tokens = tokenize(query)
    scored: list[tuple[float, MemoryCard]] = []
    for card in cards:
        card_tokens = tokenize(card.text) | set(card.tags)
        overlap = len(query_tokens & card_tokens)
        score = overlap / max(1, len(query_tokens | card_tokens))
        scored.append((score, card))
    scored.sort(key=lambda item: (item[0], item[1].id), reverse=True)
    return [card for score, card in scored[:limit] if score > 0]


def build_prompt(query: str, selected: list[MemoryCard]) -> str:
    memory = "\n".join(f"- [{card.id}] {card.text}" for card in selected)
    return (
        "You are a learning agent. Answer using only the memory cards that matter.\n\n"
        f"Question: {query}\n\n"
        f"Relevant memory:\n{memory}\n\n"
        "Return a concise teaching plan with proof, practice, and a teach-back step."
    )


def build_naive_prompt(query: str, cards: list[MemoryCard]) -> str:
    memory = "\n".join(f"- [{card.id}] {card.text}" for card in cards)
    return (
        "You are a learning agent. Answer using the full accumulated workspace.\n\n"
        f"Question: {query}\n\n"
        f"Full memory:\n{memory}\n\n"
        "Return a concise teaching plan with proof, practice, and a teach-back step."
    )


def score_recall(selected: list[MemoryCard], expected_tags: set[str]) -> float:
    if not expected_tags:
        return 0.0
    selected_tags = {tag for card in selected for tag in card.tags}
    return len(selected_tags & expected_tags) / len(expected_tags)


def run_query(cards: list[MemoryCard], query: str, limit: int, expected_tags: set[str] | None = None) -> dict[str, object]:
    start = time.perf_counter()
    raw_context = "\n".join(card.text for card in cards)
    selected = retrieve(cards, query, limit)
    naive_prompt = build_naive_prompt(query, cards)
    prompt = build_prompt(query, selected)
    elapsed_ms = (time.perf_counter() - start) * 1000

    raw_bytes = len(raw_context.encode("utf-8"))
    naive_bytes = len(naive_prompt.encode("utf-8"))
    prompt_bytes = len(prompt.encode("utf-8"))
    return {
        "cards_loaded": len(cards),
        "cards_selected": [card.id for card in selected],
        "raw_context_bytes": raw_bytes,
        "naive_prompt_bytes": naive_bytes,
        "optimized_prompt_bytes": prompt_bytes,
        "compression_ratio": round(prompt_bytes / max(naive_bytes, 1), 4),
        "bytes_saved_vs_naive": naive_bytes - prompt_bytes,
        "elapsed_ms": round(elapsed_ms, 3),
        "tag_recall": round(score_recall(selected, expected_tags or set()), 4),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


def run(dataset: Path, query: str, limit: int) -> dict[str, object]:
    cards = dedupe_cards(load_cards(dataset))
    return run_query(cards, query, limit)


def load_queries(path: Path) -> list[dict[str, object]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("queries file must be a JSON list")
    return rows


def run_suite(dataset: Path, queries: Path, limit: int) -> dict[str, object]:
    cards = dedupe_cards(load_cards(dataset))
    results: list[dict[str, object]] = []
    for row in load_queries(queries):
        query = str(row["query"])
        expected_tags = {str(tag).lower() for tag in row.get("expected_tags", [])}
        results.append(run_query(cards, query, limit, expected_tags))

    ratios = [float(item["compression_ratio"]) for item in results]
    latencies = [float(item["elapsed_ms"]) for item in results]
    recalls = [float(item["tag_recall"]) for item in results]
    return {
        "dataset": str(dataset),
        "queries": str(queries),
        "cards_loaded": len(cards),
        "query_count": len(results),
        "average_compression_ratio": round(statistics.mean(ratios), 4),
        "median_compression_ratio": round(statistics.median(ratios), 4),
        "average_elapsed_ms": round(statistics.mean(latencies), 3),
        "average_tag_recall": round(statistics.mean(recalls), 4),
        "total_bytes_saved_vs_naive": sum(int(item["bytes_saved_vs_naive"]) for item in results),
        "results": results,
    }


def write_markdown_report(report: dict[str, object], output: Path) -> None:
    lines = [
        "# Arm Memory Agent Benchmark Report",
        "",
        f"- Dataset: `{report['dataset']}`",
        f"- Query suite: `{report['queries']}`",
        f"- Memory cards loaded: `{report['cards_loaded']}`",
        f"- Queries tested: `{report['query_count']}`",
        f"- Average compression ratio: `{report['average_compression_ratio']}`",
        f"- Median compression ratio: `{report['median_compression_ratio']}`",
        f"- Total bytes saved vs naive prompts: `{report['total_bytes_saved_vs_naive']}`",
        f"- Average tag recall: `{report['average_tag_recall']}`",
        f"- Average runtime: `{report['average_elapsed_ms']} ms`",
        "",
        "## Query Results",
        "",
    ]
    for index, item in enumerate(report["results"], start=1):
        lines.extend(
            [
                f"### Query {index}",
                "",
                f"- Selected cards: `{', '.join(item['cards_selected'])}`",
                f"- Naive prompt bytes: `{item['naive_prompt_bytes']}`",
                f"- Optimized prompt bytes: `{item['optimized_prompt_bytes']}`",
                f"- Compression ratio: `{item['compression_ratio']}`",
                f"- Tag recall: `{item['tag_recall']}`",
                f"- Prompt hash: `{item['prompt_sha256']}`",
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument(
        "--query",
        default="Build a bilingual learning path for energy transition with memory and audio.",
    )
    parser.add_argument("--queries", type=Path)
    parser.add_argument("--limit", type=int, default=4)
    parser.add_argument("--markdown-report", type=Path)
    args = parser.parse_args()

    if args.queries:
        report = run_suite(args.dataset, args.queries, args.limit)
        if args.markdown_report:
            write_markdown_report(report, args.markdown_report)
    else:
        report = run(args.dataset, args.query, args.limit)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
