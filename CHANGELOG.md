# Changelog

## v1.2.1 - Gemini provider support

Released: 2026-07-18

### Fixed

- Route `gemini-*` models to the Google Gemini API instead of the OpenAI API.
- Use Google’s current Interactions API for compatibility with Gemini authorization keys.
- Support neutral provider settings while keeping the initial Streamlit configuration compatible.
- Use provider-neutral public errors without exposing API details.

### Changed

- Document the live Streamlit application and both supported AI providers.

## v1.2.0 - Simple AI generation

Released: 2026-07-18

### Added

- Public simple mode with one request field and a direct AI-generated result.
- Server-side OpenAI Responses API integration with bounded input and output.
- Safe provider-error messages and downloadable Markdown results.
- Streamlit secrets example and deployment instructions.
- Unit tests for prompt validation and API request construction.

## v1.1.0 - Interactive Dashboard

Released: 2026-07-18

### Added

- Interactive Streamlit application with CSV upload and filters.
- Visibility, mention, citation, recommendation, accuracy and position KPIs.
- AI-engine, prompt-category, trend and competitor views.
- Standalone HTML and filtered CSV exports.
- CSV validation, normalization and transparent automatic scoring.
- Backward compatibility with the v1.0 data structure.
- Fictional multi-date Moroccan demo dataset and reusable CSV template.
- Unit tests and GitHub Actions for Python 3.10 and 3.12.

### Changed

- Reworked the README around the runnable application.
- Added optional `brand` and `recommended` fields to the data schema.
- Moved Streamlit from a future idea to the core public implementation.

## v1.0 - Initial Public Release

Released: 2026-06-15

### Added

- Sample GEO prompt audit dataset.
- Prompt tracking structure.
- Scoring model.
- Dashboard logic documentation.
- Example notebook.
- Documentation for running a GEO prompt audit.
- Metrics dictionary.
- Data schema.
- Interpretation guide.
- Roadmap.
- Changelog.
- MIT license.

### Purpose

This first version provides a practical structure to track brand visibility across AI answer engines using prompt-level testing.

The goal is to help consultants, SMBs and B2B teams measure:

- Brand mention rate.
- Mention position.
- Answer sentiment.
- Answer accuracy.
- Source citations.
- Competitor presence.
- Prompt category performance.
- Visibility score.

### Notes

This project does not guarantee AI visibility, rankings, mentions or citations.

AI answers can vary depending on time, model version, user context, location, prompt wording and retrieval behavior.

This dashboard should be used as a practical monitoring tool, not as an absolute measurement system.
