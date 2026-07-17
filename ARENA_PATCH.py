<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sprout Admin — waitlist</title>
<meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{--bg:#050810;--panel:#0d1424;--line:#1b2740;--teal:#0ee8d4;--amber:#f5b544;
        --text:#e6edf7;--dim:#7d8aa3;--faint:#4a566e;
        --disp:"Space Grotesk",sans-serif;--mono:"JetBrains Mono",monospace}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font:15px/1.6 var(--disp);min-height:100vh}
  .wrap{max-width:860px;margin:0 auto;padding:40px 24px}
  h1{font-size:24px;display:flex;align-items:center;gap:12px}
  h1 img{height:28px}
  h1 b{color:var(--teal)}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:26px;margin-top:22px}
  label{font-family:var(--mono);font-size:12px;color:var(--dim);display:block;margin:14px 0 6px}
  input{width:100%;background:var(--bg);border:1px solid var(--line);border-radius:5px;
        color:var(--text);padding:11px 13px;font:14px var(--mono)}
  input:focus{outline:none;border-color:var(--teal)}
  button{background:var(--teal);color:var(--bg);border:none;border-radius:5px;padding:11px 20px;
         font:600 14px var(--mono);cursor:pointer;margin-top:16px}
  button.ghost{background:transparent;border:1px solid var(--line);color:var(--dim)}
  .err{color:var(--amber);font-family:var(--mono);font-size:13px;margin-top:10px}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
  .stat{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:16px}
  .stat .n{font-family:var(--mono);font-size:26px;font-weight:700;color:var(--teal)}
  .stat .l{font-size:12px;color:var(--dim)}
  table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:13px}
  th{text-align:left;color:var(--dim);font-weight:500;font-size:11px;text-transform:uppercase;
     letter-spacing:.06em;padding:10px 12px;border-bottom:1px solid var(--line)}
  td{padding:10px 12px;border-bottom:1px solid var(--line)}
  tr:last-child td{border-bottom:none}
  .bars{display:flex;align-items:flex-end;gap:6px;height:90px;margin:8px 0 4px}
  .bar{flex:1;background:var(--teal);border-radius:3px 3px 0 0;min-height:3px;position:relative;opacity:.85}
  .bar span{position:absolute;top:-18px;left:50%;transform:translateX(-50%);
            font:10px var(--mono);color:var(--dim);white-space:nowrap}
  .row{display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}
  .hide{display:none}
</style>
</head>
<body><div class="wrap">
  <h1><img src="images/logo.png" alt="">Sprout <b>Admin</b></h1>

  <!-- LOGIN -->
  <div class="panel" id="login-panel">
    <div style="font-family:var(--mono);font-size:13px;color:var(--dim)">
      Sign in with the admin user you created in Supabase → Authentication → Users.</div>
    <label>Email</label><input type="email" id="li-email" autocomplete="username">
    <label>Password</label><input type="password" id="li-pass" autocomplete="current-password">
    <button id="li-btn">Sign in</button>
    <div class="err" id="li-err"></div>
  </div>

  <!-- DASH -->
  <div class="panel hide" id="dash">
    <div class="row">
      <div style="font-family:var(--mono);font-size:13px;color:var(--dim)" id="who"></div>
      <div>
        <button class="ghost" id="csv-btn">Export CSV</button>
        <button class="ghost" id="out-btn">Sign out</button>
      </div>
    </div>
    <div class="stats" style="margin-top:18px">
      <div class="stat"><div class="n" id="s-total">—</div><div class="l">total signups</div></div>
      <div class="stat"><div class="n" id="s-week">—</div><div class="l">this week</div></div>
      <div class="stat"><div class="n" id="s-prev">—</div><div class="l">last week</div></div>
    </div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--dim)">signups per week</div>
    <div class="bars" id="bars"></div>
    <table>
      <thead><tr><th>Email</th><th>Joined</th><th>Source</th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<script>
// ============ SUPABASE — same two values as index.html ============
const SUPABASE_URL = "https://dkuiqxxxmyekpdggdoic.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_Y1HBqD-Aqr_DCtcxo5vXFw_d1CIMZv5";
// The anon key alone CANNOT read the list — reading requires the admin
// login below, which upgrades this session to `authenticated` (see RLS).
// ==================================================================
const supa = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const $ = id => document.getElementById(id);

async function refresh() {
  const { data: rows, error } = await supa.from("signups")
    .select("email,created_at,source").order("created_at",{ascending:false}).limit(500);
  if (error) { $("li-err").textContent = error.message; return; }
  $("rows").innerHTML = rows.map(r =>
    `<tr><td>${r.email.replace(/</g,"&lt;")}</td><td>${new Date(r.created_at).toLocaleString()}</td><td>${(r.source||"").replace(/</g,"&lt;")}</td></tr>`).join("");
  const { data: weeks } = await supa.from("weekly_signups").select("*").limit(12);
  const w = (weeks||[]).slice().reverse();
  $("s-total").textContent = rows.length + (rows.length===500 ? "+" : "");
  $("s-week").textContent  = w.length ? w[w.length-1].signups : 0;
  $("s-prev").textContent  = w.length>1 ? w[w.length-2].signups : 0;
  const max = Math.max(1,...w.map(x=>x.signups));
  $("bars").innerHTML = w.map(x =>
    `<div class="bar" style="height:${100*x.signups/max}%"><span>${x.signups}</span></div>`).join("");
}

$("li-btn").onclick = async () => {
  $("li-err").textContent = "";
  const { error } = await supa.auth.signInWithPassword({
    email: $("li-email").value.trim(), password: $("li-pass").value });
  if (error) { $("li-err").textContent = error.message; return; }
  enter();
};
$("out-btn").onclick = async () => { await supa.auth.signOut(); location.reload(); };
$("csv-btn").onclick = async () => {
  const { data } = await supa.from("signups").select("email,created_at,source").order("created_at");
  const csv = "email,created_at,source\n" +
    (data||[]).map(r=>`${r.email},${r.created_at},${r.source||""}`).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
  a.download = "sprout-signups.csv"; a.click();
};
async function enter(){
  const { data: { user } } = await supa.auth.getUser();
  if (!user) return;
  $("login-panel").classList.add("hide");
  $("dash").classList.remove("hide");
  $("who").textContent = "signed in as " + user.email;
  refresh();
}
enter(); // auto-resume an existing session
</script>
</body>
</html>
