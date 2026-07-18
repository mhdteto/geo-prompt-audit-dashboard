# Metrics Dictionary

## Interactive dashboard metrics

| Metric | Definition |
|---|---|
| Visibility score | Average of the supplied or calculated 0-100 row scores. |
| Mention rate | Percentage of rows where `brand_mentioned` is `yes` or `partial`. |
| Strict mention rate | Percentage of rows where `brand_mentioned` is `yes`. |
| Citation rate | Percentage of rows with at least one recorded cited source. |
| Recommendation rate | Percentage of observed `recommended` values equal to `yes`; `N/A` when no observations exist. |
| Average position | Mean numeric mention position among mentioned rows with a valid position. |
| Accuracy rate | Directional average using accurate=100, mostly accurate=75, partially accurate=40 and inaccurate=0. |
| Competitor mentions | Count of each comma- or semicolon-separated competitor occurrence. |

This document explains the core metrics used in the GEO Prompt Audit Dashboard.

---

## date

The date when the prompt was tested.

Example:

```txt
2026-06-15
```

---

## engine

The AI answer engine used for the test.

Examples:

```txt
ChatGPT
Perplexity
Gemini
Claude
Google AI Overviews
```

---

## prompt

The exact prompt tested.

Example:

```txt
Best AI consultant in Morocco
```

Prompt wording matters. Keep it consistent across repeated audits.

---

## prompt_category

The type of prompt.

Recommended categories:

```txt
branded
category
local_intent
comparison
recommendation
```

---

## brand_mentioned

Whether the target brand appeared in the answer.

Accepted values:

```txt
yes
no
partial
```

Use `partial` when the answer mentions a related name, founder, product or unclear reference.

---

## position

The position of the brand mention in the answer.

Examples:

```txt
1
2
3
not_mentioned
```

If the brand is not mentioned, use:

```txt
not_mentioned
```

---

## sentiment

The tone of the answer toward the brand.

Recommended values:

```txt
positive
neutral
negative
unclear
```

---

## answer_accuracy

How accurate the AI-generated description is.

Recommended values:

```txt
accurate
mostly_accurate
partially_accurate
inaccurate
not_applicable
```

---

## cited_sources

Sources cited by the AI answer engine, if available.

Examples:

```txt
website, linkedin, directory
```

If no sources are cited:

```txt
none
```

---

## competitors_mentioned

Competitors or alternative providers mentioned in the answer.

Examples:

```txt
competitor_a, competitor_b
```

If no competitors are mentioned:

```txt
none
```

---

## score

A numeric visibility score from 0 to 100.

The score should be calculated using the same scoring method across all audits.

---

## notes

Free-text field for context.

Examples:

```txt
Brand mentioned but description is outdated.
Competitor appears first.
No sources cited.
Answer confused brand with another entity.
```
