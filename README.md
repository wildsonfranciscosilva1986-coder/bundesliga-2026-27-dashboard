# Bundesliga 2026/27 dashboard

Standalone, mobile-first Bundesliga-only dashboard. It does not include Brasileirão Série A or Premier League data.

## Data snapshot

- Results/table cutoff: 19 October 2026, 08:16 America/Sao_Paulo.
- Current DFL table and Matchday 6 result snapshot: 19 October 2026, 08:16 BRT.
- Full fixture schedule: all 34 rounds / 306 official pairings from Bundesliga matchday pages; snapshots for matchdays 8–34 were retrieved 19 October 2026, 10:59–11:00 BRT.
- Final scores: 54 confirmed results through the complete round 6; all 9 round-6 fixtures are final.
- Future results are never inferred. The source publishes date ranges for several rounds; those are preserved as ranges, and no precise date is guessed. Rounds 16 and 24 have no date in the snapshots used.
- Kickoff times are copied exactly from official fixture cards, but the captured cards do not label a timezone, so the dashboard labels them as source times rather than converting them.
- The Bundesliga table is recomputed from confirmed finals and matches the current official DFL table for all 18 clubs; ESPN standings independently match all 18. ESPN match-report checks confirm only the two Sunday round-6 results; earlier result checks against Sofascore remain.

## Dashboard features

Standings, current form, last five completed games, home/away splits, next fixture, season H2H, 1-X-2/goal projection from a simple Poisson model, BTTS and over-2.5 estimates, overall/home/away top-five rankings, source links, cutoff, method, and explicit limitations.

The 1-X-2, expected-goals, modal-score, BTTS and over-2.5 figures are projections based only on small early-season samples, not confirmed match facts or betting advice.

## Sources

See `bundesliga_2026_27_sources_validation.json` for source links, scope, cutoff and validation. Primary source: [Bundesliga official fixtures and table](https://www.bundesliga.com/en/bundesliga/matchday). Independent checks: [Sofascore](https://www.sofascore.com/football/tournament/germany/bundesliga/35) and [ESPN standings](https://www.espn.com/soccer/standings/_/league/ger.1).

`index.html` is self-contained. The CSV preserves the schedule/results rows and the JSON documents sources, cutoff, rules and validation.

## Overview and league rules

The overview shows 18 clubs, completed/total fixtures, total and mean goals, BTTS and over-2.5 numerator/denominator/rates, home wins/draws/away wins, and the exact result/table cutoff. The overview also includes upcoming fixtures. European qualification zones reflect the confirmed official 2026/27 allocation (places 1–4 Champions League, 5–6 Europa League, 7 Conference League qualifying); the relegation zone reflects the official two-leg playoff for 16th and direct relegation for 17th–18th. Sources and nuance are recorded in the JSON and validation record.

## Deterministic rebuild and validation

All dashboard refresh inputs and artifacts are kept in this repository:

- `bundesliga_2026_27_results_verified.csv` — official fixtures and only confirmed final scores.
- `bundesliga_2026_27_sources_validation.json` — source snapshots, exact cutoff, rules and standings validation data.
- `bundesliga_2026_27_dashboard_template.html` — responsive, self-contained dashboard template.
- `build_bundesliga_2026_dashboard.py` — deterministic offline validator and builder (standard Python only).
- `bundesliga_2026_27_dashboard.html` / `index.html` — generated dashboard (self-contained page).
- `bundesliga_2026_27_validation.txt` — readable validation, sources and refresh procedure.

Run `python3 build_bundesliga_2026_dashboard.py` from the repository root after updating source data and validation metadata. The build is intentionally offline and fails closed if fixture coverage, score/status consistency, league table computation or the independent table-check flag fails. Review and update the validation record, then replace `index.html` with the generated `bundesliga_2026_27_dashboard.html` before publishing. No scheduled refresh/cron is configured.
