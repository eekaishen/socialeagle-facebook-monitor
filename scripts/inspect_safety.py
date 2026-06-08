#!/usr/bin/env python3
"""Read-only inspector for SocialEagle-style monitoring safety artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def latest_report(reports_dir: Path) -> Path | None:
    dated_report = re.compile(r"^facebook_daily_\d{4}-\d{2}-\d{2}\.json$")
    candidates = sorted(
        p
        for p in reports_dir.glob("facebook_daily_*.json")
        if dated_report.match(p.name)
    )
    return candidates[-1] if candidates else None


def compact_report_summary(report: dict[str, Any]) -> dict[str, Any]:
    run_summary = report.get("run_summary") or {}
    totals = report.get("totals") or {}
    return {
        "target_date": report.get("target_date") or report.get("report_date"),
        "status": report.get("status"),
        "collection_state": report.get("collection_state"),
        "run_verdict": run_summary.get("run_verdict"),
        "accuracy_status": run_summary.get("accuracy_status"),
        "active_brands": run_summary.get("active_brands") or totals.get("targets"),
        "checked_brands": run_summary.get("checked_brands") or totals.get("ok_targets"),
        "not_checked_targets": totals.get("not_checked_targets"),
        "row_accuracy_pct": run_summary.get("row_accuracy_pct"),
    }


def build_result(reports_dir: Path, safety_name: str) -> dict[str, Any]:
    safety_path = reports_dir / safety_name
    if not safety_path.exists():
        raise SystemExit(f"Missing safety file: {safety_path}")

    safety = load_json(safety_path)
    report_path = latest_report(reports_dir)
    report_summary: dict[str, Any] | None = None
    if report_path:
        report_summary = compact_report_summary(load_json(report_path))

    return {
        "ok": safety.get("ok") is True,
        "safety_path": str(safety_path),
        "latest_report_path": str(report_path) if report_path else None,
        "safety_target_date": safety.get("target_date"),
        "report_summary": report_summary,
        "blocking_targets": safety.get("blocking_targets") or [],
        "automation_attempts": safety.get("automation_attempts") or [],
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"ok={str(result['ok']).lower()}")
    print(f"safety_path={result['safety_path']}")
    print(f"latest_report_path={result['latest_report_path']}")
    if result.get("report_summary"):
        print("report_summary=" + json.dumps(result["report_summary"], ensure_ascii=False))

    blockers = result["blocking_targets"]
    print(f"blocking_targets={len(blockers)}")
    for blocker in blockers:
        print(
            "{target_name} | {page_status}/{metric_status} | {status_reason} | {page_url}".format(
                target_name=blocker.get("target_name", ""),
                page_status=blocker.get("page_status", ""),
                metric_status=blocker.get("metric_status", ""),
                status_reason=blocker.get("status_reason", ""),
                page_url=blocker.get("page_url", ""),
            )
        )

    attempts = result["automation_attempts"]
    print(f"automation_attempts={len(attempts)}")
    for attempt in attempts:
        print(json.dumps(attempt, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reports-dir",
        default="output/reports/daily",
        help="Directory containing the safety JSON and dated report JSON files.",
    )
    parser.add_argument(
        "--safety-name",
        default="facebook_daily_latest_safety.json",
        help="Safety JSON file name inside --reports-dir.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = build_result(Path(args.reports_dir), args.safety_name)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_text(result)

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
