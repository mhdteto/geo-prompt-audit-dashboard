import unittest

import pandas as pd

from src.scoring import calculate_score, ensure_scores, score_label


class ScoringTests(unittest.TestCase):
    def test_strong_result_scores_one_hundred(self):
        row = pd.Series(
            {
                "brand_mentioned": "yes",
                "position_numeric": 1,
                "answer_accuracy": "accurate",
                "sentiment": "positive",
                "cited_sources": "official website, third-party article",
                "competitors_mentioned": "Competitor A",
                "recommended": True,
            }
        )
        self.assertEqual(calculate_score(row), 100)

    def test_missing_brand_with_competitors_scores_zero(self):
        row = pd.Series(
            {
                "brand_mentioned": "no",
                "position_numeric": None,
                "answer_accuracy": "not_applicable",
                "sentiment": "negative",
                "cited_sources": "none",
                "competitors_mentioned": "Competitor A",
                "recommended": False,
            }
        )
        self.assertEqual(calculate_score(row), 0)

    def test_existing_score_is_preserved_and_missing_score_is_filled(self):
        data = pd.DataFrame(
            [
                {
                    "brand_mentioned": "yes",
                    "position_numeric": 1,
                    "answer_accuracy": "accurate",
                    "sentiment": "positive",
                    "cited_sources": "official website",
                    "competitors_mentioned": "none",
                    "recommended": True,
                    "score": 77,
                },
                {
                    "brand_mentioned": "no",
                    "position_numeric": None,
                    "answer_accuracy": "not_applicable",
                    "sentiment": "neutral",
                    "cited_sources": "none",
                    "competitors_mentioned": "Competitor A",
                    "recommended": False,
                    "score": None,
                },
            ]
        )
        result = ensure_scores(data)
        self.assertEqual(result.loc[0, "score"], 77)
        self.assertEqual(result.loc[1, "score"], 6)

    def test_score_labels(self):
        self.assertEqual(score_label(80), "Strong")
        self.assertEqual(score_label(60), "Good, improvable")
        self.assertEqual(score_label(40), "Weak or inconsistent")
        self.assertEqual(score_label(39.9), "Low visibility")


if __name__ == "__main__":
    unittest.main()

