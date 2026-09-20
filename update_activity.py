"""Generate a dated, truthful profile snapshot from GitHub GraphQL."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from html import escape
import json, subprocess
ROOT=Path(__file__).resolve().parent
QUERY='query { user(login:"Knaifu0030") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } repositories(first:100,privacy:PUBLIC,ownerAffiliations:OWNER,isFork:false,orderBy:{field:UPDATED_AT,direction:DESC}) { nodes { name stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}) { edges { size node { name color } } } } pageInfo { hasNextPage } } } }'
r=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+QUERY]))
if r.get('errors'):raise RuntimeError(r['errors'])
u=r['data']['user']; assert not u['repositories']['pageInfo']['hasNextPage'],'Pagination required'
cal=u['contributionsCollection']['contributionCalendar'];repos=u['repositories']['nodes'];langs=Counter();colors={}
for repo in repos:
 for e in repo['languages']['edges']:
  name=e['node']['name'];langs[name]+=e['size'];colors[name]=e['node']['color'] or '#999999'
date=datetime.now(timezone.utc).strftime('%Y-%m-%d')
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="360" viewBox="0 0 960 360"><rect width="960" height="360" rx="12" fill="#111820"/>']
def text(x,y,t,size=15,fill='#b4bec9'):parts.append(f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" fill="{fill}">{escape(str(t))}</text>')
text(28,38,'On GitHub',23,'#f0f4f8');text(680,36,'Snapshot · '+date+' UTC',13)
text(28,78,f"{cal['totalContributions']:,} contributions in the displayed year",18,'#f0f4f8')
for w,week in enumerate(cal['weeks']):
 for d,day in enumerate(week['contributionDays']):
  n=day['contributionCount'];c='#232e3b' if n==0 else '#4b5e75' if n<5 else '#798ea6' if n<12 else '#b8c8da' if n<25 else '#f0f4f8'
  parts.append(f'<rect x="{28+w*16}" y="{97+d*15}" width="12" height="11" rx="2" fill="{c}"><title>{day["date"]}: {n} contributions</title></rect>')
text(28,225,'Languages across public, non-fork repositories',17,'#f0f4f8')
top=langs.most_common(5);total=sum(langs.values());x=28
for name,n in top:
 width=880*n/total;parts.append(f'<rect x="{x:.2f}" y="242" width="{width:.2f}" height="8" fill="{colors[name]}"/>');x+=width
for i,(name,n) in enumerate(top):text(28+i*175,282,f'{name} {100*n/total:.1f}%',13)
text(28,328,'Public repository bytes · weekly snapshot',12)
parts.append('</svg>');(ROOT/'assets/activity.svg').write_text(''.join(parts))
print({'contributions':cal['totalContributions'],'public_nonfork_repos':len(repos),'languages':top,'snapshot':date})
