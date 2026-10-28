import re, json, sys, html
raw = sys.argv[1]; out = sys.argv[2]
cell = lambda row, s: (lambda m: html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else None)(re.search(r'data-stat="%s"[^>]*>(.*?)</t[dh]>'%s, row))
games=[]
for m in ['october','november','december','january','february','march','april']:
    t=open(f'{raw}/games_{m}.html',encoding='utf-8').read()
    body=t[t.find('id="schedule"'):]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S):
        if 'Playoffs' in row and 'data-stat="date_game"' not in row: break
        d=cell(row,'date_game'); v=cell(row,'visitor_team_name'); h=cell(row,'home_team_name')
        vp=cell(row,'visitor_pts'); hp=cell(row,'home_pts')
        if d and vp and hp and vp.isdigit(): games.append(dict(date=d,v=v,h=h,vp=int(vp),hp=int(hp)))
    else: continue
    break
t=open(f'{raw}/league.html',encoding='utf-8').read().replace('<!--','').replace('-->','')
adv=t[t.find('id="advanced-team"'):]; adv=adv[:adv.find('</table>')]
teams=[]
for row in re.findall(r'<tr[^>]*>(.*?)</tr>', adv, re.S):
    n=cell(row,'team')
    if not n or n=='League Average' or not (cell(row,'wins') or '').isdigit(): continue
    teams.append(dict(team=n.rstrip('*'),w=int(cell(row,'wins')),l=int(cell(row,'losses')),pw=int(cell(row,'wins_pyth')),
      mov=float(cell(row,'mov')),sos=float(cell(row,'sos')),srs=float(cell(row,'srs')),ortg=float(cell(row,'off_rtg')),drtg=float(cell(row,'def_rtg')),nrtg=float(cell(row,'net_rtg')),pace=float(cell(row,'pace'))))
json.dump(dict(games=games,teams=teams),open(out,'w'))
print(len(games),'games',len(teams),'teams', games[0], games[-1]); print(sorted(teams,key=lambda x:-x['nrtg'])[:3])
