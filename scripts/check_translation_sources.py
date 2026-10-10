#!/usr/bin/env python3
"""Compare Qt TS message identities, not translation formatting or translated text."""
import collections
import pathlib
import sys
import xml.etree.ElementTree as ET

def message_keys(path: pathlib.Path):
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise RuntimeError(f"{path}: cannot parse TS catalog: {exc}") from exc
    keys = []
    for context in root.findall("context"):
        context_name = context.findtext("name", default="")
        for message in context.findall("message"):
            keys.append((
                context_name, message.get("id", ""), message.get("numerus", ""),
                message.findtext("source", default=""), message.findtext("comment", default=""),
            ))
    return collections.Counter(keys)

def main():
    if len(sys.argv) != 3:
        print("usage: check_translation_sources.py SNAPSHOT_DIR UPDATED_DIR", file=sys.stderr)
        return 2
    snapshot_dir, updated_dir = map(pathlib.Path, sys.argv[1:])
    snapshots = sorted(snapshot_dir.glob("*.ts"))
    if not snapshots:
        print(f"No TS catalogs found in {snapshot_dir}", file=sys.stderr)
        return 2
    errors = []
    for before in snapshots:
        after = updated_dir / before.name
        if not after.is_file():
            errors.append(f"{before.name}: catalog disappeared after lupdate")
            continue
        try:
            old_keys, new_keys = message_keys(before), message_keys(after)
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        missing, added = old_keys - new_keys, new_keys - old_keys
        if missing or added:
            errors.append(f"{before.name}: source-message keys changed ({sum(missing.values())} removed, {sum(added.values())} added)")
    if errors:
        print("Translation source check failed:", file=sys.stderr)
        print("\n".join(f"  - {e}" for e in errors), file=sys.stderr)
        print("Run the update_translations target and review source-string changes.", file=sys.stderr)
        return 1
    print(f"Translation source check passed for {len(snapshots)} catalogs.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
