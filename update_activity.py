"""Small contribution strip; real public GitHub data, no fabricated stats."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess
R=Path(__file__).resolve().parent
q='query { user(login:"Knaifu0030") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }'
r=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+q]))
if r.get('errors'):raise RuntimeError(r['errors'])
c=r['data']['user']['contributionsCollection']['contributionCalendar']
a=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="167" viewBox="0 0 960 167"><rect width="960" height="167" fill="#0d1117"/>']
a.append(f'<text x="32" y="26" fill="#abb8c4" font-family="monospace" font-size="14">{c["totalContributions"]} contributions</text>')
a.append(f'<text x="783" y="26" fill="#748594" font-family="monospace" font-size="12">{datetime.now(timezone.utc):%Y-%m-%d}</text>')
for w,week in enumerate(c['weeks']):
 for d,day in enumerate(week['contributionDays']):
  n=day['contributionCount'];color='#202a35' if n==0 else '#536879' if n<5 else '#8ca1af' if n<12 else '#c5d4de'
  a.append(f'<rect x="{32+w*16.8}" y="{43+d*14}" width="12" height="10" fill="{color}"><title>{day["date"]}: {n}</title></rect>')
a.append('</svg>');(R/'assets/activity.svg').write_text(''.join(a));print('Contribution strip updated')
