"""Download 2025-26 NBA schedule/results and league tables from Basketball-Reference into raw/."""
import os, sys, time, urllib.request

out = sys.argv[1] if len(sys.argv) > 1 else "raw"
os.makedirs(out, exist_ok=True)
base = "https://www.basketball-reference.com/leagues/"
pages = {f"games_{m}.html": f"NBA_2026_games-{m}.html" for m in
         ["october", "november", "december", "january", "february", "march", "april"]}
pages["league.html"] = "NBA_2026.html"
pages.update({f"players_{t}.html": f"NBA_2026_{t}.html" for t in ["per_game", "per_poss", "advanced"]})
for name, path in pages.items():
    req = urllib.request.Request(base + path, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(os.path.join(out, name), "wb") as f:
        f.write(r.read())
    print("saved", name)
    time.sleep(3.5)  # Basketball-Reference allows ~20 requests/minute
