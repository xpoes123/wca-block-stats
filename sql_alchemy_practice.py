from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///wca.db", future=True)

checks = [
    # results -> persons
    ("results.person_id -> persons.wca_id",
     "SELECT COUNT(*) AS missing "
     "FROM results r LEFT JOIN persons p ON r.person_id = p.wca_id "
     "WHERE r.person_id IS NOT NULL AND p.wca_id IS NULL"),
    # results -> competitions
    ("results.competition_id -> competitions.id",
     "SELECT COUNT(*) AS missing "
     "FROM results r LEFT JOIN competitions c ON r.competition_id = c.id "
     "WHERE c.id IS NULL"),
    # results -> events
    ("results.event_id -> events.id",
     "SELECT COUNT(*) AS missing "
     "FROM results r LEFT JOIN events e ON r.event_id = e.id "
     "WHERE e.id IS NULL"),
    # result_attempts -> results
    ("result_attempts.result_id -> results.id",
     "SELECT COUNT(*) AS missing "
     "FROM result_attempts a LEFT JOIN results r ON a.result_id = r.id "
     "WHERE r.id IS NULL"),
]

with engine.connect() as conn:
    for name, sql in checks:
        missing = conn.execute(text(sql)).scalar_one()
        print(f"{name}: missing={missing}")
