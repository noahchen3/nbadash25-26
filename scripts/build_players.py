"""Merge Basketball-Reference per-game, per-100 and advanced player tables into data/players_2025_26.js."""
import re, sys, json, html

raw, out = sys.argv[1], sys.argv[2]
MIN_MP = 100  # players below this are left out entirely; percentile pools use a higher cutoff in the page

def rows(name, table_id):
    t = open(f"{raw}/players_{name}.html", encoding="utf-8").read().replace("<!--", "").replace("-->", "")
    t = t[t.find(f'id="{table_id}"'):]
    t = t[:t.find("</table>")]
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        m = re.search(r'data-append-csv="([^"]+)"', row)
        if not m:
            continue
        cells = {k: html.unescape(re.sub("<[^>]+>", "", v)).strip()
                 for k, v in re.findall(r'data-stat="([a-z0-9_]+)"[^>]*>(.*?)</t[dh]>', row)}
        yield m.group(1), cells

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

players = {}
for name, tid in [("per_game", "per_game_stats"), ("per_poss", "per_poss"), ("advanced", "advanced")]:
    seen = set()
    for pid, c in rows(name, tid):
        team = c.get("team_name_abbr", "")
        p = players.setdefault(pid, {"id": pid, "name": c["name_display"], "pos": c.get("pos", ""), "age": num(c.get("age")), "teams": []})
        if pid in seen:  # later rows are the per-team splits of a traded player
            if name == "per_game" and team:
                p["teams"].append(team)
            continue
        seen.add(pid)
        if name == "per_game" and not re.match(r"\dTM", team):
            p["teams"].append(team)
        p[name] = c

KEEP = {
    "per_game": ["games", "games_started", "mp_per_g", "pts_per_g", "trb_per_g", "ast_per_g", "stl_per_g", "blk_per_g", "tov_per_g",
                 "fg_pct", "fg3_pct", "ft_pct", "efg_pct", "fg3a_per_g", "fta_per_g"],
    "per_poss": ["mp", "pts_per_poss", "trb_per_poss", "ast_per_poss", "stl_per_poss", "blk_per_poss", "tov_per_poss", "fg3a_per_poss", "fta_per_poss", "off_rtg", "def_rtg"],
    "advanced": ["per", "ts_pct", "fg3a_per_fga_pct", "fta_per_fga_pct", "orb_pct", "drb_pct", "trb_pct", "ast_pct", "stl_pct", "blk_pct",
                 "tov_pct", "usg_pct", "ws", "ws_per_48", "obpm", "dbpm", "bpm", "vorp"],
}
outp = []
for p in players.values():
    if not all(k in p for k in KEEP):
        continue
    s = {}
    for table, keys in KEEP.items():
        for k in keys:
            s[k] = num(p[table].get(k))
    if (s["mp"] or 0) < MIN_MP:
        continue
    # season attempt totals, used for shooting-percentage volume cutoffs
    s["fg3a_tot"] = round((s["fg3a_per_g"] or 0) * (s["games"] or 0))
    s["fta_tot"] = round((s["fta_per_g"] or 0) * (s["games"] or 0))
    outp.append({"id": p["id"], "name": p["name"], "pos": p["pos"], "age": p["age"], "team": p["teams"][-1] if p["teams"] else "", "teams": p["teams"], "s": s})

outp.sort(key=lambda p: -p["s"]["mp"])
open(out, "w").write("const PLAYERS = " + json.dumps({"season": "2025-26", "players": outp}, separators=(",", ":")) + ";\n")
print(len(outp), "players;", sum(p["s"]["mp"] >= 500 for p in outp), "with 500+ min")
print(outp[0]["name"], outp[0]["team"], {k: outp[0]["s"][k] for k in ["pts_per_g", "ts_pct", "bpm", "mp"]})
multi = [p for p in outp if len(p["teams"]) > 1][:2]; print([(p["name"], p["teams"]) for p in multi])
print(sorted({p["pos"] for p in outp}))
