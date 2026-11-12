"""Collect public GitHub activity and draw a notebook dashboard.

Set GH_TOKEN to the workflow's built-in token, or use --snapshot with an existing
normalized snapshot for deterministic offline rendering. No private repo access.
"""
import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from notebook_art import ROOT, INK, PAPER, BLUE, MINT, YELLOW, text, svg

LOGIN = 'sakarkhadka10'

def api(path, payload=None):
    token = os.environ.get('GH_TOKEN')
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'notebook-profile'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request('https://api.github.com/' + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)

def collect():
    end = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=364)
    query = '''query($login:String!,$from:DateTime!,$to:DateTime!){
      user(login:$login){contributionsCollection(from:$from,to:$to){
        contributionCalendar{weeks{contributionDays{date contributionCount}}}
      }}
    }'''
    result = api('graphql', {'query': query, 'variables': {
        'login': LOGIN, 'from': f'{start}T00:00:00Z', 'to': f'{end}T23:59:59Z'}})
    if result.get('errors'):
        raise RuntimeError('GitHub contribution query failed; preserving current assets')
    weeks = result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    days = [{'date': day['date'], 'count': day['contributionCount']}
            for week in weeks for day in week['contributionDays']
            if str(start) <= day['date'] <= str(end)]
    commits = api('search/commits?' + urllib.parse.urlencode({
        'q': f'author:{LOGIN} author-date:{start}..{end}', 'per_page': 1}))
    if commits.get('incomplete_results'):
        raise RuntimeError('Incomplete commit search; preserving current assets')
    repos = []
    page = 1
    while True:
        batch = api(f'users/{LOGIN}/repos?per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return {'login': LOGIN, 'from': str(start), 'through': str(end),
            'days': days, 'public_indexed_commits': commits['total_count'],
            'public_stars': sum(r['stargazers_count'] for r in repos if not r['fork']),
            'public_repositories': sum(not r['fork'] for r in repos)}


def render(snapshot):
    start, end = [dt.date.fromisoformat(snapshot[k]) for k in ['from', 'through']]
    days = sorted(snapshot['days'], key=lambda x: x['date'])
    assert len(days) == 365 and (end - start).days == 364
    assert all(d['date'] == str(start + dt.timedelta(days=i)) and
               isinstance(d['count'], int) and d['count'] >= 0 for i, d in enumerate(days))
    active, longest, current = 0, 0, 0
    for day in days:
        active += day['count'] > 0
        current = current + 1 if day['count'] else 0
        longest = max(longest, current)
    total = sum(d['count'] for d in days)
    body = f'<rect x="1" y="1" width="998" height="468" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += text('The commit journal.', 32, 48, 34, 'hand', BLUE)
    body += text(f'{start:%d %b %Y} — {end:%d %b %Y}', 620, 45, 18)
    metrics = [(f'{total:,}', 'contributions', MINT),
               (f'{snapshot["public_indexed_commits"]:,}', 'public commits', YELLOW),
               (f'{longest} days', 'longest streak', '#e5ebfa'),
               (str(snapshot['public_stars']), 'public repo stars', '#ffdeeb')]
    for i, (number, label, color) in enumerate(metrics):
        x = 32 + i * 240
        body += f'<rect x="{x+3}" y="75" width="216" height="112" rx="6" fill="{INK}"/>'
        body += f'<rect x="{x}" y="72" width="216" height="112" rx="6" fill="{color}" stroke="{INK}" stroke-width="1.5"/>'
        body += text(number, x + 16, 130, 53, 'display')
        body += text(label, x + 16, 162, 18)
    body += text('A YEAR OF SHOWING UP', 32, 224, 16, spacing=1.2)
    body += text(f'{active} active days / {snapshot["public_repositories"]} public repositories', 620, 224, 17)
    # Sunday-first calendar; incomplete edge weeks contain only observed dates.
    first_sunday = start - dt.timedelta(days=(start.weekday()+1) % 7)
    palette = ['#e6e6df', '#bdd6f7', '#7fa4ef', '#4873ed', BLUE]
    maximum = max(d['count'] for d in days) or 1
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        offset = (date - first_sunday).days
        week, weekday = divmod(offset, 7)
        level = 0 if not day['count'] else min(4, 1 + int(day['count'] / maximum * 3))
        x, y = 55 + week * 17, 262 + weekday * 17
        body += f'<rect x="{x}" y="{y}" width="13" height="13" rx="3" fill="{palette[level]}"><title>{date}: {day["count"]} contributions</title></rect>'
    for label, row in [('M', 1), ('W', 3), ('F', 5)]:
        body += text(label, 32, 273 + row * 17, 11)
    # Month labels appear once at the first week boundary inside each month.
    for i in range(54):
        date = first_sunday + dt.timedelta(days=i*7)
        if start <= date <= end and date.day <= 7:
            body += text(date.strftime('%b'), 55+i*17, 251, 12)
    body += text('Less', 758, 408, 13)
    for i, color in enumerate(palette):
        body += f'<rect x="{794+i*18}" y="396" width="13" height="13" rx="3" fill="{color}"/>'
    body += text('More', 889, 408, 13)
    body += text('Public activity. Small steps, real things shipped.', 32, 443, 23, 'hand', BLUE)
    body += text('Refreshed daily / UTC', 753, 444, 13)
    return svg(1000, 470, f'{LOGIN} — the commit journal',
        f'{total} contributions, {snapshot["public_indexed_commits"]} indexed public commits, '
        f'{longest}-day longest streak, {snapshot["public_stars"]} public repository stars. '
        f'Activity from {start} through {end}.', body)

