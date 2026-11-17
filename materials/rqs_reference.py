"""rqs_reference.py - Python twin of assets/rqs-live.js (the spec checker), by Phoebe Fu.

The ONE source of truth for the checker's word lists, field names, padding sentences and the
Saffrondale presets: build_rqs_sample.py copies CONSTANTS and PRESETS into assets/rqs-sample.js with
json.dumps, and the browser engine reads them from there. The rule LOGIC is written twice (here and
in rqs-live.js) on purpose, so that a disagreement shows up in compare-ladder.py.

  python3 materials/rqs_reference.py ladder > py.json     every preset, plain and padded, + corpus
  python3 materials/rqs_reference.py test                  pass + fail unit test for every rule
  python3 materials/rqs_reference.py write-tests           (re)write materials/rqs_rule_tests.json
  python3 materials/rqs_reference.py full-corpus <rawdir>  base rates on all 1,721 stories (map only)

Saffrondale Clinics is a constructed example. The stories in the corpus are real (Dalpiaz 2018,
CC BY 4.0). The rules are a teaching lint, not AQUSA: see RULES[...]["origin"] for which published
criterion each one is modelled on and which are lab-only.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------- constants
# Every regex below is written in the subset where Python `re` (with re.I | re.A) and JavaScript
# (flag "i") behave the same on ASCII text. The sample builder folds the corpus to ASCII first.

RULES = [
    # id, name, scope, origin, question
    {"id": "no-decision", "name": "No decision named", "scope": "spec",
     "origin": "Lab-only rule: a 'Decision:' line must name a choice (which, whether, when, how many, how much, who).",
     "question": "What will someone decide differently once this exists, and between which options?"},
    {"id": "no-user", "name": "No user story", "scope": "spec",
     "origin": "Lab-only rule, from the story format (Connextra template, reported by Cohn).",
     "question": "Who will use this, in which part of their job?"},
    {"id": "well-formed", "name": "Story lacks a role or a want", "scope": "story",
     "origin": "QUS 'Well-formed': a story includes at least a role and a means (Lucassen et al. 2016).",
     "question": "Who is this for, and what do they want to do?"},
    {"id": "no-benefit", "name": "Story gives no reason", "scope": "story",
     "origin": "Lab-only rule. Contested: QUS calls the 'so that' end optional, and Cohn does not make it mandatory.",
     "question": "What changes for this person if we build it?"},
    {"id": "compound", "name": "Two asks in one story", "scope": "story",
     "origin": "QUS 'Atomic'. Simplified from AQUSA, which also parses both sides of the 'and' (AQUSA's own Atomic precision was 51.18%).",
     "question": "These are two asks: which comes first, and can they ship apart?"},
    {"id": "not-minimal", "name": "Extra notes inside the story", "scope": "story",
     "origin": "QUS 'Minimal': nothing more than role, means and ends; AQUSA flags text in brackets or after a full stop, hyphen or asterisk.",
     "question": "Is this note part of the requirement, or a comment for later?"},
    {"id": "vague", "name": "Vague word", "scope": "line",
     "origin": "Modelled on QUS 'Unambiguous' (a semantic criterion AQUSA v1 does not check). The word list is lab-only.",
     "question": "(set per word)"},
    {"id": "untestable", "name": "Criterion with nothing to check", "scope": "criterion",
     "origin": "Lab-only rule, after Wake's 'Testable' and Gherkin's advice to verify an observable outcome.",
     "question": "What would I look at, or count, to call this passed?"},
    {"id": "no-criteria", "name": "No acceptance criteria", "scope": "spec",
     "origin": "Lab-only rule: the Agile Alliance glossary pairs every story with acceptance criteria.",
     "question": "How will we both know it is done?"},
    {"id": "metric-undefined", "name": "Metric named but not defined", "scope": "data",
     "origin": "Lab-only rule, after the dbt Semantic Layer ratio metric (numerator and denominator).",
     "question": "Which number exactly: a count of what, divided by a count of what?"},
    {"id": "no-grain", "name": "No grain", "scope": "data",
     "origin": "Lab-only rule.",
     "question": "One row, one bar, one dot per what: per clinic, per day, per patient?"},
    {"id": "no-freshness", "name": "No freshness with a number", "scope": "data",
     "origin": "Lab-only rule.",
     "question": "How old may the data be when someone acts on it?"},
    {"id": "no-source", "name": "No data source or owner", "scope": "data",
     "origin": "Lab-only rule, after the Data Cards 'upstream sources' field (Pushkarna et al. 2022).",
     "question": "Which table does this come from, and who answers when it looks wrong?"},
    {"id": "no-signoff", "name": "No decision owner or sign-off", "scope": "spec",
     "origin": "Lab-only rule.",
     "question": "Who confirms this is what they asked for, and on which date?"},
]
RULE_IDS = [r["id"] for r in RULES]

# term, pattern, quantity word (exempt when the line carries a digit), builder question
VAGUE = [
    ["fast", r"\bfast(er)?\b", True, "How fast is fast: in seconds, at which load?"],
    ["quick", r"\bquick(ly)?\b", True, "How quick, measured how?"],
    ["real-time", r"\breal[- ]?time\b", True, "Real time means how many seconds or minutes behind?"],
    ["up to date", r"\bup[- ]to[- ]date\b", True, "Up to date as of when: the last hour, last night?"],
    ["timely", r"\btimely\b", True, "Timely by which deadline?"],
    ["accurate", r"\baccurate(ly)?\b", True, "Accurate against what, within what tolerance?"],
    ["user-friendly", r"\buser[- ]friendly\b", False, "Friendly to which user, shown how?"],
    ["easy", r"\beas(y|ily|ier)\b", False, "Easy for whom, checked how?"],
    ["simple", r"\bsimple\b", False, "Simple compared with what?"],
    ["intuitive", r"\bintuitive(ly)?\b", False, "Intuitive to whom, without what help?"],
    ["efficient", r"\befficient(ly)?\b", False, "Efficient in time, clicks or cost?"],
    ["flexible", r"\bflexible\b", False, "Flexible in which direction: what may change later?"],
    ["robust", r"\brobust\b", False, "Robust to which failure?"],
    ["seamless", r"\bseamless(ly)?\b", False, "Seamless across which steps?"],
    ["as appropriate", r"\bas appropriate\b", False, "Appropriate by whose rule?"],
    ["as needed", r"\bas needed\b", False, "Needed when, decided by whom?"],
    ["etc.", r"\betc\b", False, "What else is in the list?"],
    ["and/or", r"\band/or\b", False, "Both, or either one?"],
    ["maybe", r"\bmaybe\b", False, "Is it in scope or not?"],
]

FIELDS = ["decision", "decision owner", "metric", "definition", "numerator", "denominator", "grain",
          "freshness", "source", "data owner", "signed off", "version", "change log",
          "acceptance criteria", "criteria", "stories", "user stories", "ask", "notes", "filters",
          "time window", "excludes"]
SECTION_FIELDS = {"acceptance criteria": "criteria", "criteria": "criteria", "stories": "stories",
                  "user stories": "stories"}

PATTERNS = {
    "bullet": r"^(?:[-*]|\d+[.)])\s+",
    "field": r"^([A-Za-z][A-Za-z ]{1,30}):\s*(.*)$",
    "gherkin": r"^(given|when|then|and|but)\b",
    "story_start": r"^as\s+(?:an?|the)\s",
    "story_want": r"\bi\s+(?:want|need|would like|would be able|am able|'m able|can|don't want|do not want)\b",
    "role": r"^as\s+[a-z]",
    "means": r"\bi\s+(?:want|need|would like|would be able|am able|'m able|can|don't want|do not want)\b(?:\s+to\b)?",
    "ends": r"\bso\s+(?:that|i|we)\b",
    "compound": r"\s(?:and|or)\s|\s&\s|\s\+\s",
    "minimal": r"[(\[{]|[.?!]\s+\S|\s-\s|\*",
    "observable": r"\b(shows?|displays?|lists?|returns?|sends?|flags?|highlights?|exports?|equals?|matches|appears?|contains?|includes?|sorted|filtered|counts?|prints?|opens?|alerts?)\b",
    "quoted": "\"[^\"]+\"",
    "digit": r"\d",
    "choice": r"\b(which|whether|when|how many|how much|who)\b",
    "date": r"\d{4}-\d{2}-\d{2}",
    "letter": r"[a-z]",
    "data_product": r"\b(dashboards?|reports?|metrics?|rates?|kpis?|models?|forecasts?|charts?|pipelines?)\b|%",
    "grain_phrase": r"\bone row per\b",
    "fresh_phrase": r"\b(no older than|refreshed|updated|loaded)\b[^.]*\d",
    "ratio_words": r"\bdivided by\b",
}

PAD = [
    "It should be easy to use for all clinic staff.",
    "The numbers should always be accurate and up to date.",
    "Ideally it loads fast and works seamlessly on any device.",
    "Staff can then act on it as appropriate.",
]

CONSTANTS = {"rules": RULES, "vague": VAGUE, "fields": FIELDS, "sectionFields": SECTION_FIELDS,
             "patterns": PATTERNS, "pad": PAD}

FL = re.I | re.A


def rx(name):
    return re.compile(PATTERNS[name], FL)


VAGUE_RX = [(t, re.compile(p, FL), q, ques) for t, p, q, ques in VAGUE]
QUESTION = {r["id"]: r["question"] for r in RULES}


# ----------------------------------------------------------------------------- parsing
def parse(text):
    """Classify each non-empty line: field / criterion / story / text. Returns a list of dicts."""
    out = []
    section = None
    chain = None  # last Gherkin main keyword: given / when / then
    for i, raw in enumerate(text.split("\n")):
        t = raw.strip()
        if not t:
            continue
        body = rx("bullet").sub("", t, count=1)
        ln = {"line": i + 1, "body": body, "kind": "text"}
        m = rx("field").match(body)
        if m and m.group(1).strip().lower() in FIELDS:
            name = m.group(1).strip().lower()
            ln.update(kind="field", field=name, value=m.group(2).strip())
            section = SECTION_FIELDS.get(name)
            chain = None
            out.append(ln)
            continue
        g = rx("gherkin").match(body)
        if g:
            kw = g.group(1).lower()
            if kw in ("given", "when", "then"):
                chain = kw
            ln.update(kind="criterion", kw=kw, checked=(kw == "then" or (kw in ("and", "but") and chain == "then")))
            out.append(ln)
            continue
        if rx("story_start").search(body) or rx("story_want").search(body):
            ln["kind"] = "story"
            out.append(ln)
            continue
        if section == "criteria":
            ln.update(kind="criterion", kw="bullet", checked=True)
        out.append(ln)
    return out


def vague_hits(body):
    has_digit = bool(rx("digit").search(body))
    hits = []
    for term, r, quantity, ques in VAGUE_RX:
        if r.search(body) and not (quantity and has_digit):
            hits.append((term, ques))
    return hits


def story_findings(body):
    """Story-level rules on one story. Returns [(rule, term or None, question)]."""
    f = []
    m = rx("means").search(body)
    if not rx("role").search(body) or not m:
        f.append(("well-formed", None, QUESTION["well-formed"]))
    if not rx("ends").search(body):
        f.append(("no-benefit", None, QUESTION["no-benefit"]))
    if m:
        rest = body[m.end():]
        e = rx("ends").search(rest)
        means = rest[:e.start()] if e else rest
        if rx("compound").search(" " + means + " "):
            f.append(("compound", None, QUESTION["compound"]))
    if rx("minimal").search(body.rstrip(".!? ")):
        f.append(("not-minimal", None, QUESTION["not-minimal"]))
    return f


def field_value(lines, name):
    for ln in lines:
        if ln["kind"] == "field" and ln["field"] == name and ln["value"]:
            return ln["value"]
    return None


def check(text):
    lines = parse(text)
    findings = []

    def add(rule, line, term=None, question=None):
        findings.append({"rule": rule, "line": line, "term": term,
                         "question": question or QUESTION[rule]})

    for ln in lines:
        body = ln["body"]
        if ln["kind"] == "story":
            for rule, term, q in story_findings(body):
                add(rule, ln["line"], term, q)
        if ln["kind"] == "criterion" and ln["checked"]:
            if not (rx("digit").search(body) or rx("quoted").search(body) or rx("observable").search(body)):
                add("untestable", ln["line"])
        scan = ln["value"] if ln["kind"] == "field" else body
        for term, q in vague_hits(scan):
            add("vague", ln["line"], term, q)

    # whole-spec rules (line 0 = the spec as a whole)
    dec = field_value(lines, "decision")
    if not dec or not rx("choice").search(dec):
        add("no-decision", 0)
    if not any(ln["kind"] == "story" for ln in lines):
        add("no-user", 0)
    if not any(ln["kind"] == "criterion" for ln in lines):
        add("no-criteria", 0)
    if rx("data_product").search(text):
        metric = field_value(lines, "metric")
        defined = field_value(lines, "definition") or (field_value(lines, "numerator") and field_value(lines, "denominator"))
        if not metric or not defined:
            add("metric-undefined", 0)
        if not field_value(lines, "grain") and not rx("grain_phrase").search(text):
            add("no-grain", 0)
        fr = field_value(lines, "freshness")
        if not (fr and rx("digit").search(fr)) and not any(rx("fresh_phrase").search(ln["body"]) for ln in lines):
            add("no-freshness", 0)
        if not field_value(lines, "source") or not field_value(lines, "data owner"):
            add("no-source", 0)
    owner = field_value(lines, "decision owner")
    signed = field_value(lines, "signed off")
    if not (owner and rx("letter").search(owner)) or not (signed and rx("date").search(signed)):
        add("no-signoff", 0)

    findings.sort(key=lambda x: (x["line"], RULE_IDS.index(x["rule"]), x["term"] or ""))
    by_rule = {r: 0 for r in RULE_IDS}
    for x in findings:
        by_rule[x["rule"]] += 1
    words = len(text.split())
    return {"questions": len(findings), "words": words, "lines": len([1 for ln in lines]),
            "byRule": by_rule, "findings": findings}


def pad(text):
    """The anti-lever: append one well-meaning sentence to every story and checked criterion."""
    out, k = [], 0
    kinds = {ln["line"]: ln for ln in parse(text)}
    for i, raw in enumerate(text.split("\n")):
        ln = kinds.get(i + 1)
        if ln and (ln["kind"] == "story" or (ln["kind"] == "criterion" and ln["checked"])):
            raw = raw.rstrip() + " " + PAD[k % len(PAD)]
            k += 1
        out.append(raw)
    return "\n".join(out)


def pct(count, n):
    """Round half up to one decimal with integers only, so node and python agree exactly."""
    return ((count * 2000 + n) // (2 * n)) / 10 if n else 0.0


CORPUS_RULES = ["well-formed", "no-benefit", "compound", "not-minimal", "vague"]


def corpus(stories):
    """Base rate per story rule over real stories (each story checked on its own line)."""
    n = len(stories)
    counts = {r: 0 for r in CORPUS_RULES}
    total_q = 0
    for s in stories:
        rules = [r for r, _, _ in story_findings(s)] + ["vague" for _ in vague_hits(s)]
        total_q += len(rules)
        for r in set(rules):
            counts[r] += 1
    clean = sum(1 for s in stories if not story_findings(s) and not vague_hits(s))
    return {"n": n, "rates": {r: {"count": counts[r], "pct": pct(counts[r], n)} for r in CORPUS_RULES},
            "clean": {"count": clean, "pct": pct(clean, n)},
            "questions": total_q, "perHundred": pct(total_q, n)}


# ----------------------------------------------------------------------------- presets
PRESETS = [
    {"id": "ask", "label": "1 · The one-line ask",
     "note": "Constructed Saffrondale example. What the operations director sent: one line.",
     "text": "Can we get a no-show dashboard for the clinics, and maybe a model?"},
    {"id": "draft", "label": "2 · First draft",
     "note": "Constructed Saffrondale example. The analyst's first written draft: more words, and now the questions are visible.",
     "text": "\n".join([
         "Saffrondale Clinics no-show dashboard (first draft)",
         "Decision: better visibility of no-shows",
         "As a manager, I want a no-show dashboard and a prediction model.",
         "As a receptionist, I want to see no-shows in real time.",
         "As a clinic lead, I want a user-friendly dashboard that loads fast.",
         "Acceptance criteria:",
         "- The dashboard is easy to read.",
         "- Data is accurate and up to date.",
         "- The model works well.",
     ])},
]
_DEC = "Decision: Each Monday, the clinic operations lead decides which booked patients get a reminder call."
_STORIES = [
    "As a clinic operations lead, I want to see last week's no-show rate for each clinic, so that I can decide where reminder calls go.",
    "As a receptionist, I want a list of next week's patients with a high no-show risk, so that I can call them first.",
    "As a clinic operations lead, I want to compare this month's no-show rate with last month's, so that I can tell whether the calls help.",
]
_VAGUE_AC = ["Acceptance criteria:", "- The dashboard is easy to read.", "- Data is accurate and up to date.",
             "- The model works well."]
_TEST_AC = [
    "Acceptance criteria:",
    "Given the dashboard is opened on a Monday",
    "When the clinic operations lead picks a clinic",
    "Then the page shows last week's no-show rate for that clinic, Monday to Sunday.",
    "And the page shows the same rate for each of the 4 weeks before it.",
    "- The receptionist list shows the 20 patients with the highest predicted no-show risk for next week, sorted by risk.",
    "- Data on the page is no older than 24 hours at 07:00 each weekday.",
]
_METRIC = [
    "Metric: no-show rate",
    "Definition: booked appointments with status \"no-show\", divided by all booked appointments not cancelled 24 hours or more before the start time.",
    "Grain: one row per clinic per appointment date",
    "Freshness: loaded by 06:00 each weekday, with data to the end of the previous day",
    "Source: appointments table in the booking system, nightly extract",
    "Data owner: head of patient access",
]
_SIGN = [
    "Decision owner: Amara Osei, clinic operations lead",
    "Signed off: 2026-03-02 by Amara Osei, version 1.0",
    "Change log: v1.0 2026-03-02 first signed version",
]
_T = "Saffrondale Clinics no-show dashboard"
PRESETS += [
    {"id": "stories", "label": "3 · Stories fixed",
     "note": "Constructed Saffrondale example. A decision statement and three stories that say who, what and why. The criteria are still the first draft's.",
     "text": "\n".join([_T + " (stories fixed)", _DEC] + _STORIES + _VAGUE_AC)},
    {"id": "criteria", "label": "4 · Criteria testable",
     "note": "Constructed Saffrondale example. Criteria rewritten so a builder can check each one.",
     "text": "\n".join([_T + " (criteria testable)", _DEC] + _STORIES + _TEST_AC)},
    {"id": "metric", "label": "5 · Metric defined",
     "note": "Constructed Saffrondale example. The no-show rate pinned down: definition, grain, freshness, source and owner.",
     "text": "\n".join([_T + " (metric defined)", _DEC] + _STORIES + _TEST_AC + _METRIC)},
    {"id": "signed", "label": "6 · Signed spec",
     "note": "Constructed Saffrondale example. The decision owner signs a dated version.",
     "text": "\n".join([_T + " v1.0", _DEC] + _STORIES + _TEST_AC + _METRIC + _SIGN)},
]


def ladder(sample_stories):
    out = {}
    for p in PRESETS:
        out[p["id"]] = check(p["text"])
        out[p["id"] + "+padded"] = check(pad(p["text"]))
    out["corpus"] = corpus(sample_stories)
    return out


def load_sample():
    txt = (ROOT / "assets" / "rqs-sample.js").read_text()
    data = json.loads(txt[txt.index("window.RQS_SAMPLE = ") + 20: txt.rindex(";")])
    return data


# ----------------------------------------------------------------------------- unit tests
TESTS = [
    # rule, fires?, text, why
    ("no-decision", True, "Decision: better visibility of no-shows", "a decision with no choice word"),
    ("no-decision", False, "Decision: the lead decides which patients get a call", "names a choice"),
    ("no-user", True, "Can we get a dashboard?", "no story line at all"),
    ("no-user", False, "As a nurse, I want to see my list, so that I can plan.", "one story"),
    ("well-formed", True, "I want to see an error when I cannot see recommendations.", "QUS US1: no role"),
    ("well-formed", False, "As a Member, I want to see an error, so that I know.", "role and means"),
    ("no-benefit", True, "As a receptionist, I want to see no-shows.", "no so-that"),
    ("no-benefit", False, "As a receptionist, I want to see no-shows, so that I can call.", "has so-that"),
    ("compound", True, "As a manager, I want a dashboard and a model, so that I can plan.", "two asks"),
    ("compound", False, "As a manager, I want a dashboard, so that I can plan and staff.", "'and' only in the ends"),
    ("not-minimal", True, "As a nurse, I want to see hours (split by product), so that I can plan.", "QUS US3-style bracket"),
    ("not-minimal", False, "As a nurse, I want to see hours, so that I can plan.", "role, means, ends only"),
    ("vague", True, "As a lead, I want a fast dashboard, so that I can act.", "fast, no number"),
    ("vague", False, "As a lead, I want the page in under 3 seconds, so that I can act.", "a number, no vague word"),
    ("vague", False, "- Loads fast: under 3 seconds at 50 users.", "quantity word with a number on the line"),
    ("untestable", True, "Acceptance criteria:\n- The model works well.", "nothing to observe"),
    ("untestable", False, "Acceptance criteria:\n- The list shows 20 patients.", "observable verb and a number"),
    ("untestable", True, "Given a clinic\nWhen I open the page\nThen it is good", "Then with nothing to check"),
    ("untestable", False, "Given a clinic\nWhen I open the page\nThen the page shows the rate", "Then shows"),
    ("no-criteria", True, "As a nurse, I want to see hours, so that I can plan.", "story but no criteria"),
    ("no-criteria", False, "Acceptance criteria:\n- The page shows 7 days.", "one criterion"),
    ("metric-undefined", True, "Metric: no-show rate", "named, not defined"),
    ("metric-undefined", False, "Metric: no-show rate\nNumerator: no-shows\nDenominator: booked appointments", "numerator and denominator"),
    ("no-grain", True, "A no-show dashboard", "data product, no grain"),
    ("no-grain", False, "A no-show dashboard\nGrain: one row per clinic per day", "grain field"),
    ("no-freshness", True, "A no-show dashboard\nFreshness: real-time", "freshness without a number"),
    ("no-freshness", False, "A no-show dashboard\nFreshness: loaded by 06:00 daily", "a number"),
    ("no-source", True, "A no-show dashboard\nSource: booking system", "source without an owner"),
    ("no-source", False, "A no-show dashboard\nSource: booking system\nData owner: patient access", "both"),
    ("no-signoff", True, "Decision owner: Amara Osei\nSigned off: soon", "no date"),
    ("no-signoff", False, "Decision owner: Amara Osei\nSigned off: 2026-03-02", "owner and date"),
]


def run_tests(verbose=True):
    fails = 0
    for rule, fires, text, why in TESTS:
        got = check(text)["byRule"][rule] > 0
        if got != fires:
            fails += 1
            if verbose:
                print("FAIL", rule, fires, why)
    covered = {r for r, _, _, _ in TESTS}
    both = {r for r in covered if any(t[0] == r and t[1] for t in TESTS) and any(t[0] == r and not t[1] for t in TESTS)}
    missing = [r for r in RULE_IDS if r not in both]
    if verbose:
        print(f"{len(TESTS) - fails}/{len(TESTS)} rule tests pass in python; rules without pass+fail: {missing}")
    return fails == 0 and not missing


def full_corpus(rawdir):
    sys.path.insert(0, str(ROOT / "materials"))
    from build_rqs_sample import read_raw  # noqa: E402
    allst = [s for _, ss in read_raw(rawdir) for s in ss]
    return corpus(allst)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ladder"
    if cmd == "ladder":
        print(json.dumps(ladder([s[1] for s in load_sample()["stories"]]), indent=1))
    elif cmd == "test":
        sys.exit(0 if run_tests() else 1)
    elif cmd == "write-tests":
        cases = [{"rule": r, "fires": f, "text": t, "desc": d} for r, f, t, d in TESTS]
        (ROOT / "materials" / "rqs_rule_tests.json").write_text(json.dumps(cases, indent=1) + "\n")
        print(len(cases), "cases written")
    elif cmd == "full-corpus":
        print(json.dumps(full_corpus(sys.argv[2]), indent=1))
