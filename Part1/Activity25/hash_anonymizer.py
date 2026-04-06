import csv
import hashlib
import sys
from pathlib import Path


def sha256_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def anonymize_csv(input_path: Path, output_path: Path) -> int:
    with input_path.open("r", newline="", encoding="utf-8") as src:
        reader = csv.DictReader(src)
        rows = list(reader)

    if not rows:
        raise ValueError("Input CSV contains no records")

    fieldnames = list(rows[0].keys())
    if "email" not in fieldnames:
        raise ValueError("Input CSV must contain an 'email' column")

    output_rows = []
    for row in rows:
        new_row = dict(row)
        new_row["email"] = sha256_hash(row["email"].strip().lower())
        output_rows.append(new_row)

    with output_path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    return len(output_rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 hash_anonymizer.py <input_csv> <output_csv>")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    processed = anonymize_csv(input_path, output_path)
    print(f"Records processed: {processed}")
    print(f"Output written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
