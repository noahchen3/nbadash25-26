# SBIN Analytics: Interactive Dashboard Project Guide

This is the brief for every analytics subteam this year. It is intentionally open-ended. You pick the sport, the question and the tools. The NBA Power Board in this repo is **one example** of what a finished project can look like. It is not a template you have to follow.

## The one requirement

Build an interactive dashboard that **answers a question about a sport using data, and that someone outside your group would want to come back to.**

Beyond that, it's up to you. A few directions groups have talked about:

- Rankings: who is actually the best team or player right now?
- Prediction: who makes the playoffs, gets relegated, or wins the title?
- Performance vs. results: who has been lucky or unlucky, and who will regress?
- Player scouting or comparison: who plays like whom, and who is underrated?
- Business: payroll, transfer spend, attendance, ticket prices or valuations vs. on-field results
- Betting markets: does your model beat the odds?
- Something we haven't thought of. Weird questions often make the best projects.

Any sport or league works: NBA, NFL, MLB, NHL, Premier League, Champions League, college, F1, tennis, esports.

## What a strong project has

You don't need all of these, but the best projects usually have most of them.

1. **A clear question.** Write it in one sentence before you build anything. Every chart should help answer it. Three focused charts beat fifteen unrelated ones.
2. **Real interactivity.** The viewer should be able to *do* something: change weights, pick a team, move through time, lock in a result, or filter. Ask yourself what the viewer can find out that a static image couldn't show them.
3. **A sense of time.** Sports change week to week. Either refresh the dashboard as the season goes on, or let the viewer step through a past season.
4. **Your own analysis.** Reproducing the standings is not enough. Add a metric, model or comparison that shows something the standings don't.
5. **Choices you can defend.** Any weighting, threshold or model choice should be written down with a reason. "We weighted recent form at 25% because..." is a strong sentence to have in your presentation.
6. **Explanations in the dashboard itself.** Add tooltips or a methodology section so a club member who doesn't know what xG or net rating means can still use it.
7. **Some form of validation (bonus).** If your dashboard predicts or ranks anything, test it on a past season. "Our rankings predicted second-half records better than the standings did" makes a great final slide.

## Suggested path

1. **Pick a question and check the data first.** Before you commit, confirm you can get the data you need for free and that the site's terms allow your use. Good ideas often die because the data turns out to be paywalled or was taken down (FBref lost its advanced soccer stats in January 2026, for example).
2. **Build a minimum version.** One page, one or two charts, working end to end with real data. Get here early.
3. **Add your own analysis.** This is where the metric, model or comparison from point 4 comes in.
4. **Add interactivity and polish.** Controls, tooltips, a methodology section, a clean layout.
5. **Validate and present.** Explain what you found, how you know it holds up, and what you'd do next.

Check in with the directors after step 1 and after step 2.

## Tools

Use whatever your group knows or wants to learn:

- **Python:** Streamlit, Plotly Dash, or a static page built with Plotly or Altair
- **R:** Shiny or Quarto
- **JavaScript:** a static HTML page with D3, Chart.js or Observable Plot (this is what the NBA example uses)
- **No-code:** Tableau Public or Flourish. These are easier to build with but harder to keep updated automatically.

Free hosting options include GitHub Pages, Streamlit Community Cloud and Tableau Public. A GitHub Action can rerun your data script on a schedule.

## Data starting points

These are starting points, not a full list. Always check each site's terms before scraping.

| Sport | Places to look |
|---|---|
| NBA / NFL / MLB / NHL | Sports-Reference sites, `nba_api`, `nflverse`, `pybaseball`, the NHL API |
| Soccer | Understat (xG), FotMob, Sofascore, Opta Analyst, football-data.co.uk (results and odds), ClubElo, the FPL API, StatsBomb open data |
| Business | Spotrac (payroll), Transfermarkt (transfers and values), Forbes valuations |
| Betting | football-data.co.uk, Kaggle odds datasets |

## Pitfalls to avoid

- **Small samples.** Early-season numbers are noisy. Say so on the dashboard, or use metrics that stabilize faster (margin and xG rather than wins and goals).
- **Unnormalized player stats.** Use per-game, per-36 or per-90 rates with a minimum-minutes cutoff, and compare players only within their position.
- **Mixing data sources.** Different providers calculate xG, ratings and the like differently. Pick one source per metric.
- **Scope creep.** A finished small dashboard beats an unfinished ambitious one.

## How to use the NBA example

Open `index.html` in a browser. Things to notice:

- **The question:** "Who is actually good?" as opposed to who has won the most games.
- **Interactivity with a point:** the weight sliders show how much the rankings depend on your assumptions.
- **Time:** the week slider and the rank chart tell the story of the season.
- **Performance vs. results:** the expected-wins chart is the NBA version of a soccer xPts chart.
- **A methodology section** at the bottom, with the formulas written out.

You're welcome to fork the code if your project goes in a similar direction. You're just as welcome to ignore it and build something completely different.
