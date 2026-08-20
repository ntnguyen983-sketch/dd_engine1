"""Gemini API adapter for DUYEN DICH.

Uses the Gemini REST API directly so the serverless runtime does not retain a
Google GenAI client between invocations.
"""

from __future__ import annotations

import json
import os
from urllib import error, request
from typing import Any

DEFAULT_MODEL = "gemini-3.6-flash"

class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini is not configured in the runtime environment."""

def _resolve_model(model: str | None = None) -> str:
    return (model or os.getenv("GEMINI_MODEL") or DEFAULT_MODEL).strip()

def generate_text(prompt: str, *, system_instruction: str | None = None, model: str | None = None, temperature: float = 0.2, max_output_tokens: int = 4096) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("prompt không được rỗng")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError("GEMINI_API_KEY chưa được cấu hình.")
    resolved_model = _resolve_model(model)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{resolved_model}:generateContent?key={api_key}"
    payload: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_output_tokens},
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
    req = request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Không kết nối được Gemini: {exc.reason}") from exc
    candidates = result.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini không trả về candidate: {result}")
    parts = (candidates[0].get("content") or {}).get("parts") or []
    text = "".join(str(part.get("text", "")) for part in parts).strip()
    if not text:
        raise RuntimeError(f"Gemini không trả về nội dung văn bản: {result}")
    return text

def analyze_engine_output(engine_output: dict[str, Any], question: str = "") -> str:
    payload = json.dumps(engine_output, ensure_ascii=False, default=str)
    prompt = ("Hãy diễn giải kết quả Duyên Dịch dưới đây. Không tự ý thay đổi, tính lại hoặc phủ định các giá trị cấu trúc của Engine. Chỉ dùng chúng làm dữ liệu đầu vào để diễn giải rõ ràng, có cấu trúc và truy vết được.\n\n" f"Câu hỏi người dùng: {question or '(không cung cấp)'}\n\n" f"ENGINE_OUTPUT:\n{payload}")
    return generate_text(prompt, system_instruction="Bạn là tầng diễn giải AI của hệ thống Duyên Dịch. Engine lõi là nguồn sự thật về kết quả tính toán; bạn không được sửa Core output. Phân biệt rõ dữ liệu Engine và phần diễn giải của AI.")
