"""Gemini API adapter for DUYEN DICH.

The API key is read only from GEMINI_API_KEY. It is never stored in source code.
Model can be overridden with GEMINI_MODEL.
"""

from __future__ import annotations

import os
from typing import Any

from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini is not configured in the runtime environment."""


def _client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError("GEMINI_API_KEY chưa được cấu hình.")
    return genai.Client(api_key=api_key)


def _resolve_model(model: str | None = None) -> str:
    """Always return a non-empty model name, including when the env var is blank."""
    return (model or os.getenv("GEMINI_MODEL") or DEFAULT_MODEL).strip()


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 4096,
) -> str:
    """Generate a text response from Gemini without exposing the API key."""
    if not prompt or not prompt.strip():
        raise ValueError("prompt không được rỗng")

    config_kwargs: dict[str, Any] = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction

    response = _client().models.generate_content(
        model=_resolve_model(model),
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini không trả về nội dung văn bản.")
    return text


def analyze_engine_output(engine_output: dict[str, Any], question: str = "") -> str:
    """Ask Gemini to interpret an already-computed engine result."""
    import json

    payload = json.dumps(engine_output, ensure_ascii=False, default=str)
    prompt = (
        "Hãy diễn giải kết quả Duyên Dịch dưới đây. "
        "Không tự ý thay đổi, tính lại hoặc phủ định các giá trị cấu trúc của Engine. "
        "Chỉ dùng chúng làm dữ liệu đầu vào để diễn giải rõ ràng, có cấu trúc và truy vết được.\n\n"
        f"Câu hỏi người dùng: {question or '(không cung cấp)'}\n\n"
        f"ENGINE_OUTPUT:\n{payload}"
    )
    return generate_text(
        prompt,
        system_instruction=(
            "Bạn là tầng diễn giải AI của hệ thống Duyên Dịch. "
            "Engine lõi là nguồn sự thật về kết quả tính toán; bạn không được sửa Core output. "
            "Phân biệt rõ dữ liệu Engine và phần diễn giải của AI."
        ),
    )
