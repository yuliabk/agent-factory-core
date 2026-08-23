"""Command-line entry point for the offline PR-G1 dry validator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .validator import run_dry_validation


def _local_json_path(raw: str) -> Path:
    if "://" in raw:
        raise argparse.ArgumentTypeError("only local JSON paths are allowed")
    path = Path(raw).expanduser().resolve()
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"local JSON file not found: {raw}")
    return path


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate local synthetic runtime-portability fixtures without external calls."
    )
    parser.add_argument("--adapter", required=True, type=_local_json_path)
    parser.add_argument("--question-set", required=True, type=_local_json_path)
    parser.add_argument("--fixtures", required=True, type=_local_json_path)
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_dry_validation(
        _load_json(args.adapter),
        _load_json(args.question_set),
        _load_json(args.fixtures),
    )
    print(
        json.dumps(
            report,
            ensure_ascii=False,
            sort_keys=True,
            indent=None if args.compact else 2,
        )
    )
    return 0 if report["overall_verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
