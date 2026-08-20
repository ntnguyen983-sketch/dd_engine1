#!/usr/bin/env python3
"""Web API cho hệ thống DUYÊN DỊCH (DCGF)."""

from __future__ import annotations

import os
from dataclasses import asdict, is_dataclass

from flask import Flask, jsonify, request

from engine.pipeline import cast_and_run
from engine.report import build_s12_report
from gemini_service import GeminiConfigurationError, analyze_engine_output, generate_text

app = Flask(__name__)
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-3.6-flash"


def _json_safe(obj):
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def _run_engine(body: dict):
    mode = body.get("mode")
    if mode not in ("thoi_gian", "hai_so", "mot_tin_hieu", "thu_cong"):
        raise ValueError("Trường 'mode' phải là một trong: thoi_gian, hai_so, mot_tin_hieu, thu_cong")
    if mode == "thoi_gian":
        return cast_and_run("thoi_gian")
    if mode == "hai_so":
        return cast_and_run("hai_so", x=int(body["x"]), y=int(body["y"]))
    if mode == "mot_tin_hieu":
        return cast_and_run("mot_tin_hieu", total=int(body["total"]))
    return cast_and_run("thu_cong", upper=int(body["upper"]), lower=int(body["lower"]), active_line=int(body["active_line"]))


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "system": "Duyên Dịch (DCGF)",
        "version": "1.0.0",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "gemini_model": DEFAULT_GEMINI_MODEL,
    })


@app.post("/api/khoi-que")
def khoi_que():
    body = request.get_json(silent=True) or {}
    try:
        result = _run_engine(body)
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify({"error": f"Tham số không hợp lệ: {exc}"}), 400
    report = build_s12_report(result)
    return app.response_class(response=__import__("json").dumps(report, ensure_ascii=False, indent=2, default=_json_safe), status=200, mimetype="application/json")


@app.post("/api/ai")
def ai():
    body = request.get_json(silent=True) or {}
    prompt = body.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Trường 'prompt' bắt buộc và phải là chuỗi không rỗng."}), 400
    model = body.get("model") or DEFAULT_GEMINI_MODEL
    try:
        text = generate_text(prompt, system_instruction=body.get("system_instruction"), model=model)
    except GeminiConfigurationError as exc:
        return jsonify({"error": str(exc), "code": "GEMINI_NOT_CONFIGURED"}), 503
    except Exception as exc:
        app.logger.exception("Gemini request failed")
        return jsonify({"error": str(exc), "code": "GEMINI_REQUEST_FAILED"}), 502
    return jsonify({"model": model, "text": text})


@app.post("/api/duyen-dich/analyze")
def duyen_dich_analyze():
    body = request.get_json(silent=True) or {}
    question = body.get("question", "")
    try:
        engine_result = _run_engine(body)
        report = build_s12_report(engine_result)
        text = analyze_engine_output(report, question=question)
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify({"error": f"Tham số Engine không hợp lệ: {exc}"}), 400
    except GeminiConfigurationError as exc:
        return jsonify({"error": str(exc), "code": "GEMINI_NOT_CONFIGURED"}), 503
    except Exception as exc:
        app.logger.exception("Duyên Dịch Gemini analysis failed")
        return jsonify({"error": str(exc), "code": "ANALYSIS_FAILED"}), 502
    return jsonify({"engine_output": report, "ai_interpretation": text})


if __name__ == "__main__":
    app.run(debug=True)
