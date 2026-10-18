#!/usr/bin/env python3
"""Deterministically validate the Bundesliga 2026/27 CSV and build its static dashboard.

Inputs (same directory):
  - bundesliga_2026_27_results_verified.csv
  - bundesliga_2026_27_sources_validation.json
  - bundesliga_2026_27_dashboard_template.html

This script performs no network access and never changes the source CSV or metadata.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "bundesliga_2026_27_results_verified.csv"
META_PATH = ROOT / "bundesliga_2026_27_sources_validation.json"
TEMPLATE_PATH = ROOT / "bundesliga_2026_27_dashboard_template.html"
OUT_PATH = ROOT / "bundesliga_2026_27_dashboard.html"

with CSV_PATH.open(newline="", encoding="utf-8") as f:
    raw_rows = list(csv.DictReader(f))
with META_PATH.open(encoding="utf-8") as f:
    meta = json.load(f)
template = TEMPLATE_PATH.read_text(encoding="utf-8")
if "__DATA__" not in template or "__META__" not in template:
    raise ValueError("Dashboard template is missing its JSON placeholders")
if not raw_rows:
    raise ValueError("Source CSV is empty")

required = {"round", "date", "date_range", "date_label", "kickoff_time", "timezone", "home", "away", "home_goals", "away_goals", "status", "official_match_url"}
missing = required - set(raw_rows[0])
if missing:
    raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

rows = []
valid_status = {"finished", "unfinished_at_cutoff", "scheduled"}
for source in raw_rows:
    r = dict(source)
    r["round"] = int(r["round"])
    if r["round"] < 1 or r["round"] > 34:
        raise ValueError(f"Invalid round number: {r['round']}")
    if not r["home"] or not r["away"] or r["home"] == r["away"]:
        raise ValueError(f"Invalid club pairing: {r}")
    if r["status"] not in valid_status:
        raise ValueError(f"Invalid status {r['status']!r}")
    if r["status"] == "finished":
        if r["home_goals"] == "" or r["away_goals"] == "":
            raise ValueError(f"Finished match lacks a confirmed score: {r}")
        r["home_goals"] = int(r["home_goals"])
        r["away_goals"] = int(r["away_goals"])
        if min(r["home_goals"], r["away_goals"]) < 0:
            raise ValueError(f"Negative score: {r}")
    elif r["home_goals"] != "" or r["away_goals"] != "":
        raise ValueError(f"Non-final match must not have a score: {r}")
    rows.append(r)

clubs = sorted({r["home"] for r in rows} | {r["away"] for r in rows})
if len(clubs) != 18:
    raise ValueError(f"Expected 18 Bundesliga clubs, found {len(clubs)}")
if len(rows) != 306 or meta.get("coverage", {}).get("official_fixtures") != len(rows):
    raise ValueError(f"Expected 306 official fixture rows; found {len(rows)}")
if len(meta.get("standings_snapshot", [])) != 18:
    raise ValueError("Metadata must contain the official 18-club table snapshot")

fixture_keys = set()
for r in rows:
    key = (r["round"], r["home"], r["away"])
    if key in fixture_keys:
        raise ValueError(f"Duplicate fixture key: {key}")
    fixture_keys.add(key)
for rnd in range(1, 35):
    fixtures = [r for r in rows if r["round"] == rnd]
    if len(fixtures) != 9:
        raise ValueError(f"Round {rnd} has {len(fixtures)} fixtures instead of 9")
    appearances = [r["home"] for r in fixtures] + [r["away"] for r in fixtures]
    if Counter(appearances) != Counter(clubs):
        raise ValueError(f"Round {rnd} does not contain each club exactly once")
for club in clubs:
    if sum(r["home"] == club for r in rows) != 17 or sum(r["away"] == club for r in rows) != 17:
        raise ValueError(f"{club} must have exactly 17 home and 17 away fixtures")

# Compute the live table exclusively from rows marked finished.
stats = {club: {"MP": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "Pts": 0} for club in clubs}
finished = []
for r in rows:
    if r["status"] != "finished":
        continue
    finished.append(r)
    h, a = stats[r["home"]], stats[r["away"]]
    hg, ag = r["home_goals"], r["away_goals"]
    h["MP"] += 1; a["MP"] += 1
    h["GF"] += hg; h["GA"] += ag; a["GF"] += ag; a["GA"] += hg
    if hg > ag:
        h["W"] += 1; a["L"] += 1; h["Pts"] += 3
    elif hg < ag:
        a["W"] += 1; h["L"] += 1; a["Pts"] += 3
    else:
        h["D"] += 1; a["D"] += 1; h["Pts"] += 1; a["Pts"] += 1

ordered = sorted(clubs, key=lambda c: (-stats[c]["Pts"], -(stats[c]["GF"] - stats[c]["GA"]), -stats[c]["GF"], c))
computed = []
for pos, club in enumerate(ordered, 1):
    s = stats[club]
    computed.append({"club": club, "position": pos, **s, "GD": s["GF"] - s["GA"]})
source_table = meta["standings_snapshot"]
if computed != source_table:
    raise ValueError("Results-derived standings do not match the saved official table snapshot")
if meta.get("independent_table_matches_official") is not True:
    raise ValueError("Independent ESPN table cross-check is not marked as passed in metadata")
if meta.get("coverage", {}).get("final_results") != len(finished):
    raise ValueError("Confirmed final count in metadata does not match CSV")

# Keep source records in round/date order; blank dates remain blank rather than inferred.
rows.sort(key=lambda r: (r["round"], r["date"] or r["date_range"], r["home"]))
data_json = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
meta_json = json.dumps(meta, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = template.replace("__DATA__", data_json).replace("__META__", meta_json)
OUT_PATH.write_text(page, encoding="utf-8")

print(json.dumps({
    "output": str(OUT_PATH),
    "fixtures": len(rows),
    "confirmed_results": len(finished),
    "clubs": len(clubs),
    "rounds": 34,
    "table_validation": "PASS: all 18 computed standings rows match the saved official Bundesliga table snapshot; independent ESPN cross-check recorded",
    "network_access": False
}, ensure_ascii=False, indent=2))
