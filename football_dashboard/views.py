# =====================================================================
# football_dashboard/views.py
# WHAT THIS DOES: reads the pipeline's saved files from the app's data/
#   folder and sends them to the template. The only calculation is
#   counting player positions into a grid for the heat maps; everything
#   else shown comes straight from the files the notebook wrote.
# FILES NEEDED in football_dashboard/data/:
#   match_facts_v3.json, coach_notes_v2.md, player_stats_final_v9.csv,
#   positions_final_v9.csv  (Steps 2-3: the moving pitch and the heat maps)
#   Step 4 uses player_stats_final_v9.csv and the events in match_facts_v3.json
# =====================================================================
import csv
import html
import json
import re
from functools import lru_cache
from pathlib import Path

from django.shortcuts import render

DATA = Path(__file__).resolve().parent / "data"      # the data folder inside this app


@lru_cache(maxsize=1)                                # read each file once, reuse afterwards
def load_facts():
    with open(DATA / "match_facts_v3.json", encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def load_notes():
    return (DATA / "coach_notes_v2.md").read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def load_player_stats():
    with open(DATA / "player_stats_final_v9.csv", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fmt(v):
    """Show numbers with at most 1 decimal; leave text alone."""
    try:
        x = float(v)
        return str(int(x)) if x == int(x) else "%.1f" % x
    except (TypeError, ValueError):
        return "" if v is None else str(v)


def notes_to_html(md):
    """Tiny markdown converter for our notes: **bold**, '- ' bullets, paragraphs."""
    out, in_list = [], False
    for line in md.splitlines():
        line = html.escape(line.strip())                         # escape first so nothing can inject HTML
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>%s</li>" % line[2:])
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            if line:
                out.append("<p>%s</p>" % line)
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def pick(cols, *names):
    """Return the first column name from names that exists in cols (else None)."""
    return next((n for n in names if n in cols), None)


def team_of(chain, given=None):
    """Team from a team column if there is one, else from the chain name (W.. / GKW.. = white, L.. / GKL.. = lime)."""
    if given in ("white", "lime"):
        return given
    c = chain.upper()
    if c.startswith("GKW") or c.startswith("W"):
        return "white"
    if c.startswith("GKL") or c.startswith("L"):
        return "lime"
    return "other"


def read_positions():
    """Read positions_final_v9.csv. Returns (list of (chain, step, x, y, team), message).
    Rows flagged as outliers or with empty positions are skipped."""
    path = DATA / "positions_final_v9.csv"
    if not path.exists():
        return None, "positions_final_v9.csv is not in the data folder."
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return None, "positions_final_v9.csv is empty."
    cols = rows[0].keys()
    cx, cy = pick(cols, "x_m", "x"), pick(cols, "y_m", "y")
    cc, cs, ct = pick(cols, "chain", "player", "id"), pick(cols, "step"), pick(cols, "team")
    if not (cx and cy and cc and cs):
        return None, "Could not find the position columns. Columns in the file: " + ", ".join(cols)
    out = []
    for r in rows:
        if r.get("outlier", "").strip().lower() in ("true", "1"):  # skip positions the pipeline flagged as outliers
            continue
        try:
            step, x, y = int(float(r[cs])), float(r[cx]), float(r[cy])
        except (ValueError, TypeError):
            continue                                              # empty cell: no position for this step
        out.append((r[cc], step, x, y, team_of(r[cc], r.get(ct) if ct else None)))
    return out, ""


def load_tracks(pos):
    """Positions grouped by step for the animated pitch."""
    frames = {}                                                   # step -> {"white": [(chain, x, y)], "lime": [...]}
    for chain, step, x, y, t in pos:
        frames.setdefault(step, {"white": [], "lime": [], "other": []})[t].append((chain, round(x, 2), round(y, 2)))
    out = []
    for step in sorted(frames):
        fr = frames[step]
        out.append({
            "t": round(step * 0.12, 2),                           # 1 step = 3 video frames = 0.12 s
            **{t: {"c": [p[0] for p in fr[t]], "x": [p[1] for p in fr[t]], "y": [p[2] for p in fr[t]]} for t in ("white", "lime")},
        })
    return out


CELL = 5.0                                                        # heat map cell size in metres
NX, NY = 21, 14                                                   # 105 m / 5 = 21 columns, 68 m / 5 = 13.6 -> 14 rows


def load_heat(pos):
    """For each team: share (%) of its tracked player-steps that fall in each 5 m x 5 m cell.
    A player-step is one player at one step; a player is counted only when he is tracked."""
    counts = {t: [[0] * NX for _ in range(NY)] for t in ("white", "lime")}
    totals = {"white": 0, "lime": 0}
    for chain, step, x, y, t in pos:
        if t not in counts or not (0 <= x <= 105 and 0 <= y <= 68):   # ignore anything outside the pitch
            continue
        i, j = min(int(y // CELL), NY - 1), min(int(x // CELL), NX - 1)
        counts[t][i][j] += 1
        totals[t] += 1
    z = {t: [[round(100.0 * c / totals[t], 2) if totals[t] else 0 for c in row] for row in counts[t]] for t in counts}
    return {
        "z": z,
        "x": [round(CELL * (j + 0.5), 2) for j in range(NX)],     # cell centres in metres
        "y": [round(min(CELL * (i + 0.5), 68 - 0.5), 2) if i < NY - 1 else round((CELL * (NY - 1) + 68) / 2, 2) for i in range(NY)],
        "zmax": max(max(max(r) for r in z[t]) for t in z),
        "n": totals,
    }


def num(v):
    """Float or None (empty or text cells become None)."""
    try:
        x = float(v)
        return x if x == x else None                              # x == x is False for NaN
    except (TypeError, ValueError):
        return None


def load_player_charts(stats):
    """Per-player numbers for the bar charts from player_stats_final_v9.csv. Returns (list, message)."""
    if not stats:
        return None, "player_stats_final_v9.csv is empty."
    cols = stats[0].keys()
    cc = pick(cols, "chain", "player", "id")
    cd, ch, ctop = pick(cols, "dist_m", "distance_m"), pick(cols, "hsr_m"), pick(cols, "top_kmh")
    cok, ct = pick(cols, "top_ok"), pick(cols, "team")
    if not (cc and cd and ch and ctop):
        return None, "Could not find the stats columns. Columns in the file: " + ", ".join(cols)
    out = []
    for r in stats:
        out.append({
            "chain": r[cc],
            "team": team_of(r[cc], r.get(ct) if ct else None),
            "dist": num(r[cd]), "hsr": num(r[ch]), "top": num(r[ctop]),
            "top_ok": (r.get(cok, "").strip().lower() in ("true", "1")) if cok else False,   # top speed trusted only if tracked cleanly long enough
        })
    return out, ""


EVENT_KINDS = ("pass", "contested", "turnover", "carry")          # names in the events list start with these


def load_event_points(f):
    """Events for the timeline: time, lane (team), kind, who, confidence."""
    out = []
    for e in sorted(f.get("events", []), key=lambda e: e["t_s"]):
        kind = next((k for k in EVENT_KINDS if str(e["event"]).startswith(k)), "other")
        out.append({
            "t": e["t_s"], "team": e.get("team_from"), "kind": kind, "name": e["event"],
            "from": e.get("from"), "to": e.get("to"), "ball": e.get("ball_m"), "conf": e.get("confidence"),
        })
    return out

STEP_S = 0.12                                                     # 1 step = 3 video frames = 0.12 s


def load_control_seconds():
    """Seconds each player was the nearest player to a slow ball while a team had it (from ball_possession_v2.csv).
    Returns {chain: seconds}, or None if the file or its columns are not as expected."""
    path = DATA / "ball_possession_v2.csv"
    if not path.exists():
        return None
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or not {"chain", "status"} <= set(rows[0].keys()):
        return None
    secs = {}
    for r in rows:
        chain = (r.get("chain") or "").strip()
        if r["status"] in ("white", "lime") and chain and chain.lower() != "nan":
            secs[chain] = secs.get(chain, 0) + STEP_S
    return secs


def load_player_table(stats, f):
    """One row per player: movement from the stats file, ball control from the possession file,
    and pass / duel / turnover counts from the events. Counts come from the events list as it stands."""
    if not stats:
        return None
    cols = stats[0].keys()
    cc = pick(cols, "chain", "player", "id")
    cd, ch, cs = pick(cols, "dist_m", "distance_m"), pick(cols, "hsr_m"), pick(cols, "sprint_m")
    ctop, cok, cclean = pick(cols, "top_kmh"), pick(cols, "top_ok"), pick(cols, "clean_s")
    ct = pick(cols, "team")
    if not (cc and cd):
        return None
    control = load_control_seconds()
    counts = {}                                                   # chain -> counts of events involving him
    for e in f.get("events", []):
        kind = str(e["event"])
        who_from, who_to = e.get("from"), e.get("to")
        c = lambda ch_: counts.setdefault(ch_, {"made": 0, "recv": 0, "duel": 0, "lost": 0})
        if kind.startswith("pass"):
            if who_from: c(who_from)["made"] += 1
            if who_to: c(who_to)["recv"] += 1
        elif kind.startswith("contested"):
            for w in (who_from, who_to):
                if w: c(w)["duel"] += 1
        elif kind.startswith("turnover") and who_from:
            c(who_from)["lost"] += 1                              # the player who lost it
    rows = []
    for r in stats:
        chain = r[cc]
        n = counts.get(chain, {"made": 0, "recv": 0, "duel": 0, "lost": 0})
        rows.append({
            "chain": chain, "team": team_of(chain, r.get(ct) if ct else None),
            "dist": fmt(r[cd]), "hsr": fmt(r[ch]) if ch else "", "sprint": fmt(r[cs]) if cs else "",
            "top": fmt(r[ctop]) if ctop else "", "top_ok": (r.get(cok, "").strip().lower() in ("true", "1")) if cok else False,
            "clean": fmt(r[cclean]) if cclean else "",
            "control": ("%.1f" % control.get(chain, 0.0)) if control is not None else "-",
            "made": n["made"], "recv": n["recv"], "duel": n["duel"], "lost": n["lost"],
            "_sort": (0 if team_of(chain, r.get(ct) if ct else None) == "white" else 1, -(num(r[cd]) or 0)),
        })
    rows.sort(key=lambda x: x["_sort"])                           # white first, then lime, each by distance
    return rows



def dashboard(request):
    f = load_facts()
    totals = f.get("team_totals_lower_bounds", {})                # {team: {metric: value}}
    metrics = sorted({m for t in totals.values() for m in t})
    team_rows = [{"metric": m, "values": [fmt(totals[t].get(m)) for t in totals]} for m in metrics]
    events = [{k: fmt(e.get(k)) for k in ("t_s", "event", "team_from", "from", "to", "ball_m", "progress_m", "confidence")}
              for e in sorted(f.get("events", []), key=lambda e: e["t_s"])]
    stats = load_player_stats()
    players, players_msg = load_player_charts(stats)
    pos, tracks_msg = read_positions()                            # read the positions file once for both charts
    return render(request, "football_dashboard/dashboard.html", {
        "tracks": load_tracks(pos) if pos else None,
        "heat": load_heat(pos) if pos else None,
        "tracks_msg": tracks_msg,
        "players": players,
        "players_msg": players_msg,
        "event_points": load_event_points(f),
        "player_table": load_player_table(stats, f),
        "teams": list(totals),
        "team_rows": team_rows,
        "events": events,
        "notes_html": notes_to_html(load_notes()),
        "stat_cols": list(stats[0].keys()) if stats else [],
        "stat_rows": [[fmt(v) for v in r.values()] for r in stats],
    })