# GEO Prompt Audit Scoring Model

## Core dimensions

| Dimension | Weight | Description |
|---|---:|---|
| Brand presence | 30 | Whether the brand appears in the answer. |
| Position | 15 | How early the brand appears when listed with alternatives. |
| Answer accuracy | 20 | Whether the answer describes the brand correctly. |
| Sentiment | 10 | Whether the mention is positive, neutral or negative. |
| Citation quality | 15 | Whether reliable sources are cited. |
| Competitor context | 10 | Whether the answer positions the brand clearly against alternatives. |

## Scoring rules

- Start from 0.
- Add points for each dimension using the table above.
- Penalize inaccurate or unsupported claims.
- Penalize answers that mention the brand but describe the wrong service, market or location.
- Track the same prompt wording over time to avoid noisy comparisons.

## Score bands

| Score | Interpretation |
|---:|---|
| 80-100 | Strong visibility |
| 60-79 | Improving visibility |
| 40-59 | Weak visibility |
| 0-39 | Low or no visibility |
