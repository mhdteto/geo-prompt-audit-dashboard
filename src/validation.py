"""Input validation and normalization for prompt-audit datasets."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = {
    "date",
    "engine",
    "prompt",
    "prompt_category",
    "brand_mentioned",
    "position",
    "sentiment",
    "answer_accuracy",
    "cited_sources",
    "competitors_mentioned",
}

ALLOWED_MENTION_VALUES = {"yes", "no", "partial"}
ALLOWED_SENTIMENT_VALUES = {"positive", "neutral", "negative", "unclear"}
ALLOWED_ACCURACY_VALUES = {
    "accurate",
    "mostly_accurate",
    "partially_accurate",
    "inaccurate",
    "not_applicable",
}


@dataclass(frozen=True)
class ValidationResult:
    data: pd.DataFrame
    errors: list[str]
    warnings: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _normalized_text(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip()


def validate_and_normalize(raw: pd.DataFrame) -> ValidationResult:
    """Validate a CSV-like dataframe and return a safe normalized copy."""
    data = raw.copy()
    data.columns = [str(column).strip().lower() for column in data.columns]
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED_COLUMNS - set(data.columns))
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing))
        return ValidationResult(data, errors, warnings)

    if data.empty:
        errors.append("The dataset contains no rows.")
        return ValidationResult(data, errors, warnings)

    for column in REQUIRED_COLUMNS - {"date", "position"}:
        data[column] = _normalized_text(data[column])

    data["engine"] = data["engine"].replace("", "Unknown")
    data["prompt_category"] = data["prompt_category"].str.lower()
    data["brand_mentioned"] = data["brand_mentioned"].str.lower()
    data["sentiment"] = data["sentiment"].str.lower()
    data["answer_accuracy"] = data["answer_accuracy"].str.lower()

    parsed_dates = pd.to_datetime(data["date"], errors="coerce")
    invalid_dates = int(parsed_dates.isna().sum())
    if invalid_dates:
        errors.append(f"{invalid_dates} row(s) contain an invalid date. Use YYYY-MM-DD.")
    data["date"] = parsed_dates

    numeric_position = pd.to_numeric(data["position"], errors="coerce")
    mentioned_mask = data["brand_mentioned"].isin({"yes", "partial"})
    missing_positions = int((mentioned_mask & numeric_position.isna()).sum())
    if missing_positions:
        warnings.append(
            f"{missing_positions} mentioned row(s) have no numeric position and are excluded from average position."
        )
    data["position_numeric"] = numeric_position

    for column, allowed in (
        ("brand_mentioned", ALLOWED_MENTION_VALUES),
        ("sentiment", ALLOWED_SENTIMENT_VALUES),
        ("answer_accuracy", ALLOWED_ACCURACY_VALUES),
    ):
        invalid = sorted(set(data[column]) - allowed)
        if invalid:
            errors.append(f"Invalid {column} value(s): " + ", ".join(invalid))

    if "brand" not in data.columns:
        data["brand"] = "Audited Brand"
        warnings.append("No brand column found; using 'Audited Brand'.")
    else:
        data["brand"] = _normalized_text(data["brand"]).replace("", "Audited Brand")

    if "recommended" not in data.columns:
        data["recommended"] = pd.NA
    else:
        recommended = _normalized_text(data["recommended"]).str.lower()
        mapping = {
            "yes": True,
            "true": True,
            "1": True,
            "no": False,
            "false": False,
            "0": False,
            "": pd.NA,
        }
        invalid = sorted(set(recommended) - set(mapping))
        if invalid:
            errors.append("Invalid recommended value(s): " + ", ".join(invalid))
        data["recommended"] = recommended.map(mapping).astype("boolean")

    if "score" in data.columns:
        data["score"] = pd.to_numeric(data["score"], errors="coerce")
        invalid_scores = int(((data["score"] < 0) | (data["score"] > 100)).sum())
        if invalid_scores:
            errors.append(f"{invalid_scores} score value(s) fall outside the 0-100 range.")

    duplicate_count = int(
        data.duplicated(subset=["date", "engine", "prompt", "brand"], keep=False).sum()
    )
    if duplicate_count:
        warnings.append(f"{duplicate_count} row(s) may be duplicates.")

    return ValidationResult(data, errors, warnings)

