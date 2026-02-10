from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import Session, selectinload
from models import Person, Result, Competition, Country, Event, RoundType 

engine = create_engine("sqlite:///wca.db", future=True)

WCA_ID = "2016JIAN13"

with Session(engine) as session:
    recent_comp_id = session.execute(
        select(Competition.id)
        .join(Result)
        .where(Result.person_id == WCA_ID)
        .order_by(Competition.start_date.desc())
        .limit(1)
    ).scalars().one()
    print(recent_comp_id)
    
    max_round_subq = (
        select(
            Result.event_id.label("event_id"),
            func.max(RoundType.rank).label("max_rank")
        )
        .join(RoundType, Result.round_type_id == RoundType.id)
        .where(
            Result.person_id == WCA_ID,
            Result.competition_id == recent_comp_id,
        )
        .group_by(Result.event_id)
        .subquery()
    )
    
    final_results = session.execute(
        select(Result)
        .join(RoundType, Result.round_type_id == RoundType.id)
        .join(
            max_round_subq,
            (Result.event_id == max_round_subq.c.event_id)
            & (RoundType.rank == max_round_subq.c.max_rank)
        )
        .where(
            Result.person_id == WCA_ID,
            Result.competition_id == recent_comp_id
        )
    ).scalars().all()
    
    for r in final_results:
        print(
            r.event_id,
            r.average,
            r.best,
            r.round_type.name
        )