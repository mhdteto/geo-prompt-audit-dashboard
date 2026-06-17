# Data Schema

This document defines the recommended CSV structure for the GEO Prompt Audit Dashboard.

## Recommended columns

```csv
date,engine,prompt,prompt_category,brand_mentioned,position,sentiment,answer_accuracy,cited_sources,competitors_mentioned,score,notes
```

---

## Example row

```csv
2026-06-15,ChatGPT,"Best AI consultant in Morocco",category,yes,2,positive,mostly_accurate,"website,linkedin","competitor_a,competitor_b",78,"Brand mentioned second with mostly accurate description."
```

---

## Column definitions

| Column | Description | Example |
|---|---|---|
| date | Test date | 2026-06-15 |
| engine | AI answer engine | ChatGPT |
| prompt | Exact prompt tested | Best AI consultant in Morocco |
| prompt_category | Prompt category | category |
| brand_mentioned | Whether brand appeared | yes |
| position | Mention position | 2 |
| sentiment | Answer sentiment | positive |
| answer_accuracy | Description accuracy | mostly_accurate |
| cited_sources | Sources cited | website, linkedin |
| competitors_mentioned | Competitors mentioned | competitor_a |
| score | Visibility score | 78 |
| notes | Free-text notes | Brand mentioned second |

---

## Recommended values

### prompt_category

```txt
branded
category
local_intent
comparison
recommendation
```

### brand_mentioned

```txt
yes
no
partial
```

### sentiment

```txt
positive
neutral
negative
unclear
```

### answer_accuracy

```txt
accurate
mostly_accurate
partially_accurate
inaccurate
not_applicable
```

---

## Data quality rules

- Keep prompt wording consistent.
- Use one row per engine and prompt.
- Use the same scoring model across audits.
- Use ISO date format: `YYYY-MM-DD`.
- Avoid changing categories mid-analysis.
- Add notes when an answer is ambiguous.
