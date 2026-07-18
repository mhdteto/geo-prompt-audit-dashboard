import unittest

import pandas as pd

from src.analytics import competitor_summary, headline_metrics
from src.scoring import ensure_scores
from src.validation import validate_and_normalize


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "date": "2026-07-18",
                "engine": "ChatGPT",
                "prompt": "Best AI consultant in Morocco",
                "prompt_category": "category",
                "brand_mentioned": "yes",
                "position": "2",
                "sentiment": "positive",
                "answer_accuracy": "accurate",
                "cited_sources": "official website",
                "competitors_mentioned": "Competitor A; Competitor B",
                "recommended": "yes",
            },
            {
                "date": "2026-07-18",
                "engine": "Gemini",
                "prompt": "GEO consultant Morocco",
                "prompt_category": "recommendation",
                "brand_mentioned": "no",
                "position": "not_mentioned",
                "sentiment": "neutral",
                "answer_accuracy": "not_applicable",
                "cited_sources": "none",
                "competitors_mentioned": "Competitor B",
                "recommended": "no",
            },
        ]
    )


class ValidationTests(unittest.TestCase):
    def test_valid_data_is_normalized(self):
        result = validate_and_normalize(valid_frame())
        self.assertTrue(result.is_valid)
        self.assertEqual(result.data.loc[0, "position_numeric"], 2)
        self.assertEqual(result.data.loc[0, "brand"], "Audited Brand")
        self.assertTrue(result.data.loc[0, "recommended"])

    def test_missing_columns_are_reported(self):
        result = validate_and_normalize(pd.DataFrame({"date": ["2026-07-18"]}))
        self.assertFalse(result.is_valid)
        self.assertIn("Missing required columns", result.errors[0])

    def test_invalid_values_are_reported(self):
        data = valid_frame()
        data.loc[0, "sentiment"] = "excellent"
        result = validate_and_normalize(data)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Invalid sentiment" in error for error in result.errors))

    def test_headline_and_competitor_metrics(self):
        validated = validate_and_normalize(valid_frame()).data
        scored = ensure_scores(validated)
        metrics = headline_metrics(scored)
        self.assertEqual(metrics["tests"], 2)
        self.assertEqual(metrics["mention_rate"], 50.0)
        self.assertEqual(metrics["citation_rate"], 50.0)
        self.assertEqual(metrics["recommendation_rate"], 50.0)
        competitors = competitor_summary(scored)
        self.assertEqual(competitors.iloc[0]["Competitor"], "Competitor B")
        self.assertEqual(competitors.iloc[0]["Mentions"], 2)


if __name__ == "__main__":
    unittest.main()

