"""Build the GitHub Pages copy of the app into docs/.

index.html at the repo root is written for Claude artifacts (no <html>/<head> skeleton).
This wraps it into a standalone page and copies the samples next to it.
Run from the repo root:  python3 tools/build_pages.py
"""
import pathlib, shutil

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
cut = src.index("</style>") + len("</style>")
head, body = src[:cut], src[cut:]

page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#17110f">
<meta name="apple-mobile-web-app-title" content="Salsa">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-180.png">
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
{head}
</head>
<body>
{body}
</body>
</html>
"""
docs = root / "docs"
docs.mkdir(exist_ok=True)
(docs / "index.html").write_text(page, encoding="utf-8")
(docs / ".nojekyll").write_text("")
shutil.copytree(root / "samples", docs / "samples", dirs_exist_ok=True)
shutil.copy(root / "tools" / "icon-180.png", docs / "icon-180.png")
print("docs/ built:", sum(1 for _ in (docs / "samples").iterdir()), "samples")
