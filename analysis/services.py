import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple

import requests

from .prompts import build_prompt, validate_response, SUPPORTED_LANGUAGES

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3-flash-preview:generateContent"
)


def load_local_env() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env()


class AnalysisService:
    @classmethod
    def _post_request(cls, payload: dict) -> dict:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Gemini API key is not configured.")

        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def _extract_response(cls, data: dict) -> Tuple[str, dict]:
        raw = ""
        if data.get("candidates"):
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            raw = "".join([p.get("text", "") for p in parts])
        elif data.get("output"):
            parts = data["output"][0].get("content", {}).get("parts", [])
            raw = "".join([p.get("text", "") for p in parts])
        else:
            raw = data.get("response", {}).get("text", "")

        if not raw:
            raise RuntimeError("Gemini returned an empty response.")

        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.strip("`")

        start = raw.find("{")
        end = raw.rfind("}")
        if start < 0 or end < 0:
            raise RuntimeError("Could not parse JSON from Gemini response.")

        parsed = json.loads(raw[start : end + 1])
        return raw, parsed

    @classmethod
    def analyze(cls, code: str, language: str) -> dict:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        prompt_text = build_prompt(language, code)
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt_text}],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024,
                "candidateCount": 1,
            },
        }

        last_error: Exception | None = None
        for attempt in range(2):
            try:
                data = cls._post_request(payload)
                raw, parsed = cls._extract_response(data)
                validate_response(language, raw, parsed)
                return parsed
            except ValueError as exc:
                last_error = exc
                if attempt == 0:
                    continue
                raise RuntimeError(
                    "Gemini response failed language validation: " + str(exc)
                )
            except Exception as exc:
                last_error = exc
                if attempt == 0 and isinstance(exc, RuntimeError):
                    continue
                raise

        raise RuntimeError(
            "Gemini analysis failed after retry."
            + (f" {last_error}" if last_error else "")
        )
