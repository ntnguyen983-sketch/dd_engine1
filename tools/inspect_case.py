#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def compact(value, limit=500):
    text = json.dumps(value, ensure_ascii=False, indent=2)
    return text if len(text) <= limit else text[:limit] + "\n…"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: inspect_case.py <json>")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    engine = data.get("engine_output", {})
    print("TOP_LEVEL", sorted(data))
    print("ENGINE_SECTIONS", sorted(engine))
    for name, value in engine.items():
        print(f"\n## {name} ({type(value).__name__})")
        if isinstance(value, dict):
            print("KEYS", sorted(value))
            for key, child in value.items():
                print(f"\n### {key} ({type(child).__name__})")
                print(compact(child))
        else:
            print(compact(value))
    ai = data.get("ai_interpretation")
    print("\nAI_TYPE", type(ai).__name__, "AI_CHARS", len(ai) if isinstance(ai, str) else "-")
    if isinstance(ai, str):
        print(ai[:1200])


if __name__ == "__main__":
    main()
