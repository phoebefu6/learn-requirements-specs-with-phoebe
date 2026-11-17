"""Write window.MINDMAP_DATA into index.html with json.dumps (never string interpolation).
Run from the repo root: python3 materials/build_index_mindmap.py"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = [
    ("The ask behind\nthe dashboard", "01-the-ask-behind-the-dashboard.html", "#34D399",
     ["The decision it serves", "Guessed vs asked", "A decision statement"]),
    ("User stories:\nwho, what, why", "02-user-stories-who-what-why.html", "#34D399",
     ["Role, want, reason", "INVEST and splitting", "Stories or job stories"]),
    ("Acceptance criteria\na builder can test", "03-acceptance-criteria-a-builder-can-test.html", "#FBBF24",
     ["Given, When, Then", "Freshness and access", "Definition of done"]),
    ("The spec\nchecker", "04-the-spec-checker.html", "#FB923C",
     ["14 rules, 14 questions", "Real-story base rates", "More words, more questions"]),
    ("Metric definitions,\ngrain, freshness", "05-metric-definitions-grain-freshness.html", "#FB923C",
     ["Numerator, denominator", "Same name, two numbers", "Source and owner"]),
    ("The one-page spec\nand sign-off", "06-the-one-page-spec-and-sign-off.html", "#F87171",
     ["The one-page template", "Who signs, when", "What forces a re-sign"]),
]
data = {"title": "Requirements\n& Specs", "centerColor": "#3D000E", "sessions": [
    {"label": l, "href": "courses/" + h, "color": c,
     "concepts": [{"label": x, "href": "courses/" + h} for x in cs]} for l, h, c, cs in S]}
p = ROOT / "index.html"
s = p.read_text()
block = "<script>\nwindow.MINDMAP_DATA = " + json.dumps(data, indent=1, ensure_ascii=False) + ";\n</script>"
s2 = re.sub(r"<script>\nwindow\.MINDMAP_DATA = .*?;\n</script>", lambda m: block, s, flags=re.S)
assert s2 != s or block in s
p.write_text(s2)
print("mindmap nodes:", 1 + len(S) + sum(len(x[3]) for x in S))
