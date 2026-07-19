#!/usr/bin/env python3
"""
weekly_report.py — Project Sprout signup digest.
Run it weekly (cron, or just by hand every Monday) to see growth.

Setup (one time):
    pip install supabase
    export SUPABASE_URL="https://YOURPROJECT.supabase.co"
    export SUPABASE_SERVICE_KEY="...service_role key..."   # Settings -> API
    # The service key BYPASSES RLS — keep it in your shell env or a .env
    # you never commit. It exists only on your machine, never in the site.

Cron example (every Monday 9am):
    0 9 * * 1  cd /path/here && ./weekly_report.py >> signups.log
"""
import os, sys
from datetime import datetime

try:
    from supabase import create_client
except ImportError:
    sys.exit("pip install supabase")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
if not url or not key:
    sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_KEY env vars (see header).")

supa = create_client(url, key)
weeks = supa.table("weekly_signups").select("*").limit(8).execute().data
total = supa.table("signups").select("id", count="exact").execute().count

print(f"\n=== PROJECT SPROUT — signup report · {datetime.now():%Y-%m-%d} ===")
print(f"total signups: {total}\n")
print(f"{'week of':<14}{'signups':>8}   trend")
prev = None
for w in reversed(weeks):
    n = w["signups"]
    arrow = "" if prev is None else ("▲" if n > prev else "▼" if n < prev else "→")
    bar = "█" * max(1, round(n / max(x['signups'] for x in weeks) * 24))
    print(f"{w['week_start']:<14}{n:>8}   {arrow} {bar}")
    prev = n
print()
