# GEO Prompt Audit Dashboard

An interactive, open-source dashboard for measuring how a brand appears across ChatGPT, Perplexity, Gemini, Claude and Google AI Overviews.

[![Python tests](https://github.com/mhdteto/geo-prompt-audit-dashboard/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mhdteto/geo-prompt-audit-dashboard/actions/workflows/python-tests.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-0b7285.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)

**[Open the live application](https://geo-prompt-audit-dashboard-gl8ahrmbneyhcbpleasac4.streamlit.app/)**

> Upload a prompt-audit CSV, compare AI engines, identify visibility gaps and export a client-ready HTML report.

The application also includes a **Simple generation** mode: a visitor writes a request and receives a direct AI-generated answer in the same language.

## What the application measures

- Visibility score on a transparent 100-point model
- Brand mention and citation rates
- Recommendation rate when supplied in the dataset
- Average mention position
- Answer-accuracy indicator
- Performance by AI engine and prompt category
- Visibility trend over time
- Most-mentioned competitors

The included sample is a **fictional Moroccan demo dataset**. It demonstrates the interface and must not be interpreted as observed AI-engine results.

## Run locally

```bash
git clone https://github.com/mhdteto/geo-prompt-audit-dashboard.git
cd geo-prompt-audit-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Replace the placeholder with your real provider API key.
streamlit run app.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Use your audit data

1. Download [`data/data-template.csv`](data/data-template.csv).
2. Add one row for each prompt, engine and test date.
3. Record the answer exactly and consistently.
4. Upload the CSV from the application's sidebar.
5. Filter the results and export a CSV or standalone HTML report.

The application validates required columns, dates, categorical values, score ranges and likely duplicate rows before calculating any metric.

## Use simple generation mode

1. Open the application and select **Génération simple**.
2. Enter a request in natural language.
3. Select **Générer le résultat**.
4. Read the answer or download it as Markdown.

The server supports Google Gemini through the Interactions API and OpenAI through the Responses API. Configure `AI_PROVIDER`, `AI_MODEL` and the matching `GEMINI_API_KEY` or `OPENAI_API_KEY` in an environment variable or Streamlit secrets. The key is never displayed in the interface and must never be committed to GitHub.

For backward compatibility, a model named `gemini-*` in `OPENAI_MODEL` is routed automatically to Gemini and can reuse the existing server-side key setting. New deployments should use the neutral settings shown in `.streamlit/secrets.toml.example`.

## CSV schema

Required columns:

```text
date,engine,prompt,prompt_category,brand_mentioned,position,sentiment,
answer_accuracy,cited_sources,competitors_mentioned
```

Optional columns:

```text
brand,recommended,score,notes
```

- If `brand` is absent, the application uses `Audited Brand`.
- If `score` is empty, the documented scoring model calculates it.
- If `recommended` is absent, recommendation rate displays as `N/A` instead of inventing a value.
- Existing v1.0 datasets remain supported.

See the complete [data schema](docs/data-schema.md) and [scoring methodology](docs/scoring-methodology.md).

## Project structure

```text
.
├── app.py                       # Streamlit interface
├── src/
│   ├── analytics.py             # Metrics and aggregations
│   ├── report.py                # Standalone HTML export
│   ├── scoring.py               # Transparent 100-point model
│   └── validation.py            # CSV validation and normalization
├── tests/                       # Unit tests
├── data/
│   ├── sample-results.csv       # Fictional multi-date demo
│   └── data-template.csv        # Reusable audit template
├── docs/                        # Methodology and operating guides
└── .github/workflows/           # Python 3.10/3.12 CI
```

## Run the tests

The tests use Python's standard library test runner:

```bash
python -m unittest discover -v
```

GitHub Actions runs the suite on Python 3.10 and 3.12 for every pull request and every push to `main`.

## Deploy on Streamlit Community Cloud

1. Fork or use this repository in your GitHub account.
2. In Streamlit Community Cloud, create an app from the repository.
3. Select `app.py` as the entry point.
4. Open **App settings → Secrets** and add the values from `.streamlit/secrets.toml.example` with your real provider API key.
5. Deploy the application. The audit dashboard remains available without an API call; simple generation requires the configured secret.

## Methodology and limitations

AI answers are variable. Results may change with the model version, retrieval system, user location, personalization, prompt wording, conversation context and test date.

This project supports consistent directional measurement. It does not guarantee a ranking, citation, recommendation or commercial outcome. Human review remains necessary, especially for answer accuracy, source quality and competitive context.

## Documentation

- [How to run a GEO prompt audit](docs/how-to-run-a-geo-prompt-audit.md)
- [Metrics dictionary](docs/metrics-dictionary.md)
- [Scoring methodology](docs/scoring-methodology.md)
- [Data schema](docs/data-schema.md)
- [Dashboard interpretation guide](docs/dashboard-interpretation-guide.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Author

Built by [Mohammed Teto](https://mohammedteto.com)<br>
AI, Automation & LLM Visibility Consultant<br>
Casablanca, Morocco

## License

[MIT](LICENSE)
