# Bundesliga 2026/27 dashboard

Standalone, mobile-first Bundesliga-only dashboard. It does not include Brasileirão Série A or Premier League data.

## Data snapshot

- Results/table cutoff: 18 October 2026, 10:52 America/Sao_Paulo.
- Full fixture schedule: all 34 rounds / 306 official pairings from Bundesliga matchday pages; the pages for matchdays 8–34 were retrieved 10:59–11:00 BRT on 18 October.
- Final scores: 52 confirmed results (rounds 1–5 and seven completed matches in round 6). Two round-6 matches on 18 October are explicitly unfinished at the result cutoff and have no score recorded.
- Future results are never inferred. The source only publishes date ranges for several rounds; those are preserved as ranges, and no precise date is guessed. Rounds 16 and 24 have no date in the snapshots used.
- The Bundesliga table is recomputed from confirmed finals and compared club-by-club with the Bundesliga official table and ESPN's independent 2026/27 table. The seven completed round-6 scorelines are also spot-checked against Sofascore.

## Dashboard features

Standings, current form, last five completed games, home/away splits, next fixture, season H2H, 1-X-2/goal projection from a simple Poisson model, BTTS and over-2.5 estimates, overall/home/away top-five rankings, source links, cutoff, method, and explicit limitations.

The 1-X-2, expected-goals, modal-score, BTTS and over-2.5 figures are projections based only on small early-season samples, not confirmed match facts or betting advice.

## Sources

See `bundesliga_2026_27_sources_validation.json` for source links, scope, cutoff and validation. Primary source: [Bundesliga official fixtures and table](https://www.bundesliga.com/en/bundesliga/matchday). Independent checks: [Sofascore](https://www.sofascore.com/football/tournament/germany/bundesliga/35) and [ESPN standings](https://www.espn.com/soccer/standings/_/league/ger.1).

`index.html` is self-contained. The CSV preserves the schedule/results rows and the JSON documents sources, cutoff, rules and validation.
