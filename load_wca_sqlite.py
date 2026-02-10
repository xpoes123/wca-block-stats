import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("wca.db")
DATA_DIR = Path("data")


def table_name_from_file(path: Path) -> str:
    # data/WCA_export_results.tsv -> results
    name = path.stem
    if name.startswith("WCA_export_"):
        name = name[len("WCA_export_") :]
    return name


def infer_sqlite_type(sample: str | None) -> str:
    if sample is None:
        return "TEXT"
    s = sample.strip()
    if s == "":
        return "TEXT"
    if s.lstrip("-").isdigit():
        return "INTEGER"
    return "TEXT"


def normalize_row(row: list[str], width: int) -> list[str]:
    if len(row) < width:
        return row + [""] * (width - len(row))
    if len(row) > width:
        return row[:width]
    return row


def load_tsv(conn: sqlite3.Connection, tsv_path: Path) -> None:
    table = table_name_from_file(tsv_path)
    print(f"Loading {table} from {tsv_path.name} ...")

    with tsv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        # Preview rows for crude type inference
        preview: list[list[str]] = []
        for _ in range(200):
            try:
                preview.append(next(reader))
            except StopIteration:
                break

        col_types: list[tuple[str, str]] = []
        for i, col in enumerate(header):
            sample = None
            for r in preview:
                if i < len(r) and r[i] != "":
                    sample = r[i]
                    break
            col_types.append((col, infer_sqlite_type(sample)))

        conn.execute(f'DROP TABLE IF EXISTS "{table}"')
        cols_sql = ", ".join(f'"{c}" {t}' for c, t in col_types)
        conn.execute(f'CREATE TABLE "{table}" ({cols_sql})')

        placeholders = ", ".join(["?"] * len(header))
        insert_sql = f'INSERT INTO "{table}" VALUES ({placeholders})'

        conn.executemany(
            insert_sql,
            [normalize_row(r, len(header)) for r in preview],
        )

        batch: list[list[str]] = []
        for r in reader:
            batch.append(normalize_row(r, len(header)))
            if len(batch) >= 5_000:
                conn.executemany(insert_sql, batch)
                batch.clear()

        if batch:
            conn.executemany(insert_sql, batch)

    conn.commit()
    count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    print(f"  -> {count:,} rows")


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    tsv_files = sorted(DATA_DIR.glob("*.tsv"))
    if not tsv_files:
        raise RuntimeError(f"No .tsv files found in {DATA_DIR}")

    conn = sqlite3.connect(DB_PATH)
    try:
        for path in tsv_files:
            load_tsv(conn, path)
    finally:
        conn.close()

    print(f"\nCreated SQLite DB at {DB_PATH.resolve()}")


if __name__ == "__main__":
    main()
