"""Small dependency-free HTML report generator."""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape

import pandas as pd

from src.analytics import competitor_summary, engine_summary, headline_metrics
from src.scoring import score_label


def _table(data: pd.DataFrame) -> str:
    if data.empty:
        return "<p>No data available.</p>"
    return data.to_html(index=False, border=0, classes="data-table", escape=True)


def build_html_report(data: pd.DataFrame, title: str = "GEO Prompt Audit Report") -> str:
    metrics = headline_metrics(data)
    engines = engine_summary(data)
    competitors = competitor_summary(data).head(10)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    recommendation = metrics["recommendation_rate"]
    recommendation_text = "N/A" if recommendation is None else f"{recommendation}%"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 0; color: #152536; background: #f5f8fb; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px 64px; }}
    h1 {{ margin-bottom: 4px; }} .muted {{ color: #64748b; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 28px 0; }}
    .card {{ background: white; border: 1px solid #dbe5ef; border-radius: 12px; padding: 18px; }}
    .value {{ font-size: 28px; font-weight: 750; margin-top: 8px; }}
    .data-table {{ width: 100%; border-collapse: collapse; background: white; margin-bottom: 28px; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e7edf3; }}
    th {{ background: #eaf2f8; }}
    footer {{ color: #64748b; margin-top: 36px; font-size: 13px; }}
    @media (max-width: 760px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  </style>
</head>
<body><main>
  <h1>{escape(title)}</h1>
  <p class="muted">Generated {generated}. Directional measurement, not a ranking guarantee.</p>
  <section class="grid">
    <div class="card">Average score<div class="value">{metrics['average_score']}/100</div><small>{score_label(float(metrics['average_score']))}</small></div>
    <div class="card">Mention rate<div class="value">{metrics['mention_rate']}%</div></div>
    <div class="card">Citation rate<div class="value">{metrics['citation_rate']}%</div></div>
    <div class="card">Recommendation rate<div class="value">{recommendation_text}</div></div>
  </section>
  <h2>Performance by engine</h2>
  {_table(engines)}
  <h2>Most-mentioned competitors</h2>
  {_table(competitors)}
  <h2>Audit data</h2>
  {_table(data.drop(columns=['position_numeric'], errors='ignore'))}
  <footer>Generated with the open-source GEO Prompt Audit Dashboard by Mohammed Teto.</footer>
</main></body></html>"""

