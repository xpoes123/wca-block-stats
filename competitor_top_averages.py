from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import Session
from models import Person, Result, Competition, Country, Event, RoundType

engine = create_engine("sqlite:///wca.db", future=True)

WCA_ID = "2016JIAN13"

# Goal here is to find PR averages for a user with subquery
with Session(engine) as session:
    # Subquery acts as a sort of filiter.
    row_number = func.row_number().over(
        partition_by=Result.event_id,
        order_by=[
            Result.average.asc(),
            Competition.start_date.desc(),
            Result.id.desc(),  # tie-breaker for determinism
        ],
    )

    ranked_subq = (
        select(
            Result.id.label("result_id"),
            row_number.label("rn"),
        )
        .join(Competition, Result.competition_id == Competition.id)
        .where(
            Result.person_id == WCA_ID,
            Result.average > 0,
        )
        .subquery()
    )

    pr_rows = session.execute(
        select(Result)
        .join(ranked_subq, Result.id == ranked_subq.c.result_id)
        .where(ranked_subq.c.rn == 1)
        .order_by(Result.event_id)
    ).scalars().all()

    for r in pr_rows:
        print(r.person_id, r.event_id, r.average, r.competition_id)
