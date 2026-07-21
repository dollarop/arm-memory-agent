import unittest
from pathlib import Path

from src.memory_agent_benchmark import load_cards, retrieve, run_suite


class MemoryAgentBenchmarkTest(unittest.TestCase):
    def test_retrieve_prefers_relevant_tags(self) -> None:
        cards = load_cards(Path("examples/learning_notes.jsonl"))
        selected = retrieve(cards, "energy storage batteries transmission", 2)
        self.assertTrue(selected)
        self.assertTrue(any("energy" in card.tags for card in selected))

    def test_suite_reports_compression(self) -> None:
        report = run_suite(Path("examples/synthetic_learning_notes.jsonl"), Path("examples/query_suite.json"), 4)
        self.assertEqual(report["query_count"], 4)
        self.assertLess(report["average_compression_ratio"], 1)
        self.assertGreater(report["total_bytes_saved_vs_naive"], 0)
        self.assertEqual(report["average_tag_recall"], 1.0)


if __name__ == "__main__":
    unittest.main()
