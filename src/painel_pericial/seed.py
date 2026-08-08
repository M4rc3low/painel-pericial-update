from __future__ import annotations

import argparse
import csv

from .db import Process, SessionLocal, init_db


def import_csv(path: str) -> int:
    init_db()
    count = 0
    with open(path, newline="", encoding="utf-8-sig") as handle, SessionLocal.begin() as session:
        for row in csv.DictReader(handle):
            number = (row.get("process_number") or "").strip()
            if not number:
                continue
            obj = session.get(Process, number) or Process(process_number=number)
            obj.nickname = row.get("nickname", "")
            obj.client = row.get("client", "")
            obj.category = row.get("category", "")
            obj.active = row.get("active", "1").strip().lower() not in {"0", "false", "no"}
            session.add(obj)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a process registry into the configured database.")
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    print(f"Imported {import_csv(args.file)} processes")


if __name__ == "__main__":
    main()
