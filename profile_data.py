#!/usr/bin/env python3
"""Generate profile SVGs from a verified GitHub contribution calendar."""
import datetime as dt
import json
import os
import shutil
import subprocess
import urllib.request

QUERY = """query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      contributionCalendar { totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, ownerAffiliations: [OWNER], privacy: PUBLIC, isFork: false) {
      pageInfo { hasNextPage }
      nodes { name isArchived languages(first: 100) { edges { size node { name } } } }
    }
  }
}"""


def month_window(today):
    """Twelve calendar months including the current incomplete month."""
    last = today.year * 12 + today.month - 1
    return [f"{i // 12:04d}-{i % 12 + 1:02d}" for i in range(last - 11, last + 1)]


def graphql(variables):
    payload = {"query": QUERY, "variables": variables}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        request = urllib.request.Request(
            "https://api.github.com/graphql", json.dumps(payload).encode(),
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json",
             "User-Agent": "Pedrowtst-profile"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    else:
        # Reuse local gh authentication without printing or storing its token.
        gh_bin = shutil.which("gh")
        if not gh_bin:
            raise RuntimeError(
                "GitHub CLI ('gh') is not installed or not in PATH, and neither GH_TOKEN nor GITHUB_TOKEN is set"
            )
        process = subprocess.run(
            [gh_bin, "api", "graphql", "--input", "-"], input=json.dumps(payload),
            capture_output=True, text=True, timeout=45, check=True,
        )
        result = json.loads(process.stdout)
    if result.get("errors") or not result.get("data", {}).get("user"):
        raise ValueError("GitHub did not return a valid contribution calendar")
    user = result["data"]["user"]
    if user["repositories"]["pageInfo"]["hasNextPage"]:
        raise ValueError("Repository pagination required; refusing an incomplete summary")
    projects = [r for r in user["repositories"]["nodes"]
                if not r["isArchived"] and r["name"].lower() != variables["login"].lower()]
    languages = {}
    for repo in projects:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            languages[name] = languages.get(name, 0) + edge["size"]
    return {"calendar": user["contributionsCollection"]["contributionCalendar"],
            "summary": {"commits": user["contributionsCollection"]["totalCommitContributions"],
                        "repos": len(projects), "languages": sorted(languages.items(), key=lambda x: (-x[1], x[0])),
                        "project_scope": "Owned public non-fork non-archived repositories, excluding the profile repository"}}


def aggregate(data, login, now):
    months = {key: 0 for key in month_window(now.date())}
    start, end = next(iter(months)) + "-01", now.date().isoformat()
    seen = set()
    for week in data["weeks"]:
        for day in week["contributionDays"]:
            date, count = day["date"], day["contributionCount"]
            dt.date.fromisoformat(date)
            if type(count) is not int or count < 0 or date in seen:
                raise ValueError("Invalid or duplicate contribution day")
            seen.add(date)
            if start <= date <= end:
                months[date[:7]] += count
    expected = (now.date() - dt.date.fromisoformat(start)).days + 1
    if len([d for d in seen if start <= d <= end]) != expected:
        raise ValueError("Incomplete contribution calendar")
    total = sum(months.values())
    if total != data["totalContributions"]:
        raise ValueError("Contribution total does not match daily counts")
    return {"schema": 2, "username": login, "source": "GitHub GraphQL contributionCalendar",
            "fetched_at": now.isoformat(timespec="seconds"), "from": start, "through": end,
            "total": total, "monthly": [{"month": k, "value": v} for k, v in months.items()]}


def validate_cache(stats, login):
    if stats.get("schema") != 2 or stats.get("username") != login:
        raise ValueError("No verified cache for this profile; run with --refresh")
    through = dt.date.fromisoformat(stats["through"])
    if [m["month"] for m in stats["monthly"]] != month_window(through):
        raise ValueError("Cached calendar months are invalid")
    if any(type(m["value"]) is not int or m["value"] < 0 for m in stats["monthly"]):
        raise ValueError("Cached contribution counts are invalid")
    if sum(m["value"] for m in stats["monthly"]) != stats["total"]:
        raise ValueError("Cached contribution total is invalid")
    if stats["from"] != month_window(through)[0] + "-01":
        raise ValueError("Cached period is invalid")
    for field in ("commits", "repos"):
        if type(stats.get(field)) is not int or stats[field] < 0:
            raise ValueError("Cached summary is invalid")
    try:
        dt.datetime.fromisoformat(stats["fetched_at"])
    except (KeyError, ValueError, TypeError):
        raise ValueError("Cached fetched_at timestamp is invalid")
    if any(not isinstance(name, str) or type(size) is not int or size < 0
           for name, size in stats["languages"]):
        raise ValueError("Cached languages are invalid")
    return stats
