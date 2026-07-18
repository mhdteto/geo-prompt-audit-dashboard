"""Transparent 100-point scoring model for prompt results."""

from __future__ import annotations

import pandas as pd


MENTION_POINTS = {"yes": 25, "partial": 10, "no": 0}
ACCURACY_POINTS = {
    "accurate": 20,
    "mostly_accurate": 15,
    "partially_accurate": 8,
    "inaccurate": 0,
    "not_applicable": 0,
}
SENTIMENT_POINTS = {"positive": 10, "neutral": 6, "unclear": 3, "negative": 0}
EMPTY_MARKERS = {"", "none", "n/a", "not_applicable", "not mentioned", "not_mentioned"}


def position_points(value: object) -> int:
    try:
        position = int(float(value))
    except (TypeError, ValueError):
        return 0
    if position == 1:
        return 15
    if 2 <= position <= 3:
        return 10
    if position > 3:
        return 5
    return 0


def source_points(value: object) -> int:
    text = str(value or "").strip().lower()
    if text in EMPTY_MARKERS:
        return 0
    sources = [item.strip() for item in text.replace(";", ",").split(",") if item.strip()]
    official = any(token in text for token in ("website", "official", "linkedin"))
    third_party = any(
        token in text
        for token in ("article", "directory", "media", "press", "review", "third-party")
    )
    if official and third_party:
        return 15
    if official:
        return 10
    return 5 if sources else 0


def competitive_points(mention: object, competitors: object, recommended: object = None) -> int:
    mention_value = str(mention).strip().lower()
    competitor_text = str(competitors or "").strip().lower()
    competitors_present = competitor_text not in EMPTY_MARKERS

    if recommended is True and mention_value == "yes":
        return 15
    if mention_value in {"yes", "partial"} and competitors_present:
        return 10
    if mention_value == "no" and competitors_present:
        return 0
    return 5


def calculate_score(row: pd.Series) -> int:
    recommended = row.get("recommended")
    if pd.isna(recommended):
        recommended = None
    score = (
        MENTION_POINTS.get(str(row.get("brand_mentioned", "")).lower(), 0)
        + position_points(row.get("position_numeric", row.get("position")))
        + ACCURACY_POINTS.get(str(row.get("answer_accuracy", "")).lower(), 0)
        + SENTIMENT_POINTS.get(str(row.get("sentiment", "")).lower(), 0)
        + source_points(row.get("cited_sources"))
        + competitive_points(
            row.get("brand_mentioned"), row.get("competitors_mentioned"), recommended
        )
    )
    return min(100, max(0, int(score)))


def ensure_scores(data: pd.DataFrame) -> pd.DataFrame:
    """Fill missing scores with calculated values while preserving supplied scores."""
    result = data.copy()
    calculated = result.apply(calculate_score, axis=1)
    if "score" not in result.columns:
        result["score"] = calculated
    else:
        result["score"] = result["score"].fillna(calculated).round(0)
    return result


def score_label(score: float) -> str:
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Good, improvable"
    if score >= 40:
        return "Weak or inconsistent"
    return "Low visibility"

