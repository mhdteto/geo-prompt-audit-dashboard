# Data Schema

This document defines the recommended CSV structure for the GEO Prompt Audit Dashboard.

## Recommended columns

```csv
date,engine,prompt,prompt_category,brand,brand_mentioned,position,sentiment,answer_accuracy,cited_sources,competitors_mentioned,recommended,score,notes
```

The application keeps backward compatibility with v1.0 datasets. The `brand`,
`recommended`, `score` and `notes` columns are optional. All other columns are
required.

---

## Example row

```csv
2026-07-18,ChatGPT,"Best AI consultant in Morocco",category,Your Brand,yes,2,positive,mostly_accurate,"official website,third-party article","Competitor A,Competitor B",yes,85,"Brand mentioned second with mostly accurate description."
```

---

## Column definitions

| Column | Description | Example |
|---|---|---|
| date | Test date | 2026-06-15 |
| engine | AI answer engine | ChatGPT |
| prompt | Exact prompt tested | Best AI consultant in Morocco |
| prompt_category | Prompt category | category |
| brand | Brand being audited (optional) | Your Brand |
| brand_mentioned | Whether brand appeared | yes |
| position | Mention position | 2 |
| sentiment | Answer sentiment | positive |
| answer_accuracy | Description accuracy | mostly_accurate |
| cited_sources | Sources cited | website, linkedin |
| competitors_mentioned | Competitors mentioned | competitor_a |
| recommended | Whether the answer recommends the brand (optional) | yes |
| score | Visibility score; calculated when empty (optional) | 85 |
| notes | Free-text notes (optional) | Brand mentioned second |

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

### recommended

```txt
yes
no
```

Leave this field empty when recommendation status cannot be judged. The
dashboard will display recommendation rate as `N/A` if the selected data has no
observations for this field.

---

## Data quality rules

- Keep prompt wording consistent.
- Use one row per engine and prompt.
- Use the same scoring model across audits.
- Use ISO date format: `YYYY-MM-DD`.
- Avoid changing categories mid-analysis.
- Add notes when an answer is ambiguous.
- Use `none` consistently when no source or competitor is present.
- Do not infer recommendation status from a simple brand mention.
- Keep the original answer or a verifiable evidence reference outside the CSV
  when the audit needs to be reviewed.
