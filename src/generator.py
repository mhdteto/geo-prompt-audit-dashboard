"""Small multi-provider wrapper for the public simple mode."""

from __future__ import annotations

from typing import Any


DEFAULT_MODEL = "gpt-5.6-luna"
OPENAI_PROVIDER = "openai"
GEMINI_PROVIDER = "gemini"
MAX_PROMPT_CHARS = 6_000
MAX_OUTPUT_TOKENS = 1_200
SYSTEM_INSTRUCTIONS = (
    "You are a concise, practical assistant. Reply in the same language as the user. "
    "Give a direct, well-structured answer. State uncertainty instead of inventing facts. "
    "Do not claim to have completed external actions that you did not actually perform."
)


def normalize_prompt(prompt: str) -> str:
    """Return a validated prompt suitable for a bounded public request."""
    normalized = prompt.strip()
    if not normalized:
        raise ValueError("Écrivez une demande avant de lancer la génération.")
    if len(normalized) > MAX_PROMPT_CHARS:
        raise ValueError(f"La demande ne doit pas dépasser {MAX_PROMPT_CHARS} caractères.")
    return normalized


def detect_provider(model: str, provider: str | None = None) -> str:
    """Resolve an explicit provider or infer it from the configured model name."""
    normalized_provider = (provider or "").strip().lower()
    if normalized_provider:
        if normalized_provider not in {OPENAI_PROVIDER, GEMINI_PROVIDER}:
            raise ValueError("Le fournisseur IA configuré n’est pas reconnu.")
        return normalized_provider
    if model.strip().lower().startswith("gemini-"):
        return GEMINI_PROVIDER
    return OPENAI_PROVIDER


def generate_response(
    prompt: str,
    api_key: str,
    *,
    model: str = DEFAULT_MODEL,
    provider: str | None = None,
    client: Any | None = None,
) -> str:
    """Generate one bounded answer with OpenAI or Google Gemini."""
    normalized_prompt = normalize_prompt(prompt)
    if not api_key.strip():
        raise ValueError("La génération n’est pas configurée sur ce serveur.")

    resolved_provider = detect_provider(model, provider)
    if resolved_provider == GEMINI_PROVIDER:
        if client is None:
            from google import genai

            client = genai.Client(api_key=api_key)

        from google.genai import types

        response = client.models.generate_content(
            model=model,
            contents=normalized_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            ),
        )
        output_text = str(getattr(response, "text", "") or "").strip()
    else:
        if client is None:
            from openai import OpenAI

            client = OpenAI(api_key=api_key, timeout=45.0, max_retries=1)

        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=normalized_prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            store=False,
        )
        output_text = str(getattr(response, "output_text", "") or "").strip()

    if not output_text:
        raise RuntimeError("The model returned an empty response.")
    return output_text


def public_error_message(error: Exception) -> str:
    """Map provider failures to safe, useful messages without leaking secrets."""
    error_name = error.__class__.__name__.lower()
    status_code = getattr(error, "status_code", None) or getattr(error, "code", None)
    if "authentication" in error_name or "permission" in error_name or status_code in {401, 403}:
        return "La configuration du service IA doit être vérifiée par l’administrateur."
    if "ratelimit" in error_name or status_code == 429:
        return "Le service reçoit trop de demandes. Réessayez dans quelques instants."
    if "timeout" in error_name or "connection" in error_name:
        return "Le service IA est momentanément indisponible. Réessayez dans quelques instants."
    if "badrequest" in error_name:
        return "La demande n’a pas pu être traitée. Reformulez-la puis réessayez."
    return "La génération a échoué. Réessayez dans quelques instants."
