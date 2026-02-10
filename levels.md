Level 1 — Warm-up (Schema fluency)
1️⃣ How many rows are in each table?

Goal: get comfortable with reflection + iteration.

Tables: all

Use inspect(engine).get_table_names()

Use SELECT COUNT(*) per table

Gotcha: don’t hardcode table names
Success: you can print something like:

results: 7,843,212
persons: 198,431
...

2️⃣ How many distinct competitors are in results?

Business question:
“How many unique people have ever recorded a result?”

Tables: results

Columns: person_id

Use COUNT(DISTINCT ...)

Gotcha: COUNT(*) ≠ COUNT(DISTINCT ...)
Success: single scalar result you trust

Level 2 — Core joins & aggregates (very Ramp)
3️⃣ Top 10 competitors by number of results

Business question:
“Who has competed the most?”

Tables: results, persons

Join: results.person_id == persons.wca_id

Aggregate: COUNT(*)

Order by count desc

Limit 10

Gotchas:

join on the correct key (wca_id, not name)

group by every non-aggregated column

Success: sensible names + large counts

4️⃣ Number of competitions per country

Business question:
“Which countries host the most competitions?”

Tables: competitions, countries

Join: competitions.country_id == countries.id

Aggregate: COUNT(*)

Group by country

Gotcha: competitions table, not results
Success: top countries match intuition (USA, etc.)

Level 3 — Correctness under ambiguity (this is big at Ramp)
5️⃣ Events with the most DNFs

Business question:
“Which events are hardest (most DNFs)?”

Tables: results, events

Filter: results.best == -1

Group by event

Order by count desc

Gotchas:

DNF is encoded as -1

Don’t accidentally include average

Success: events like 333bf / mbf appear high

6️⃣ Percentage of DNFs per event

Business question:
“What fraction of attempts result in DNF, by event?”

Tables: results, events

Compute:

dnf_count / total_count


Use CASE WHEN inside SUM(...)

Gotchas:

integer division (cast to float!)

denominator must be all results, not filtered

Success: fractions between 0 and 1 that make sense

Level 4 — Multi-table reasoning (FDE tier)
7️⃣ For a given competitor, list their best average per event

Business question:
“What are this person’s strongest events?”

Tables: results, events

Filter: person_id == "<some wca_id>"

Use MIN(results.average)

Exclude average == 0

Gotchas:

averages of 0 mean “not applicable”

some events don’t have averages

Success: clean list, one row per event

8️⃣ Competition with the most total solves

Business question:
“Which competition had the most total attempts?”

Tables: results, competitions, result_attempts

Join chain:

competitions → results → result_attempts


Count attempts

Gotchas:

join explosion if you group incorrectly

verify row counts before trusting result

Success: result looks like Worlds / large comps

Level 5 — Explainability & validation (very Ramp-specific)
9️⃣ Find results that reference missing persons (again, but generalized)

Business question:
“Are there any broken references in our core fact table?”

Generalize your earlier check

Return examples, not just counts

Limit 10 rows

Gotchas:

must use LEFT JOIN

must filter on NULL parent keys

Success: either zero rows or explainable edge cases

🔟 Pick one aggregate and validate it two ways

Example:

count total results via:

COUNT(*) FROM results

sum of counts grouped by competition

Business question:
“Do these two independent calculations agree?”

Gotcha: this is about trust, not syntax
Success: same number (or you understand why not)