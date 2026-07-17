# Project Sprout — site kit (VC landing + admin + backend)

One folder, copy-paste setup. Contents:

    index.html        VC-facing landing page (cyberpunk, real numbers, Supabase signup)
    admin.html        private waitlist dashboard (login, weekly chart, CSV export)
    supabase.sql      the entire backend — paste once into Supabase SQL editor
    weekly_report.py  weekly growth digest for your terminal / cron
    SECURITY.md       what's safe where, and why

## Setup — ~10 minutes

1. **Supabase project** — supabase.com -> New project (free tier is fine).

2. **Backend** — Dashboard -> SQL Editor -> paste ALL of `supabase.sql` -> Run.
   That creates the signups table, the security policies, and the weekly view.

3. **Admin login** — Dashboard -> Authentication -> Users -> Add user.
   Your email + a long random password. This is how admin.html signs in.

4. **Keys** — Dashboard -> Settings -> API. Copy two values:
      Project URL          -> paste into BOTH index.html and admin.html
      anon public key      -> paste into BOTH index.html and admin.html
   (Both files have a clearly marked PASTE_YOUR_... block near the bottom.)
   Do NOT put the service_role key in any web file — it's only for
   weekly_report.py via environment variable on your own machine.

5. **Deploy** — push index.html + admin.html to the GitHub Pages repo
   (alongside your existing images/logo.png — both pages reference it).
   robots.txt should include:  Disallow: /admin.html

6. **Weekly report (optional)** — see the header of weekly_report.py.

## Why this is safe to ship publicly
The anon key in the HTML can ONLY insert a signup — Row-Level Security in
supabase.sql blocks it from reading, updating, or deleting anything.
Reading the list requires the admin login (step 3). Full notes: SECURITY.md.
