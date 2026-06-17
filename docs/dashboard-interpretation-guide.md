# Dashboard Interpretation Guide

## Overview

The dashboard is designed to help interpret prompt-level AI visibility results.

It should answer:

- Where does the brand appear?
- Where is it missing?
- Which engines mention it?
- Which prompt categories perform best?
- Which competitors appear often?
- Are descriptions accurate?
- Are cited sources strong or weak?

---

## Core views

### 1. Brand mention rate

Measures how often the brand is mentioned across tested prompts.

Formula:

```txt
Number of prompts where brand is mentioned / Total prompts tested
```

Interpretation:

- High mention rate means the brand is visible across tested prompts.
- Low mention rate means the brand is missing or weakly associated with the topic.

---

### 2. Average visibility score

Average of the `score` field.

Interpretation:

- 80-100: strong visibility.
- 60-79: good but improvable visibility.
- 40-59: weak or inconsistent visibility.
- 0-39: low visibility.

---

### 3. Visibility by engine

Compare results across:

- ChatGPT.
- Perplexity.
- Gemini.
- Claude.
- Google AI Overviews.

This helps identify whether visibility is broad or concentrated in one system.

---

### 4. Visibility by prompt category

Compare performance across:

- Branded prompts.
- Category prompts.
- Local-intent prompts.
- Comparison prompts.
- Recommendation prompts.

A common pattern is strong branded visibility but weak category visibility.

---

### 5. Competitor presence

Track which competitors appear when the target brand is missing.

This helps identify:

- who is currently associated with the category;
- which sources competitors may be benefiting from;
- which content gaps should be closed.

---

### 6. Citation quality

Review cited sources when available.

Strong signals include:

- official website;
- LinkedIn profile;
- trusted directories;
- third-party reviews;
- case studies;
- media mentions;
- documentation.

Weak signals include:

- outdated pages;
- irrelevant directories;
- thin content;
- unverified profiles;
- pages with inconsistent descriptions.

---

## How to use the dashboard

Use the dashboard to prioritize action.

Example:

If the brand appears for branded prompts but not for category prompts, improve:

- service pages;
- category-specific content;
- comparison content;
- external mentions;
- case studies;
- LinkedIn positioning;
- `llms.txt` file;
- citation-ready pages.

If the brand appears but descriptions are inaccurate, improve:

- entity clarity;
- homepage positioning;
- about page;
- public profile consistency;
- structured content;
- source-of-truth pages.

If competitors appear often, analyze:

- their source pages;
- their reviews;
- their directory presence;
- their service pages;
- their authority signals.

---

## Important limitations

The dashboard does not prove permanent AI visibility.

It provides directional insight based on tested prompts, engines and dates.

Use it as a monitoring and decision-support tool.
