#!/usr/bin/env python3
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def compact(value: Any, limit: int = 180) -> str:
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
    else:
        text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def walk(value: Any, path: str, presence: dict[str, set[str]], examples: dict[str, list[str]]) -> None:
    presence[path].add(type_name(value))
    if len(examples[path]) < 3:
        item = compact(value)
        if item not in examples[path]:
            examples[path].append(item)
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            walk(child, child_path, presence, examples)
    elif isinstance(value, list):
        for child in value[:10]:
            walk(child, f"{path}[]", presence, examples)


def md_table(rows: list[tuple[str, str, str, str]]) -> str:
    lines = ["| Path | Cases | Type | Example |", "|---|---:|---|---|"]
    lines.extend(f"| `{path}` | {cases} | `{types}` | {example.replace('|', '\\|')} |" for path, cases, types, example in rows)
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: analyze_live_schema.py <case-directory>")
    root = Path(sys.argv[1]).resolve()
    result_rows = []
    with (root / "results.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 5:
                result_rows.append(parts)

    presence: dict[str, set[str]] = defaultdict(set)
    examples: dict[str, list[str]] = defaultdict(list)
    case_paths: dict[str, set[str]] = defaultdict(set)
    top_keys: dict[str, set[str]] = defaultdict(set)
    status = []
    loaded_cases = []
    for case_id, total, code, seconds, file_name in result_rows:
        payload = json.loads(Path(file_name).read_text(encoding="utf-8"))
        loaded_cases.append({"case": case_id, "total": int(total), "status": int(code), "seconds": float(seconds), "file": file_name})
        status.append({"case": case_id, "status": int(code), "seconds": float(seconds)})
        if isinstance(payload, dict):
            top_keys[case_id].update(payload.keys())
        walk(payload, "", presence, examples)
        local_presence: dict[str, set[str]] = defaultdict(set)
        walk(payload, "", local_presence, defaultdict(list))
        for path in local_presence:
            case_paths[path].add(case_id)

    paths = []
    for path in sorted(presence):
        if not path:
            continue
        paths.append((path, str(len(case_paths[path])), ", ".join(sorted(presence[path])), "; ".join(examples[path])))
    engine_paths = [row for row in paths if row[0].startswith("engine_output.")]
    ai_paths = [row for row in paths if row[0].startswith("ai_interpretation")]
    payload_paths = [row for row in paths if not row[0].startswith("engine_output") and not row[0].startswith("ai_interpretation")]

    report = {
        "directory": str(root),
        "cases": loaded_cases,
        "top_level_keys_by_case": {case: sorted(keys) for case, keys in top_keys.items()},
        "union_path_count": len(paths),
        "engine_path_count": len(engine_paths),
        "ai_path_count": len(ai_paths),
        "payload_path_count": len(payload_paths),
        "engine_paths": [{"path": p, "cases": int(c), "types": t, "examples": e} for p, c, t, e in engine_paths],
        "ai_paths": [{"path": p, "cases": int(c), "types": t, "examples": e} for p, c, t, e in ai_paths],
        "payload_paths": [{"path": p, "cases": int(c), "types": t, "examples": e} for p, c, t, e in payload_paths],
    }
    (root / "schema_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        f"# Live Engine schema report\n\nDirectory: `{root}`\n",
        "## Cases\n",
        "| Case | Total | HTTP | Seconds |\n|---|---:|---:|---:|",
    ]
    lines.extend(f"| `{item['case']}` | {item['total']} | {item['status']} | {item['seconds']:.2f} |" for item in loaded_cases)
    lines.extend(["", f"Union paths: **{len(paths)}**; Engine paths: **{len(engine_paths)}**.", "", "## Top-level key sets\n"])
    for case, keys in sorted(top_keys.items()):
        lines.append(f"- `{case}`: {', '.join(f'`{key}`' for key in sorted(keys))}")
    lines.extend(["", "## Engine output paths\n", md_table(engine_paths), "", "## Response / AI paths\n", md_table(ai_paths + payload_paths)])
    (root / "schema_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(root / "schema_report.json")
    print(root / "schema_report.md")
    print(f"cases={len(loaded_cases)} union_paths={len(paths)} engine_paths={len(engine_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
