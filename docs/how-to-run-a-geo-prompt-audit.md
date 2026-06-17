# How to Run a GEO Prompt Audit

## Overview

A GEO prompt audit evaluates how a brand appears across AI answer engines when users ask relevant questions.

GEO stands for Generative Engine Optimization.

A prompt audit helps answer questions such as:

- Is the brand mentioned?
- Is the brand described accurately?
- Is the brand recommended for relevant queries?
- Are competitors mentioned instead?
- Are sources cited?
- Is the sentiment positive, neutral or negative?
- Does performance change over time?

The goal is not to prove permanent AI visibility.

The goal is to create a structured way to measure and monitor AI answer presence.

---

## Step 1 - Define the brand

Collect the core brand information:

- Official brand name.
- Alternative names.
- Website.
- Location.
- Main services.
- Target audience.
- Competitors.
- Public profiles.
- Source-of-truth pages.

This helps make prompt testing more consistent.

---

## Step 2 - Define prompt categories

Use several types of prompts.

### Branded prompts

These test whether the AI system understands the brand directly.

Examples:

```txt
Who is [brand name]?
What does [brand name] do?
Is [brand name] reliable?
What services does [brand name] offer?
```

### Category prompts

These test whether the brand appears for broader service categories.

Examples:

```txt
Best AI consultant in Morocco
AI automation consultant in Casablanca
GEO consultant for businesses
LLM visibility expert for SMBs
```

### Local-intent prompts

These test geographic relevance.

Examples:

```txt
AI consultant in Casablanca
Automation consultant in Morocco
SEO AI consultant Morocco
ChatGPT visibility consultant Morocco
```

### Comparison prompts

These test competitive visibility.

Examples:

```txt
[brand name] vs competitors
Best alternatives to [brand name]
Top consultants for AI visibility in Morocco
```

### Recommendation prompts

These test whether the brand appears when users ask for help or vendor suggestions.

Examples:

```txt
Who should I hire for an AI visibility audit?
Which consultant can help a Moroccan SMB adopt AI?
Who can help improve visibility in ChatGPT and Perplexity?
```

---

## Step 3 - Choose AI systems to test

Run prompts across multiple systems:

- ChatGPT.
- Perplexity.
- Gemini.
- Claude.
- Google AI Overviews, when available.

Use the same prompt wording when possible.

Record the test date.

---

## Step 4 - Record the answers

For each prompt and AI system, record:

- Date.
- Engine.
- Prompt.
- Prompt category.
- Brand mentioned: yes/no.
- Mention position.
- Sentiment.
- Answer accuracy.
- Cited sources.
- Competitors mentioned.
- Score.
- Notes.

Use a structured CSV or spreadsheet.

---

## Step 5 - Score the result

Suggested scoring dimensions:

| Dimension | Max score |
|---|---:|
| Brand mentioned | 25 |
| Mention position | 15 |
| Answer accuracy | 20 |
| Sentiment | 10 |
| Source quality | 15 |
| Competitive context | 15 |
| **Total** | **100** |

The scoring model should stay consistent across audits.

---

## Step 6 - Analyze the gaps

Look for patterns:

- The brand appears only in branded prompts.
- The brand is missing from category prompts.
- Competitors appear more frequently.
- The AI system describes the brand incorrectly.
- Sources are weak or missing.
- The brand has low citation readiness.
- Results vary strongly by engine.

These gaps should guide content, entity and reputation improvements.

---

## Step 7 - Repeat over time

Run the same prompt set regularly.

Recommended frequency:

- Weekly during active visibility work.
- Monthly for maintenance.
- Before and after major website updates.
- After publishing case studies or third-party mentions.

Track changes in:

- Mention rate.
- Average score.
- Prompt category performance.
- Competitor presence.
- Citation quality.
- Answer accuracy.

---

## Important limitations

AI answer results are not perfectly stable.

They can vary based on:

- Model version.
- Retrieval behavior.
- User location.
- Prompt wording.
- Date of testing.
- Available sources.
- Personalization.
- Conversation context.

For this reason, prompt auditing should be treated as directional measurement, not absolute proof.