def render_month(snapshot):
    days = sorted(snapshot['days'], key=lambda x: x['date'])[-30:]
    maximum = max(d['count'] for d in days) or 1
    body = '''<style>@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}
    .bar{animation:rise 1.2s ease-out both;transform-box:fill-box;transform-origin:bottom}
    @media(prefers-reduced-motion:reduce){.bar{animation:none}}</style>'''
    body += f'<rect x="1" y="1" width="998" height="258" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += text('Small steps. Every day.', 32, 44, 31, 'hand', BLUE)
    body += text('DAILY CONTRIBUTIONS / LAST 30 DAYS', 582, 43, 16)
    for y in [80, 120, 160, 200]:
        body += f'<path d="M44 {y}H958" stroke="{BLUE}" stroke-opacity=".12" stroke-dasharray="3 5"/>'
    for i, day in enumerate(days):
        height = max(3, day['count'] / maximum * 125)
        x = 47 + i * 30.5
        color = YELLOW if day['count'] == maximum else BLUE
        body += f'<rect class="bar" x="{x}" y="{200-height:.2f}" width="20" height="{height:.2f}" rx="3" fill="{color}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
    body += text(dt.date.fromisoformat(days[0]['date']).strftime('%d %b'), 46, 230, 15)
    body += text(dt.date.fromisoformat(days[-1]['date']).strftime('%d %b'), 902, 230, 15)
    body += text(f'Peak: {maximum} contributions', 396, 234, 19, 'hand', BLUE)
    return svg(1000, 260, 'Daily contributions — last 30 days',
               f'Bar chart of real daily contribution counts. Highest daily count: {maximum}.', body)


