import unittest

from src.generator import (
    GEMINI_PROVIDER,
    MAX_OUTPUT_TOKENS,
    MAX_PROMPT_CHARS,
    OPENAI_PROVIDER,
    SYSTEM_INSTRUCTIONS,
    detect_provider,
    generate_response,
    normalize_prompt,
    provider_error_diagnostic,
    public_error_message,
)


class FakeResponse:
    output_text = "Une réponse utile."


class FakeResponses:
    def __init__(self):
        self.arguments = None

    def create(self, **kwargs):
        self.arguments = kwargs
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


class FakeGeminiResponse:
    output_text = "Une réponse Gemini utile."


class FakeInteractions:
    def __init__(self):
        self.arguments = None

    def create(self, **kwargs):
        self.arguments = kwargs
        return FakeGeminiResponse()


class FakeGeminiClient:
    def __init__(self):
        self.interactions = FakeInteractions()


class GeneratorTests(unittest.TestCase):
    def test_prompt_is_trimmed(self):
        self.assertEqual(normalize_prompt("  Bonjour  "), "Bonjour")

    def test_empty_and_oversized_prompts_are_rejected(self):
        with self.assertRaises(ValueError):
            normalize_prompt("   ")
        with self.assertRaises(ValueError):
            normalize_prompt("x" * (MAX_PROMPT_CHARS + 1))

    def test_response_api_call_is_bounded_and_not_stored(self):
        client = FakeClient()
        result = generate_response(" Aide-moi ", "test-key", model="test-model", client=client)

        self.assertEqual(result, "Une réponse utile.")
        self.assertEqual(client.responses.arguments["model"], "test-model")
        self.assertEqual(client.responses.arguments["instructions"], SYSTEM_INSTRUCTIONS)
        self.assertEqual(client.responses.arguments["input"], "Aide-moi")
        self.assertEqual(client.responses.arguments["max_output_tokens"], MAX_OUTPUT_TOKENS)
        self.assertFalse(client.responses.arguments["store"])

    def test_provider_is_inferred_from_model_or_explicit_setting(self):
        self.assertEqual(detect_provider("gemini-2.5-flash"), GEMINI_PROVIDER)
        self.assertEqual(detect_provider("gpt-5.6-luna"), OPENAI_PROVIDER)
        self.assertEqual(detect_provider("custom", "gemini"), GEMINI_PROVIDER)
        with self.assertRaises(ValueError):
            detect_provider("custom", "unknown")

    def test_gemini_call_is_bounded_and_uses_system_instructions(self):
        client = FakeGeminiClient()
        result = generate_response(
            " Aide-moi ",
            "test-key",
            model="gemini-2.5-flash",
            client=client,
        )

        self.assertEqual(result, "Une réponse Gemini utile.")
        arguments = client.interactions.arguments
        self.assertEqual(arguments["model"], "gemini-2.5-flash")
        self.assertEqual(arguments["input"], "Aide-moi")
        self.assertEqual(arguments["system_instruction"], SYSTEM_INSTRUCTIONS)
        self.assertEqual(
            arguments["generation_config"]["max_output_tokens"],
            MAX_OUTPUT_TOKENS,
        )
        self.assertFalse(arguments["store"])

    def test_missing_key_and_empty_output_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_response("Bonjour", "", client=FakeClient())

        client = FakeClient()
        client.responses.create = lambda **kwargs: type("Response", (), {"output_text": ""})()
        with self.assertRaises(RuntimeError):
            generate_response("Bonjour", "test-key", client=client)

    def test_provider_errors_are_safe_for_public_display(self):
        AuthenticationError = type("AuthenticationError", (Exception,), {})
        RateLimitError = type("RateLimitError", (Exception,), {})
        self.assertIn("administrateur", public_error_message(AuthenticationError()))
        self.assertIn("trop de demandes", public_error_message(RateLimitError()))

        GooglePermissionError = type(
            "ClientError",
            (Exception,),
            {"status_code": 403},
        )
        self.assertIn("administrateur", public_error_message(GooglePermissionError()))

    def test_provider_diagnostics_include_codes_but_not_provider_message(self):
        ProviderError = type(
            "BadRequestError",
            (Exception,),
            {
                "status_code": 400,
                "body": {
                    "error": {
                        "status": "INVALID_ARGUMENT",
                        "message": "API key not valid: secret-value",
                        "details": [{"reason": "API_KEY_INVALID"}],
                    }
                },
            },
        )
        diagnostic = provider_error_diagnostic(ProviderError())

        self.assertIn("status=400", diagnostic)
        self.assertIn("provider_status=INVALID_ARGUMENT", diagnostic)
        self.assertIn("category=credentials", diagnostic)
        self.assertIn("reason=API_KEY_INVALID", diagnostic)
        self.assertNotIn("secret-value", diagnostic)

        MessageOnlyError = type(
            "BadRequestError",
            (Exception,),
            {
                "status_code": 400,
                "message": "The store parameter is not supported: secret-value",
            },
        )
        message_diagnostic = provider_error_diagnostic(MessageOnlyError())
        self.assertIn("category=storage", message_diagnostic)
        self.assertNotIn("secret-value", message_diagnostic)


if __name__ == "__main__":
    unittest.main()
