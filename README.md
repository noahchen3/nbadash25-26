# NBA Power Board 2025–26

**Live dashboard: https://noahchen3.github.io/nbadash25-26/**

An example interactive dashboard from the SBIN analytics branch at Northeastern. It asks **who is actually good**, as opposed to who has won the most games, using every regular-season game of the 2025–26 NBA season.

**Subteams: start with [GUIDE.md](GUIDE.md).** It's the open-ended brief for your own projects. This dashboard is just one example.

## What's on the page

- **Power rankings.** Weight four factors (season point margin, last-10-games margin, win %, schedule strength), choose a preset or set your own, and step through the season week by week.
- **How the rankings moved.** Each team's weekly rank under your weights, recalculated whenever a weight changes.
- **Expected wins vs. net rating.** A fitted line shows how many wins a team's net rating usually produces. Teams above the line won more than their play suggests, mostly through close games.
- **Methodology.** The formulas and data notes, written out on the page.

Click any team to highlight it in every chart.

### Player profiles (`players.html`)

- **Radar chart builder.** Pick a player and 3 to 10 stats from 35 options (scoring, shooting, playmaking, rebounding, defense, impact). Each stat is one corner, placed by the player's percentile, so a point further out means better.
- **Compare two players** by overlaying their shapes, with a stat table showing raw values and percentiles side by side.
- **Comparison group.** Rank against all players or only the same position group (guards, forwards, centers), with a minimum-minutes cutoff.
- **Most similar players.** Ranks the comparison group by `100 − average percentile gap` on the stats you picked, shows each player's biggest gap, and adds any of them to the chart with one click.
- **Templates** for common archetypes: box score, scorer, playmaker, big man, two-way, shooter.
- Stats where lower is better (turnovers, defensive rating) are flipped. Shooting percentages need enough attempts to be ranked (82 threes, 50 free throws).

## View it

Use the [live link](https://noahchen3.github.io/nbadash25-26/), or open `index.html` locally in a browser. It has no build step or server, and the data is built into the page. GitHub Pages redeploys the site automatically whenever `main` changes.

## Rebuild the data

Requires only Python 3 (no packages).

```bash
python3 scripts/fetch.py raw                                   # download pages from Basketball-Reference
python3 scripts/parse.py raw data/games_raw.json               # extract games and team ratings
python3 scripts/build.py data/games_raw.json data/nba_2025_26.js   # weekly factors, validated against official records
python3 scripts/build_page.py data/nba_2025_26.js src/template.html index.html
python3 scripts/build_players.py raw data/players_2025_26.js   # merge per-game, per-100 and advanced player tables
python3 scripts/build_page.py data/players_2025_26.js src/players_template.html players.html
```

`build.py` checks every team's win total against its official record and fails if any don't match. It also removes the NBA Cup final, which doesn't count in the standings. To adapt this to a live season, change the season in `fetch.py`, run these steps on a schedule (for example with a GitHub Action), and commit the new `index.html`.

## How the numbers are calculated

- **Composite score:** each factor is turned into a z-score across all 30 teams for that week, then blended as `Σ wᵢ·zᵢ / Σ wᵢ`. A team needs 5 games before it is ranked.
- **Schedule strength:** the average season-to-date point margin of the opponents a team has faced.
- **Expected wins:** a least-squares fit of `wins = a + b × net rating` across the 30 teams.

Data: [Basketball-Reference](https://www.basketball-reference.com/leagues/NBA_2026.html). Respect their [usage terms](https://www.sports-reference.com/data_use.html) and rate limits.