def render_mobile(snapshot):
    # Keep the yearly metrics readable; show the latest 90 calendar days below.
    render(snapshot)  # Apply the same complete-history validation.
    days = sorted(snapshot['days'], key=lambda x: x['date'])
    current = longest = 0
    for day in days:
        current = current + 1 if day['count'] else 0
        longest = max(longest, current)
    body = f'<rect x="1" y="1" width="638" height="728" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += text('The commit journal.', 29, 44, 34, 'hand', BLUE)
    body += text('TRAILING 365 DAYS', 355, 42, 20)
    metrics = [(f'{sum(d["count"] for d in days):,}', 'contributions', MINT),
               (f'{snapshot["public_indexed_commits"]:,}', 'public commits', YELLOW),
               (f'{longest} days', 'longest streak', '#e5ebfa'),
               (str(snapshot['public_stars']), 'public repo stars', '#ffdeeb')]
    for i, (number, label, color) in enumerate(metrics):
        x, y = 28 + i % 2 * 302, 67 + i // 2 * 142
        body += f'<rect x="{x+3}" y="{y+4}" width="278" height="122" rx="6" fill="{INK}"/><rect x="{x}" y="{y}" width="278" height="122" rx="6" fill="{color}" stroke="{INK}" stroke-width="1.5"/>'
        body += text(number, x+18, y+66, 65, 'display')
        body += text(label, x+18, y+102, 23)
    body += text('A LITTLE EVERY DAY / LAST 90 DAYS', 28, 397, 22)
    recent = days[-90:]
    first = dt.date.fromisoformat(recent[0]['date'])
    sunday = first - dt.timedelta(days=(first.weekday()+1)%7)
    maximum = max(d['count'] for d in recent) or 1
    palette = ['#e6e6df', '#bdd6f7', '#7fa4ef', '#4873ed', BLUE]
    for day in recent:
        date = dt.date.fromisoformat(day['date'])
        week, row = divmod((date-sunday).days, 7)
        level = 0 if not day['count'] else min(4, 1+int(day['count']/maximum*3))
        body += f'<rect x="{57+week*39}" y="{425+row*32}" width="29" height="25" rx="4" fill="{palette[level]}"><title>{date}: {day["count"]} contributions</title></rect>'
    body += text('Refreshed through ' + snapshot['through'], 28, 699, 23, 'hand', BLUE)
    return svg(640, 730, 'The commit journal — mobile',
               'Yearly contributions, indexed public commits, longest streak, and public stars. Calendar shows the last 90 days.', body)


def render_month_mobile(snapshot):
    # Share the data and chart animation; enlarge the canvas typography for phones.
    import re
    full = render_month(snapshot)
    # Reuse the same animation while laying out the same data at phone scale.
    plot = re.search(r'(<style>.*?</style>)', full, re.S).group(1)
    body = plot + f'<rect x="1" y="1" width="638" height="290" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += text('Small steps. Every day.', 28, 43, 33, 'hand', BLUE)
    body += text('DAILY CONTRIBUTIONS / LAST 30 DAYS', 28, 77, 19)
    days = sorted(snapshot['days'], key=lambda x: x['date'])[-30:]
    maximum = max(d['count'] for d in days) or 1
    for y in [111, 150, 189, 228]:
        body += f'<path d="M28 {y}H612" stroke="{BLUE}" stroke-opacity=".12" stroke-dasharray="3 5"/>'
    for i, day in enumerate(days):
        height = max(3, day['count']/maximum*120)
        color = YELLOW if day['count']==maximum else BLUE
        body += f'<rect class="bar" x="{31+i*19.5}" y="{228-height:.2f}" width="13" height="{height:.2f}" rx="2" fill="{color}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
    body += text(dt.date.fromisoformat(days[0]['date']).strftime('%d %b'), 28, 267, 21)
    body += text(f'Peak: {maximum}', 269, 267, 21)
    body += text(dt.date.fromisoformat(days[-1]['date']).strftime('%d %b'), 535, 267, 21)
    return svg(640, 292, 'Daily contributions — mobile', 'The last 30 days of contribution activity.', body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text()) if args.snapshot else collect()
    output = render(snapshot)
    # Collection and rendering finish before replacing the published files.
    for name, data in [('activity.svg', output), ('activity-month.svg', render_month(snapshot)),
                       ('activity-mobile.svg', render_mobile(snapshot)),
                       ('activity-month-mobile.svg', render_month_mobile(snapshot)),
                       ('activity.json', json.dumps(snapshot, indent=2)+'\n')]:
        target = ROOT / 'assets' / name
        tmp = target.with_suffix(target.suffix + '.tmp')
        tmp.write_text(data)
        tmp.replace(target)
    print('Updated activity journal through', snapshot['through'])
