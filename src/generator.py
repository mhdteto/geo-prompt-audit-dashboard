"""Small OpenAI Responses API wrapper for the public simple mode."""

from __future__ import annotations

from typing import Any


DEFAULT_MODEL = "gpt-5.6-luna"
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


def generate_response(
    prompt: str,
    api_key: str,
    *,
    model: str = DEFAULT_MODEL,
    client: Any | None = None,
) -> str:
    """Generate one bounded answer with the OpenAI Responses API."""
    normalized_prompt = normalize_prompt(prompt)
    if not api_key.strip():
        raise ValueError("La génération n’est pas configurée sur ce serveur.")

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
    if "authentication" in error_name or "permission" in error_name:
        return "La configuration OpenAI du serveur doit être vérifiée par l’administrateur."
    if "ratelimit" in error_name:
        return "Le service reçoit trop de demandes. Réessayez dans quelques instants."
    if "timeout" in error_name or "connection" in error_name:
        return "Le service IA est momentanément indisponible. Réessayez dans quelques instants."
    if "badrequest" in error_name:
        return "La demande n’a pas pu être traitée. Reformulez-la puis réessayez."
    return "La génération a échoué. Réessayez dans quelques instants."
