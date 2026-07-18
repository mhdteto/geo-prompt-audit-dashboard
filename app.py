"""Interactive Streamlit application for GEO prompt-audit results."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import (
    category_summary,
    competitor_summary,
    engine_summary,
    headline_metrics,
    trend_summary,
)
from src.generator import (
    DEFAULT_MODEL,
    GEMINI_PROVIDER,
    MAX_PROMPT_CHARS,
    detect_provider,
    generate_response,
    public_error_message,
)
from src.report import build_html_report
from src.scoring import ensure_scores, score_label
from src.validation import validate_and_normalize


ROOT = Path(__file__).resolve().parent
SAMPLE_DATA = ROOT / "data" / "sample-results.csv"
TEMPLATE_DATA = ROOT / "data" / "data-template.csv"
LOGGER = logging.getLogger(__name__)

st.set_page_config(
    page_title="GEO Prompt Audit Dashboard",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {background:#f7fafc;border:1px solid #dce7f0;padding:14px;border-radius:12px;}
    [data-testid="stMetricValue"] {color:#102a43;}
    .small-note {color:#627d98;font-size:.88rem;}
    .app-credit {color:#627d98;font-size:.92rem;text-align:center;margin-top:1rem;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def read_csv(source: object) -> pd.DataFrame:
    return pd.read_csv(source)


def format_optional_percent(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.1f}%"


def runtime_setting(name: str) -> str | None:
    """Read a server-side setting without exposing it in the interface."""
    environment_value = os.getenv(name)
    if environment_value:
        return environment_value
    try:
        secret_value = st.secrets.get(name)
    except Exception:
        return None
    return str(secret_value) if secret_value else None


def runtime_provider_diagnostic(error: Exception) -> str:
    """Build safe diagnostic metadata without depending on a hot-reloaded import."""
    status_code = getattr(error, "status_code", None) or getattr(error, "code", None)
    body = getattr(error, "body", None)
    payload = body.get("error", body) if isinstance(body, dict) else {}
    remote_status = payload.get("status") if isinstance(payload, dict) else None
    provider_message = payload.get("message", "") if isinstance(payload, dict) else ""
    if not provider_message:
        provider_message = getattr(error, "message", "")
    message = str(provider_message).lower()

    reason = None
    details = payload.get("details", []) if isinstance(payload, dict) else []
    if isinstance(details, list):
        for detail in details:
            if isinstance(detail, dict) and detail.get("reason"):
                reason = str(detail["reason"])
                break

    if any(term in message for term in ("api key", "credential", "authorization key")):
        category = "credentials"
    elif "model" in message:
        category = "model"
    elif "store" in message:
        category = "storage"
    elif "generation_config" in message or "max_output" in message:
        category = "generation-config"
    elif "system_instruction" in message:
        category = "system-instruction"
    elif "input" in message:
        category = "input"
    else:
        category = "request"

    fields = {
        "type": error.__class__.__name__,
        "status": status_code,
        "provider_status": remote_status,
        "category": category,
        "reason": reason,
    }
    return " ".join(f"{name}={value}" for name, value in fields.items() if value is not None)


def render_app_credit() -> None:
    st.divider()
    st.markdown('<p class="app-credit">By Mohammed Teto</p>', unsafe_allow_html=True)


def render_simple_generator() -> None:
    st.subheader("Assistant IA — mode simple")
    st.write(
        "Écrivez votre demande en langage naturel. L’assistant répond directement "
        "dans la même langue, avec un résultat clair et exploitable."
    )

    configured_provider = runtime_setting("AI_PROVIDER")
    model = (
        runtime_setting("AI_MODEL")
        or runtime_setting("GEMINI_MODEL")
        or runtime_setting("OPENAI_MODEL")
        or DEFAULT_MODEL
    )
    provider = detect_provider(model, configured_provider)
    if provider == GEMINI_PROVIDER:
        api_key = (
            runtime_setting("GEMINI_API_KEY")
            or runtime_setting("AI_API_KEY")
            or runtime_setting("OPENAI_API_KEY")
        )
    else:
        api_key = runtime_setting("OPENAI_API_KEY") or runtime_setting("AI_API_KEY")
    generation_ready = bool(api_key)

    if not generation_ready:
        st.warning(
            "La génération publique n’est pas encore activée. "
            "L’administrateur doit configurer la clé du service IA."
        )
        with st.expander("Configuration administrateur"):
            st.code(
                'AI_PROVIDER = "gemini"\n'
                'AI_MODEL = "gemini-2.5-flash"\n'
                'GEMINI_API_KEY = "votre-cle-api"',
                language="toml",
            )

    with st.form("simple-generator-form"):
        prompt = st.text_area(
            "Votre demande",
            placeholder="Exemple : Prépare un plan marketing simple pour une PME marocaine.",
            height=180,
            max_chars=MAX_PROMPT_CHARS,
        )
        submitted = st.form_submit_button(
            "Générer le résultat",
            type="primary",
            width="stretch",
            disabled=not generation_ready,
        )

    if submitted:
        try:
            with st.spinner("Génération en cours…"):
                answer = generate_response(
                    prompt,
                    api_key or "",
                    model=model,
                    provider=provider,
                )
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            LOGGER.warning(
                "AI generation failed: %s",
                runtime_provider_diagnostic(exc),
            )
            st.error(public_error_message(exc))
        else:
            st.session_state["simple_generator_answer"] = answer

    answer = st.session_state.get("simple_generator_answer")
    if answer:
        st.success("Résultat généré")
        with st.container(border=True):
            st.markdown(answer)
        st.download_button(
            "Télécharger le résultat",
            data=answer.encode("utf-8"),
            file_name="resultat-ia.md",
            mime="text/markdown",
            width="stretch",
        )

    st.caption(
        f"Modèle configuré : {model}. Vérifiez les informations importantes avant de les utiliser."
    )


st.title("GEO Prompt Audit Dashboard")
st.caption(
    "Measure brand mentions, answer accuracy, citations and competitive visibility across AI answer engines."
)

mode = st.radio(
    "Choisir un mode",
    ["Génération simple", "Audit GEO"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "Génération simple":
    render_simple_generator()
    render_app_credit()
    st.stop()

with st.sidebar:
    st.header("Audit data")
    uploaded = st.file_uploader("Upload prompt results", type=["csv"])
    st.caption("Your data is processed only in the current Streamlit session.")
    with open(TEMPLATE_DATA, "rb") as template_file:
        st.download_button(
            "Download CSV template",
            data=template_file.read(),
            file_name="geo-audit-template.csv",
            mime="text/csv",
            width="stretch",
        )

try:
    raw_data = read_csv(uploaded if uploaded is not None else SAMPLE_DATA)
except Exception as exc:
    st.error(f"The CSV could not be read: {exc}")
    st.stop()

validation = validate_and_normalize(raw_data)
if not validation.is_valid:
    st.error("The dataset is not valid.")
    for error in validation.errors:
        st.write(f"- {error}")
    st.stop()

data = ensure_scores(validation.data)

with st.sidebar:
    st.divider()
    st.header("Filters")
    selected_brands = st.multiselect("Brand", sorted(data["brand"].unique()), default=sorted(data["brand"].unique()))
    selected_engines = st.multiselect("Engine", sorted(data["engine"].unique()), default=sorted(data["engine"].unique()))
    selected_categories = st.multiselect(
        "Prompt category",
        sorted(data["prompt_category"].unique()),
        default=sorted(data["prompt_category"].unique()),
    )
    start_date = data["date"].min().date()
    end_date = data["date"].max().date()
    selected_dates = st.date_input("Date range", value=(start_date, end_date), min_value=start_date, max_value=end_date)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    selected_start, selected_end = selected_dates
else:
    selected_start = selected_end = selected_dates

filtered = data[
    data["brand"].isin(selected_brands)
    & data["engine"].isin(selected_engines)
    & data["prompt_category"].isin(selected_categories)
    & data["date"].dt.date.between(selected_start, selected_end)
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

if uploaded is None:
    st.info("Showing a fictional Moroccan demo dataset. Upload your CSV to run a real audit.")
for warning in validation.warnings:
    st.caption(f"Data note: {warning}")

metrics = headline_metrics(filtered)
score = float(metrics["average_score"])

metric_columns = st.columns(6)
metric_columns[0].metric("Visibility score", f"{score:.1f}/100", help=score_label(score))
metric_columns[1].metric("Mention rate", f"{metrics['mention_rate']:.1f}%")
metric_columns[2].metric("Citation rate", f"{metrics['citation_rate']:.1f}%")
metric_columns[3].metric("Recommendation", format_optional_percent(metrics["recommendation_rate"]))
metric_columns[4].metric(
    "Average position",
    "N/A" if metrics["average_position"] is None else f"{metrics['average_position']:.2f}",
)
metric_columns[5].metric("Prompt tests", int(metrics["tests"]))

overview_tab, engines_tab, prompts_tab, competitors_tab, data_tab = st.tabs(
    ["Overview", "AI engines", "Prompt categories", "Competitors", "Data & export"]
)

with overview_tab:
    trend = trend_summary(filtered)
    left, right = st.columns([1.45, 1])
    with left:
        st.subheader("Visibility trend")
        trend_long = trend.melt(
            id_vars="Date",
            value_vars=["Average score", "Mention rate (%)", "Citation rate (%)"],
            var_name="Metric",
            value_name="Value",
        )
        figure = px.line(trend_long, x="Date", y="Value", color="Metric", markers=True)
        figure.update_layout(yaxis_range=[0, 100], legend_title_text="", hovermode="x unified")
        st.plotly_chart(figure, width="stretch")
    with right:
        st.subheader("Answer sentiment")
        sentiment = filtered["sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Tests")
        figure = px.pie(sentiment, names="Sentiment", values="Tests", hole=0.55)
        figure.update_layout(legend_title_text="")
        st.plotly_chart(figure, width="stretch")

with engines_tab:
    engines = engine_summary(filtered)
    st.subheader("Performance by AI answer engine")
    figure = px.bar(
        engines,
        x="Engine",
        y=["Average score", "Mention rate (%)", "Citation rate (%)"],
        barmode="group",
    )
    figure.update_layout(yaxis_range=[0, 100], legend_title_text="")
    st.plotly_chart(figure, width="stretch")
    st.dataframe(engines, width="stretch", hide_index=True)

with prompts_tab:
    categories = category_summary(filtered)
    st.subheader("Performance by prompt intent")
    figure = px.bar(
        categories.sort_values("Average score"),
        x="Average score",
        y="Prompt category",
        orientation="h",
        color="Mention rate (%)",
        color_continuous_scale="Blues",
        range_x=[0, 100],
    )
    st.plotly_chart(figure, width="stretch")
    st.dataframe(categories, width="stretch", hide_index=True)

with competitors_tab:
    competitors = competitor_summary(filtered)
    st.subheader("Competitive presence")
    if competitors.empty:
        st.info("No competitors were recorded in the selected results.")
    else:
        figure = px.bar(
            competitors.head(15).sort_values("Mentions"),
            x="Mentions",
            y="Competitor",
            orientation="h",
        )
        st.plotly_chart(figure, width="stretch")
        st.dataframe(competitors, width="stretch", hide_index=True)

with data_tab:
    st.subheader("Filtered audit data")
    display_data = filtered.drop(columns=["position_numeric"], errors="ignore").copy()
    display_data["date"] = display_data["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_data, width="stretch", hide_index=True)
    csv_bytes = display_data.to_csv(index=False).encode("utf-8")
    report = build_html_report(filtered, "GEO Prompt Audit Report")
    first, second = st.columns(2)
    first.download_button(
        "Download filtered CSV",
        data=csv_bytes,
        file_name="geo-audit-results.csv",
        mime="text/csv",
        width="stretch",
    )
    second.download_button(
        "Download HTML report",
        data=report.encode("utf-8"),
        file_name="geo-audit-report.html",
        mime="text/html",
        width="stretch",
    )

st.divider()
st.markdown(
    '<p class="small-note">Directional measurement only. Results can vary by model, retrieval system, location, prompt wording and date.</p>',
    unsafe_allow_html=True,
)
render_app_credit()
