# Scoring Methodology

## Overview

The GEO Prompt Audit Dashboard uses a simple 100-point scoring model.

The goal is not to create a perfect scientific measurement.

The goal is to create a consistent way to compare prompt-level visibility over time.

---

## Recommended scoring model

| Dimension | Max score |
|---|---:|
| Brand mentioned | 25 |
| Mention position | 15 |
| Answer accuracy | 20 |
| Sentiment | 10 |
| Source quality | 15 |
| Competitive context | 15 |
| **Total** | **100** |

---

## 1. Brand mentioned - 25 points

| Result | Score |
|---|---:|
| Brand clearly mentioned | 25 |
| Brand partially mentioned | 10 |
| Brand not mentioned | 0 |

---

## 2. Mention position - 15 points

| Result | Score |
|---|---:|
| Mentioned first | 15 |
| Mentioned second or third | 10 |
| Mentioned after third position | 5 |
| Not mentioned | 0 |

---

## 3. Answer accuracy - 20 points

| Result | Score |
|---|---:|
| Accurate | 20 |
| Mostly accurate | 15 |
| Partially accurate | 8 |
| Inaccurate | 0 |
| Not applicable | 0 |

---

## 4. Sentiment - 10 points

| Result | Score |
|---|---:|
| Positive | 10 |
| Neutral | 6 |
| Unclear | 3 |
| Negative | 0 |

---

## 5. Source quality - 15 points

| Result | Score |
|---|---:|
| Strong official and third-party sources | 15 |
| Official source only | 10 |
| Weak or generic sources | 5 |
| No sources | 0 |

---

## 6. Competitive context - 15 points

| Result | Score |
|---|---:|
| Brand recommended ahead of competitors | 15 |
| Brand mentioned alongside competitors | 10 |
| Competitors mentioned but brand missing | 0 |
| No relevant competitive context | 5 |

---

## Score interpretation

| Score range | Interpretation |
|---|---|
| 80-100 | Strong AI visibility |
| 60-79 | Good but improvable visibility |
| 40-59 | Weak or inconsistent visibility |
| 0-39 | Low AI visibility |

---

## Important note

Scores should be interpreted directionally.

AI answers can vary over time and across systems.

Use the scoring model to identify patterns, compare prompt categories and prioritize improvements.

## Application behavior

The interactive application preserves a valid score supplied in the CSV. When
the `score` field is absent or empty, it calculates the score from the fields
above.

Source quality is estimated conservatively from the labels recorded in
`cited_sources`:

- Official plus third-party evidence: 15 points.
- Official source only: 10 points.
- Other recorded source: 5 points.
- No source: 0 points.

Competitive context uses the optional `recommended` field where available. A
brand mentioned and explicitly recommended can receive 15 points; a brand
mentioned alongside competitors receives 10; competitors present while the
brand is missing receives 0; and no relevant competitive context receives 5.

These heuristics are intentionally transparent. Teams should document and keep
their own scoring policy stable across audit periods.
