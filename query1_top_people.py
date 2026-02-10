from sqlalchemy import create_engine, MetaData, Table, select, func, case

engine = create_engine("sqlite:///wca.db", future=True)
md = MetaData()

results = Table("results", md, autoload_with=engine)
persons = Table("persons", md, autoload_with=engine)
countries = Table("countries", md, autoload_with=engine)
competitions = Table("competitions", md, autoload_with=engine)
events = Table("events", md, autoload_with=engine)

# # Step 1
# results_count_stmt = (
#     select(
#         func.count().label("count")
#     )
#     .select_from(
#         results
#     )
# )

# persons_count_stmt = (
#     select(
#         func.count().label("count")
#     )
#     .select_from(
#         persons
#     )
# )

# countries_count_stmt = (
#     select(
#         func.count().label("count")
#     )
#     .select_from(
#         countries
#     )
# )

# with engine.connect() as conn:
#     results_rows = conn.execute(results_count_stmt).scalar_one()
#     countries_rows = conn.execute(countries_count_stmt).scalar_one()
#     persons_rows = conn.execute(persons_count_stmt).scalar_one()
    
# print(f"results: {results_rows}")
# print(f"countries: {countries_rows}")
# print(f"persons: {persons_rows}")

# # Level 2
# stmt_2 = (
#     select(
#         results.c.person_id,
#         persons.c.name.label("person_name"),
#         func.count().label("times_competed"),
#     )
#     .select_from(
#         results.join(persons, results.c.person_id == persons.c.wca_id)
#     )
#     .group_by(results.c.person_id, persons.c.name)
#     .order_by(func.count().desc())
#     .filter(results.c.person_id == "2016JIAN13")
# )

# stmt_2b = (
#     select(
#         func.count(func.distinct(results.c.competition_id)).label("distinct_competitions")
#     )
# )

# with engine.connect() as conn:
#     most_comps = conn.execute(stmt_2).all()
#     comp_count = conn.execute(stmt_2b).scalar_one()

# for r in most_comps:
#     print(r)

# print(f"Num Comps: {comp_count}")

# # Number of competitions per country

# stmt_2c = (
#     select(
#         countries.c.name.label("Country"),
#         func.count(func.distinct(competitions.c.id)).label("num_comps"),
#     )
#     .select_from(
#         results
#         .join(competitions, results.c.competition_id == competitions.c.id)
#         .join(countries, competitions.c.country_id == countries.c.id)
#     )
#     .group_by(countries.c.name)
#     .order_by(func.count(func.distinct(competitions.c.id)).desc())
#     .limit(10)
# )


# with engine.connect() as conn:
#     comps = conn.execute(stmt_2c).all()

# for comp in comps:
#     print(comp)


# # Level 3
# # Events by most DNF averages
# dnfs = func.sum(
#     case((results.c.best == -1, 1), else_=0)
# ).label("dnfs")
# total = func.count(results.c.id).label("total")
# stmt_4a = (
#     select(
#         events.c.name,
#         dnfs,
#         (dnfs / total).label("dnf_rate")
#     )
#     .select_from(
#         results.join(events, results.c.event_id == events.c.id)
#     )
#     .group_by(events.c.name)
#     .order_by((dnfs / total).desc())
# )

# with engine.connect() as conn:
#     event_rows = conn.execute(stmt_4a).all()

# for event in event_rows:
#     print(event)

# Take in an ID and get their best results
# stmt_4b = (
#     select(
#         persons.c.name,
#         events.c.id,
#         func.min(results.c.average)
#     )
#     .select_from(
#         results.join(persons, results.c.person_id == persons.c.wca_id)
#                 .join(events, results.c.event_id == events.c.id)
#     )
#     .group_by(persons.c.wca_id, events.c.id)
#     .where(persons.c.wca_id == "2016JIAN13", results.c.average > 0)
# )

# with engine.connect() as conn:
#     person_rows = conn.execute(stmt_4b).all()

# for person in person_rows:
#     print(person)

stmt_4c = (
    select(
        competitions.c.id,
        func.count().label("results")
    )
    .select_from(
        results.join(competitions, results.c.competition_id == competitions.c.id)
    )
    .group_by(results.c.competition_id)
    .where(results.c.best != -1)
    .order_by(func.count().desc())
    .limit(10)
)

with engine.connect() as conn:
    comps = conn.execute(stmt_4c).all()

for comp in comps:
    print(comp)