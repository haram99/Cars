"""Generate docs/index.html from tokens.json.  Usage: python build.py"""
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).parent
T = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))

FEATURES = [
    ("بيانات السيارات", "الموديل وسنة الصنع ورقم اللوحة وصورة كل سيارة."),
    ("عقود الإيجار", "عقود طويلة الأجل مرتبطة بالجهة المستأجرة والسيارة."),
    ("الأقساط المقترحة", "قسط مقترح لكل سيارة بحسب مدة العقد."),
    ("حركة التأجير", "متابعة يومية لما هو مؤجَّر وما هو متاح."),
]
PREVIEW = [("سنة الصنع", "2022"), ("نوع العقد", "إيجار طويل الأجل"),
           ("رقم اللوحة", "2473 ر ح ع")]

def css_vars(tokens: dict) -> str:
    """Flatten color/radius/space tokens into CSS custom properties."""
    out = []
    for group in ("color", "radius", "space"):
        out += [f"--{group}-{k}:{v};" for k, v in tokens[group].items()]
    out.append(f"--font:{tokens['font']['family']};")
    return "".join(out)

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:var(--font);background:var(--color-ground);
color:var(--color-ink);line-height:1.7}a{color:inherit;text-decoration:none}a:hover{opacity:.85}
.wrap{max-width:1200px;margin:0 auto;padding:0 var(--space-page)}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-block:24px}
.logo{font-weight:700;font-size:20px;display:flex;align-items:center;gap:10px}
.logo i{width:12px;height:12px;border-radius:4px;background:var(--color-accent)}
nav{display:flex;gap:28px;color:var(--color-muted)}
.btn{display:inline-block;padding:15px 28px;border-radius:12px;font-weight:700;font-size:17px}
.btn.dark{background:var(--color-ink);color:#fff;padding:12px 22px;font-size:15px;font-weight:500}
.btn.main{background:var(--color-accent);color:#fff}
.btn.ghost{border:1.5px solid #C9D1DC;font-weight:500}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:48px;align-items:center;padding-block:56px 72px}
.pill{display:inline-block;background:var(--color-accent-soft);color:var(--color-accent-ink);padding:6px 14px;border-radius:999px;font-size:14px;font-weight:500}
h1{margin:20px 0 16px;font-size:52px;line-height:1.25}.hero p{font-size:19px;color:var(--color-muted);max-width:520px;margin:0 0 32px}
.row{display:flex;gap:14px;flex-wrap:wrap}
.card{background:var(--color-surface);border:1px solid var(--color-line);border-radius:20px;padding:24px;box-shadow:0 12px 40px rgba(15,27,45,.08)}
.ph{height:180px;border-radius:14px;background:#EEF1F5;display:flex;align-items:center;justify-content:center;color:var(--color-subtle);margin-block:16px}
.kv{display:flex;justify-content:space-between;padding:12px 16px;background:var(--color-ground);border-radius:var(--radius-sm);margin-bottom:10px}
.kv span{color:var(--color-subtle)}.kv.hl{background:var(--color-accent-soft);color:var(--color-accent-ink)}.kv.hl span{color:inherit}
.band{background:var(--color-surface);border-block:1px solid var(--color-line)}
.band .wrap{padding-block:var(--space-section)}h2{margin:0 0 8px;font-size:34px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:var(--space-gap);margin-top:32px}
.feat{padding:24px;border:1px solid var(--color-line);border-radius:var(--radius-md)}
.feat h3{margin:0 0 6px;font-size:19px}.feat p{margin:0;color:var(--color-muted);font-size:15px}
.cta{background:var(--color-ink);color:#fff;border-radius:var(--radius-lg);padding:56px 40px;text-align:center;margin-block:var(--space-section)}
.cta p{color:#C7D0DC;font-size:17px;margin:0 0 28px}.cta .btn{background:#fff;color:var(--color-ink)}
footer{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--color-subtle);font-size:14px;padding-bottom:40px}
"""

PAGE = Template("""<!doctype html>
<html lang="$lang" dir="$dir"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>$name</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap">
<style>:root{$vars}$css</style></head><body>
<div class="wrap"><header><div class="logo"><i></i>$name</div>
<nav><a href="#features">المزايا</a><a href="#contact">تواصل معنا</a></nav>
<a class="btn dark" href="#contact">اطلب عرضًا تجريبيًا</a></header>
<section class="hero"><div><span class="pill">للشركات المؤجِّرة للسيارات</span>
<h1>أدِر أسطولك وعقودك<br>وأقساطك في مكان واحد</h1>
<p>نظام يتابع حركة تأجير السيارات: بيانات كل سيارة، وعقود الإيجار طويلة الأجل، والأقساط المقترحة، دون جداول متفرقة.</p>
<div class="row"><a class="btn main" href="#contact">ابدأ الآن</a><a class="btn ghost" href="#features">تعرّف على المزايا</a></div></div>
<div class="card"><small>حركة التأجير · نموذج</small><div class="ph">[صورة السيارة]</div>
$preview<div class="kv hl"><span>القسط المقترح</span><b>[المبلغ]</b></div></div></section></div>
<section class="band" id="features"><div class="wrap"><h2>كل ما يحتاجه مكتب التأجير</h2>
<div class="grid">$features</div></div></section>
<div class="wrap" id="contact"><div class="cta"><h2>جاهز لتنظيم حركة التأجير؟</h2>
<p>اطلب عرضًا تجريبيًا وسنعرض لك النظام على بيانات شركتك.</p><a class="btn" href="#">اطلب عرضًا تجريبيًا</a></div>
<footer><span>$name</span><span>$contact</span></footer></div></body></html>""")

def main() -> None:
    site = T["site"]
    html = PAGE.substitute(
        lang=site["lang"], dir=site["dir"], name=site["name"], contact=site["contact"],
        vars=css_vars(T), css=CSS,
        preview="".join(f'<div class="kv"><span>{k}</span><b>{v}</b></div>' for k, v in PREVIEW),
        features="".join(f'<div class="feat"><h3>{t}</h3><p>{d}</p></div>' for t, d in FEATURES),
    )
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
