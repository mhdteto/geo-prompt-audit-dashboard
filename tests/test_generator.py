import unittest

from src.generator import (
    MAX_OUTPUT_TOKENS,
    MAX_PROMPT_CHARS,
    SYSTEM_INSTRUCTIONS,
    generate_response,
    normalize_prompt,
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


if __name__ == "__main__":
    unittest.main()
