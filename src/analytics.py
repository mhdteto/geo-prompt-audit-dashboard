"""Reusable metric calculations for the interactive dashboard."""

from __future__ import annotations

from collections import Counter

import pandas as pd


EMPTY_MARKERS = {"", "none", "n/a", "not_applicable", "not mentioned", "not_mentioned"}
ACCURACY_PERCENT = {
    "accurate": 100,
    "mostly_accurate": 75,
    "partially_accurate": 40,
    "inaccurate": 0,
}


def _percent(mask: pd.Series) -> float:
    return round(float(mask.mean() * 100), 1) if len(mask) else 0.0


def citation_mask(data: pd.DataFrame) -> pd.Series:
    values = data["cited_sources"].fillna("").astype(str).str.strip().str.lower()
    return ~values.isin(EMPTY_MARKERS)


def headline_metrics(data: pd.DataFrame) -> dict[str, float | int | None]:
    mentioned = data["brand_mentioned"].isin({"yes", "partial"})
    strict_mention = data["brand_mentioned"].eq("yes")
    numeric_positions = data.loc[mentioned, "position_numeric"].dropna()
    accuracy = data["answer_accuracy"].map(ACCURACY_PERCENT).dropna()
    known_recommendations = data["recommended"].dropna()

    return {
        "tests": int(len(data)),
        "mention_rate": _percent(mentioned),
        "strict_mention_rate": _percent(strict_mention),
        "citation_rate": _percent(citation_mask(data)),
        "recommendation_rate": (
            round(float(known_recommendations.astype(bool).mean() * 100), 1)
            if len(known_recommendations)
            else None
        ),
        "average_position": (
            round(float(numeric_positions.mean()), 2) if len(numeric_positions) else None
        ),
        "accuracy_rate": round(float(accuracy.mean()), 1) if len(accuracy) else None,
        "average_score": round(float(data["score"].mean()), 1),
    }


def engine_summary(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for engine, group in data.groupby("engine", observed=True):
        metrics = headline_metrics(group)
        rows.append(
            {
                "Engine": engine,
                "Tests": metrics["tests"],
                "Mention rate (%)": metrics["mention_rate"],
                "Citation rate (%)": metrics["citation_rate"],
                "Average score": metrics["average_score"],
                "Average position": metrics["average_position"],
            }
        )
    return pd.DataFrame(rows).sort_values("Average score", ascending=False).reset_index(drop=True)


def category_summary(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for category, group in data.groupby("prompt_category", observed=True):
        metrics = headline_metrics(group)
        rows.append(
            {
                "Prompt category": category,
                "Tests": metrics["tests"],
                "Mention rate (%)": metrics["mention_rate"],
                "Citation rate (%)": metrics["citation_rate"],
                "Average score": metrics["average_score"],
            }
        )
    return pd.DataFrame(rows).sort_values("Average score", ascending=False).reset_index(drop=True)


def trend_summary(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for date, group in data.groupby("date", observed=True):
        metrics = headline_metrics(group)
        rows.append(
            {
                "Date": date,
                "Mention rate (%)": metrics["mention_rate"],
                "Citation rate (%)": metrics["citation_rate"],
                "Average score": metrics["average_score"],
            }
        )
    return pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)


def competitor_summary(data: pd.DataFrame) -> pd.DataFrame:
    counter: Counter[str] = Counter()
    for raw_value in data["competitors_mentioned"].fillna("").astype(str):
        normalized = raw_value.replace(";", ",")
        for value in normalized.split(","):
            competitor = value.strip()
            if competitor.lower() not in EMPTY_MARKERS:
                counter[competitor] += 1
    if not counter:
        return pd.DataFrame(columns=["Competitor", "Mentions"])
    return pd.DataFrame(
        [{"Competitor": name, "Mentions": count} for name, count in counter.most_common()]
    )

