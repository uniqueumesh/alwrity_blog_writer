import time
from google import genai


FALLBACK_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]


def _is_retryable_error(err):
    message = str(err).lower()
    retry_tokens = ("503", "unavailable", "429", "rate limit", "timeout", "temporar")
    return any(token in message for token in retry_tokens)


def generate_with_fallback(prompt, api_key, models=None, max_retries=2):
    """Generate text using fallback models from fastest to slowest."""
    client = genai.Client(api_key=api_key)
    model_list = models or FALLBACK_MODELS
    errors = []

    for model_name in model_list:
        for attempt in range(max_retries + 1):
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                return response.text
            except Exception as err:
                errors.append(f"{model_name}: {err}")
                if attempt < max_retries and _is_retryable_error(err):
                    time.sleep(1 + attempt)
                    continue
                break

    raise RuntimeError("All Gemini fallback models failed. " + " | ".join(errors))
