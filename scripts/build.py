import json, sys, datetime as dt
from collections import defaultdict
D=json.load(open(sys.argv[1]))
AB={'Atlanta Hawks':'ATL','Boston Celtics':'BOS','Brooklyn Nets':'BKN','Charlotte Hornets':'CHA','Chicago Bulls':'CHI','Cleveland Cavaliers':'CLE','Dallas Mavericks':'DAL','Denver Nuggets':'DEN','Detroit Pistons':'DET','Golden State Warriors':'GSW','Houston Rockets':'HOU','Indiana Pacers':'IND','Los Angeles Clippers':'LAC','Los Angeles Lakers':'LAL','Memphis Grizzlies':'MEM','Miami Heat':'MIA','Milwaukee Bucks':'MIL','Minnesota Timberwolves':'MIN','New Orleans Pelicans':'NOP','New York Knicks':'NYK','Oklahoma City Thunder':'OKC','Orlando Magic':'ORL','Philadelphia 76ers':'PHI','Phoenix Suns':'PHX','Portland Trail Blazers':'POR','Sacramento Kings':'SAC','San Antonio Spurs':'SAS','Toronto Raptors':'TOR','Utah Jazz':'UTA','Washington Wizards':'WAS'}
EAST={'ATL','BOS','BKN','CHA','CHI','CLE','DET','IND','MIA','MIL','NYK','ORL','PHI','TOR','WAS'}
D['games']=[g for g in D['games'] if not (g['date']=='Tue, Dec 16, 2025' and g['h']=='New York Knicks')]  # NBA Cup final is not a standings game
for g in D['games']: g['d']=dt.datetime.strptime(g['date'],'%a, %b %d, %Y').date()
D['games'].sort(key=lambda g:g['d'])
cnt=defaultdict(int); games=[]
for g in D['games']:
    v,h=AB[g['v']],AB[g['h']]
    if cnt[v]<82 and cnt[h]<82:
        cnt[v]+=1; cnt[h]+=1; games.append((g['d'],v,h,g['vp'],g['hp']))
log=defaultdict(list)  # team -> [(date, opp, margin, close)]
for d,v,h,vp,hp in games:
    log[h].append((d,v,hp-vp)); log[v].append((d,h,vp-hp))
teams={AB[t['team']]:t for t in D['teams']}
for a,t in teams.items():
    w=sum(m>0 for _,_,m in log[a]); assert w==t['w'],(a,w,t['w'])
    close=[m for _,_,m in log[a] if abs(m)<=5]
    t.update(abbr=a, conf='E' if a in EAST else 'W', close_w=sum(m>0 for m in close), close_l=sum(m<0 for m in close))
def factors(upto):
    sub={a:[x for x in log[a] if x[0]<=upto] for a in teams}
    mov={a:sum(m for *_,m in s)/len(s) for a,s in sub.items() if s}
    f={}
    for a,s in sub.items():
        if len(s)<5: return None
        last=s[-10:]
        f[a]=[round(mov[a],2), round(sum(m for *_,m in last)/len(last),2), round(sum(m>0 for *_,m in s)/len(s),3), round(sum(mov[o] for _,o,_ in s)/len(s),2), len(s)]
    return f
start=games[0][0]; end=games[-1][0]; snaps=[]
d=start+dt.timedelta(days=(6-start.weekday())%7+7)
while d<end:
    f=factors(d)
    if f: snaps.append(dict(date=d.strftime('%b %-d'),f=f))
    d+=dt.timedelta(days=7)
snaps.append(dict(date=end.strftime('%b %-d'),f=factors(end)))
out=dict(season='2025-26',through=end.isoformat(),teams=list(teams.values()),snaps=snaps)
open(sys.argv[2],'w').write('const NBA = '+json.dumps(out,separators=(',',':'))+';\n')
print(len(games),'games; snaps',len(snaps),'last',end)
