#!/usr/bin/env python3
import argparse
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = [
    "evidence/final_nothink_csv_checksum.sha256",
    "evidence/final_nothink_raw_checksums.sha256",
    "evidence/final_runner_v2_checksum.sha256",
    "evidence/final_scenarios_checksum.sha256",
    "evidence/v2_csv_checksum.sha256",
    "evidence/v2_input_checksums.sha256",
    "evidence/v2_raw_checksums.sha256",
    "evidence/v2_runner_checksum.sha256",
    "evidence/mcp_final_csv_checksum.sha256",
    "evidence/mcp_final_input_checksums.sha256",
    "evidence/mcp_final_raw_checksums.sha256",
    "evidence/final_analysis_checksums.sha256",
]


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Read-only verification of frozen experimental manifests.")
    parser.add_argument("--release-snapshot", action="store_true",
                        help="Also check the historical intake release manifest; publication edits and archived documents are expected to differ.")
    args = parser.parse_args()
    manifests = MANIFESTS + (["evidence/release_manifest.sha256"] if args.release_snapshot else [])
    failures = []
    checked = 0

    for rel_manifest in manifests:
        manifest = ROOT / rel_manifest
        if not manifest.exists():
            failures.append((rel_manifest, "manifest missing"))
            continue

        lines = manifest.read_text(encoding="utf-8").splitlines()
        if not any(line.strip() for line in lines):
            failures.append((rel_manifest, "empty manifest"))
        for number, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            entry = re.fullmatch(r"([0-9a-f]{64})\s+(.+)", line)
            if entry is None:
                failures.append((f"{rel_manifest}:{number}", "malformed checksum entry"))
                continue
            expected, rel_path = entry.groups()
            rel_path = rel_path.lstrip("* ")
            target = (ROOT / rel_path).resolve()
            if not target.is_relative_to(ROOT):
                failures.append((rel_path, "path escapes repository"))
                continue
            checked += 1
            if not target.is_file():
                failures.append((rel_path, "file missing"))
                continue
            actual = sha256(target)
            if actual != expected:
                failures.append((rel_path, f"hash mismatch: {actual}"))

    print(f"Checked {checked} checksum entries across {len(manifests)} manifests.")

    if failures:
        print("FAIL")
        for path, reason in failures:
            print(f"  {path}: {reason}")
        raise SystemExit(1)

    print("PASS: all checked frozen experimental checksums match.")
    if not args.release_snapshot:
        print("The preserved release_manifest.sha256 is the historical intake snapshot; see evidence/README.md.")


if __name__ == "__main__":
    main()
