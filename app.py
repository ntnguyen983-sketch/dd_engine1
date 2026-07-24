#!/usr/bin/env python3
"""
app.py — Web API cho hệ thống DUYÊN DỊCH (DCGF), dựng trên Flask.

Chạy:
    python app.py
    # mặc định lắng nghe tại http://127.0.0.1:5000

Endpoints:
    GET  /health
    POST /api/khoi-que
        Body JSON, một trong các dạng:
          {"mode": "thoi_gian"}
          {"mode": "hai_so", "x": 7, "y": 3}
          {"mode": "mot_tin_hieu", "total": 4}
          {"mode": "thu_cong", "upper": 4, "lower": 2, "active_line": 4}
        Trả về Output Chuẩn Hóa S12 (JSON).
"""

from __future__ import annotations

from dataclasses import is_dataclass, asdict

from flask import Flask, jsonify, request

from engine.pipeline import cast_and_run
from engine.report import build_s12_report

app = Flask(__name__)


def _json_safe(obj):
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "system": "Duyên Dịch (DCGF)", "version": "1.0.0"})


@app.post("/api/khoi-que")
def khoi_que():
    body = request.get_json(silent=True) or {}
    mode = body.get("mode")
    if mode not in ("thoi_gian", "hai_so", "mot_tin_hieu", "thu_cong"):
        return jsonify({"error": "Trường 'mode' phải là một trong: thoi_gian, hai_so, mot_tin_hieu, thu_cong"}), 400

    try:
        if mode == "thoi_gian":
            result = cast_and_run("thoi_gian")
        elif mode == "hai_so":
            result = cast_and_run("hai_so", x=int(body["x"]), y=int(body["y"]))
        elif mode == "mot_tin_hieu":
            result = cast_and_run("mot_tin_hieu", total=int(body["total"]))
        else:  # thu_cong
            result = cast_and_run(
                "thu_cong",
                upper=int(body["upper"]),
                lower=int(body["lower"]),
                active_line=int(body["active_line"]),
            )
    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Tham số không hợp lệ: {exc}"}), 400

    report = build_s12_report(result)
    return app.response_class(
        response=__import__("json").dumps(report, ensure_ascii=False, indent=2, default=_json_safe),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True)
