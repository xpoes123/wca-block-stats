# wca-block-stats

A tool for querying WCA (World Cube Association) competition data without writing SQL.

## Goal

Build an interactive app where users can look up cubing stats through a visual, block-style query builder backed by SQLAlchemy.

## Setup

Requires Python 3.14+ and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

You'll need to download the [WCA database export](https://www.worldcubeassociation.org/export/results) and place the TSV files in a `data/` directory, then run:

```bash
uv run python load_wca_sqlite.py
```

This creates `wca.db` locally (not committed due to size).
