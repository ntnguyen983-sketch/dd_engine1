#!/usr/bin/env python3
"""
main.py — CLI cho hệ thống DUYÊN DỊCH (DCGF).

Cách dùng:
    python main.py thoi-gian
    python main.py hai-so --x 7 --y 3
    python main.py mot-tin-hieu --total 4
    python main.py thu-cong --upper 4 --lower 2 --active-line 4
    python main.py thoi-gian --json      # xuất JSON đầy đủ thay vì văn bản
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from engine.pipeline import cast_and_run
from engine.report import build_s12_report, render_text


def _print_result(result: dict, as_json: bool) -> None:
    report = build_s12_report(result)
    if as_json:

        def _default(o):
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)

        print(json.dumps(report, ensure_ascii=False, indent=2, default=_default))
    else:
        print(render_text(report))


def main() -> int:
    json_parent = argparse.ArgumentParser(add_help=False)
    json_parent.add_argument("--json", action="store_true", help="Xuất kết quả dạng JSON đầy đủ.")

    parser = argparse.ArgumentParser(
        description="Duyên Dịch (DCGF) — khởi quẻ và chạy pipeline S00-S12.",
        parents=[json_parent],
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    p_time = sub.add_parser("thoi-gian", help="Khởi quẻ theo thời điểm hiện tại (mặc định).", parents=[json_parent])
    p_time.add_argument("--datetime", type=str, default=None, help="ISO datetime tùy chọn, vd 2026-07-24T10:30:00")

    p_two = sub.add_parser("hai-so", help="Khởi quẻ Mai Hoa từ hai số x, y.", parents=[json_parent])
    p_two.add_argument("--x", type=int, required=True)
    p_two.add_argument("--y", type=int, required=True)

    p_one = sub.add_parser("mot-tin-hieu", help="Bồ khuyết Mai Hoa từ một tín hiệu tổng (vd 'gà gáy 4 âm').",
                           parents=[json_parent])
    p_one.add_argument("--total", type=int, required=True)

    p_manual = sub.add_parser("thu-cong", help="Nhập trực tiếp Thượng/Hạ quái và Hào động.", parents=[json_parent])
    p_manual.add_argument("--upper", type=int, required=True, choices=range(1, 9))
    p_manual.add_argument("--lower", type=int, required=True, choices=range(1, 9))
    p_manual.add_argument("--active-line", type=int, required=True, choices=range(1, 7))

    args = parser.parse_args()

    kwargs: dict = {}
    if args.mode == "thoi-gian":
        if args.datetime:
            kwargs["dt"] = datetime.fromisoformat(args.datetime)
        result = cast_and_run("thoi_gian", **kwargs)
    elif args.mode == "hai-so":
        result = cast_and_run("hai_so", x=args.x, y=args.y)
    elif args.mode == "mot-tin-hieu":
        result = cast_and_run("mot_tin_hieu", total=args.total)
    elif args.mode == "thu-cong":
        result = cast_and_run(
            "thu_cong", upper=args.upper, lower=args.lower, active_line=args.active_line
        )
    else:
        parser.print_help()
        return 1

    _print_result(result, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
