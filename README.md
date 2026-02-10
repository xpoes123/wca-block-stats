# wca-block-stats

A tool for querying WCA (World Cube Association) competition data without writing SQL.

## Goal

Build an interactive app where users can look up cubing stats through a visual, block-style query builder. Users pick entities, filters, groupings, and metrics — the backend translates that into correct, performant SQLAlchemy queries.

## Status

**Currently building the query engine backend.**

- [x] ORM models for the WCA schema (Person, Result, Competition, Event, Country, RoundType)
- [x] Query spec dataclasses — a typed DSL that represents what the user wants to query
- [x] Error types for validation and internal invariant failures
- [ ] Query compiler (spec → SQLAlchemy select)
- [ ] Flask API layer
- [ ] Frontend query builder

## Project Structure

```
models.py              # SQLAlchemy ORM models
query_engine/
  spec.py              # QuerySpec, FieldRef, FilterExpr, TopPerGroupSpec
  errors.py            # QuerySpecError, ValidationError, InvariantError
```

## Setup

Requires Python 3.14+ and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

Download the [WCA database export](https://www.worldcubeassociation.org/export/results), place the TSV files in a `data/` directory, and load them into SQLite. This creates `wca.db` locally (not committed due to size).
