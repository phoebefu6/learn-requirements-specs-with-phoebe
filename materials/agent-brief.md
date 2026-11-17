# Agent brief - shared by every fan-out page of learn-requirements-specs-with-phoebe

Filled from `~/.claude/skills/course-builder/references/agent-brief.template.md` on 2026-11-16.
Internal build document: never link it from an audience page.

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file, return its path and one
line of coverage. No HTML in your reply.

## Read first, in this order

1. The template page. Copy its structure, classes, SVG grammar and quiz markup EXACTLY, including
   how many options each question has (FOUR options, "A · ...", "B · ...", "C · ...", "D · ..."):
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-requirements-specs-with-phoebe/courses/01-the-ask-behind-the-dashboard.html`
   For rhythm and the bench you may also skim
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-requirements-specs-with-phoebe/courses/04-the-spec-checker.html`
2. The source map: every verified fact, its evidence tier, per-session coverage, the seams and the
   bench canon. Use ONLY its facts and numbers; never invent a statistic; if a fact is missing, teach
   the uncertainty.
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-requirements-specs-with-phoebe/materials/official-course-map.md`
3. The stylesheet `:root` block for the palette tokens (first 30 lines):
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-requirements-specs-with-phoebe/assets/style.css`
4. If your page quotes a Saffrondale preset or a checker rule, check it in
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-requirements-specs-with-phoebe/materials/rqs_reference.py`
   (RULES, VAGUE, PATTERNS, PRESETS). Never invent a rule behaviour that is not there.

## Page skeleton (keep every component)

toolbar (crumb EXACTLY "learn-requirements-specs-with-phoebe / Session N of 6" with the repo name
linked to ../index.html, #toggle-all, #zoom-toggle) · masthead (eyebrow
"Learn Requirements &amp; Specs with Phoebe · Session N of 6", h1 with one `<span class="accent">`,
.sub, .chip-row with the level chip given in your outline, the two audience chips EXACTLY as the
template ("Managers, analysts, ops and product leads who ask for data products" and "Builders who
receive the ask" or "Builders who receive the spec"), `.chip.time` "45 min", .agenda a1-a4 with flex
weights 1/4/5/1) · main.wrap · section#intro (Part 0 "Where we start": kicker, .lede, .legend pills
as in the template, .callout.win "★ What you walk out with tonight.") · 3 Parts, each
`section.section#part-N` with section-kicker (klabel "Part N · covers ...", h2, `.tag.concept "N min
live"`), a `.lede`, ONE figure, `details.card` accordions (summary: `.mode.live` or `.mode.self`,
title, `.mini`, `.caret ▶`), and a `.callout.example` with `span.ex-pill` "Real world" in each Part ·
section#demo-1 Build-along (klabel "Build-along", h2, kicker `.tag.demo "★ 22 min · everyone
builds"`, .lede, ONE figure, `.steps > .step`, each step a `<p>` with the code box BELOW it as
`.prompt-box.good` carrying a `span.label` "★ Step N · ...") · section#exercise Homework (klabel
"Homework", h2 "Before session N+1" (session 6: "After the course" is NOT allowed; use "Your next
spec"), `.tag.exercise "30 min"`, ol of 4 items) · section#quiz (klabel "Check yourself", h2 "Three
questions", the passport line, 3 x `.quiz-q data-answer="0-based"` with `p.qtext`, four
`button.qopt`, `p.qwhy`; vary the correct letter across the three; one `p.quiz-score` after the
last) · section#official, klabel "Sources covered", h2 EXACTLY "What this session teaches, and where
it came from", `.covered > .covered-row` (pill solid ✓ / light ◐ + name + note), then the `.mono`
line EXACTLY "Every fact on this page, and its verification tier, is recorded in the course's source
map." · section.cheat#cheatsheet (h3 "Session N cheat sheet <span>· pin this</span>", .grid-2 of six
.cheat-item with b + span) · `.callout.next` with `.nx-pill` "Next session" · footer.pagefoot ·
scripts at the end exactly as the template if your page embeds the checker widget:
`<script src="../assets/rqs-sample.js?v=2"></script>` `<script src="../assets/rqs-live.js?v=2"></script>`
then `<script src="../assets/app.js?v=1"></script>`; if it does not embed the widget, only the app.js
line.

Head: copy the template's social meta block with this page's own title/description/url
(`https://phoebefu6.github.io/learn-requirements-specs-with-phoebe/courses/<file>`, og-image
`.../assets/og-cover.png`); `<title>Session N · <short title> - learn requirements specs with phoebe</title>`;
`<link rel="stylesheet" href="../assets/style.css?v=1">`. Nothing else external.

The checker widget: `<div class="rqs-bench" data-preset="<id>" data-mode="mini"></div>` inside a
build-along step (preset ids: ask, draft, stories, criteria, metric, signed). It renders the six preset
buttons, a text box, "Check my text", "Add more words", the headline count and the findings. Only
quote a number the widget prints for the exact text you give the learner (the canon below).

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm
practitioner voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines
is guidance about depth, never a target: never collapse whitespace, dissolve a list into a
paragraph, or drop a component to fit.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". State
  the professional norm directly with its reason. The two exact estate phrases above are the only
  self-references; "session 5" cross-references are fine. "These six sessions" is fine.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map or is labelled constructed. For constructed data print "your
  numbers will differ" only where a learner computes something themselves.
- Contested or missing evidence: teach the disagreement; never resolve what the literature has not.
- Citations in the exact form of the map's appendix; anything marked reported is "reported".
- NEVER "lottery" or "lotteries".
- No Chinese terms are needed on these pages.
- NO cross marks anywhere: never ✗ ✘ ✕ ❌ ×. Label states in words ("Before", "Vague", "Passes").
  The only glyphs allowed in pills are ✓ and ◐ in the covered rows.
- Titles, widget ids and class names must not collide with siblings. Your figures use the `sNx`
  prefix below; `rqs-` belongs to the bench engine; never define new CSS classes in the page.
- Course-specific: every mention of Saffrondale is labelled "Constructed Saffrondale example" or has
  "constructed" in the same sentence. Amara Osei is the constructed decision owner (fictional). Never
  Phoebe's employers, clients or projects. Do not invent other company cases; real-world stories
  come from the map only (Wake, Agile Alliance glossary, Cohn, Adams/Intercom, Lucassen et al. QUS
  and AQUSA, Cucumber Gherkin, dbt, Data Cards, Dantas 2018, Mars Climate Orbiter, Dalpiaz corpus).
- No patient data of any kind: Saffrondale numbers are constructed counts, never individual records
  with names.
- Tools (Jira, Linear, Confluence, Azure DevOps, Cucumber runners) are named only as a category in a
  Self-study card. No build-along needs an account: every build-along runs in the page.
- Seams: link, never reteach (one-card recap at most). Links are absolute https (list below).

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): #610017 (primary crimson) · #3D000E (deep) · #9E1C38
(mid) · #E7AAB7 (soft) · #FBEEF1 (tint) · #25141A (ink) · #5C474E (muted) · #CFC0C5 (faint) ·
#ECE2E5 (hairline) · #F5C518 (pencil yellow, a FILL only, never text) · #6B4E00 (yellow ink, text) ·
#FEF6D8 (yellow tint) · #FEFBFC (paper) · `#FFFFFF`. Do NOT use the universal reds (#991B1B #FEF2F2
#FCA5A5): the accent is already crimson; a wrong-way panel is a white box with a dashed stroke
(`stroke-dasharray="5 4"`) and the word "Before" or "Vague" in its heading.

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" xmlns="http://www.w3.org/2000/svg" role="img"
  aria-label="the data, not the shape">` > `<defs>` + `<style>` + content, then
  `<figcaption>🔍 Click to zoom - takeaway</figcaption>`. Grow H, never W.
- Prefix unique per figure, used for every class and id: `s{session}{letter}`, e.g. s2a, s2b, s2c,
  s2d for session 2's four figures (filter `s2aSk`, hatch `s2aHc`, arrow `s2aAr`, classes `.s2aH` ...).
- `<defs>` holds three things with the figure prefix P: a wobble filter `id="PSk"`
  (`feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="<int>"` +
  `feDisplacementMap scale="2.4" xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%"
  width="106%" height="106%"`), a hachure pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one
  #610017 line, opacity .5), an open arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none, #25141A
  stroke 1.6). ALL shapes sit inside ONE `<g filter="url(#PSk)" fill="none" stroke="#25141A"
  stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`; rects carry a tiny rotation (-4 to
  4 degrees for hand-placed items, under 1 for panels). Fills: white, #FBEEF1, the hachure for "the
  pile" or "the data" (never put text on a hachure fill), #610017 with white text for "the one source"
  (the signed spec, the definition), and #F5C518 ONLY for the one thing the figure is about. One doodle
  anchor per figure, simple strokes, never a mascot. Text classes: `.PH` 800 12px #25141A heading ·
  `.PL` 600 12px #25141A label · `.PS` 400 11px #5C474E · `.PB` 800 11px #6B4E00 · `.PV` 800 16-20px
  #3D000E value · `.PW` 800 12px #FFFFFF on a #610017 fill · `.PA` 700 11px #610017 axis caption ·
  `.PN` 400 12px #5C474E note. Text on a #F5C518 fill is #25141A (PH/PL), never white, never muted.
  Hand-stacked items must not overlap as painted rects (the gate flags a pile).
- ALL `<text>` outside the filtered group, sans stack, never below 10.5px.
- Fit: max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px; full-width note under 110 chars;
  40px between neighbouring point labels; bottom note 22px below the last row, H clears it by 8px. No
  line, arrow or curve may cross a label (the scanner flags line-through-text and text-out-of-box):
  route arrows through empty space, and keep every label inside its box with 10px to spare. When in
  doubt, shorten.
- Floor: one figure per Part plus one in the build-along (four figures). Draw the MECHANISM (which
  line triggers which question, where a definition splits two numbers, which change forces a
  re-sign), never a metaphor literally, never decoration.

## Voice and honesty

Every Part gets a real-world story from the map. Constructed cases say "constructed" on the page:
Saffrondale, its staff roles, its counts, Amara Osei, the two analysts in session 5. Nothing on the
page claims a measured outcome that was not measured.

## Cross-links (absolute URLs)

- AI PM a3: https://phoebefu6.github.io/learn-ai-pm-with-phoebe/courses/a3-specs-and-accountability.html
- AI PM b5: https://phoebefu6.github.io/learn-ai-pm-with-phoebe/courses/b5-the-spec-and-the-scorer.html
- Product thinking 01: https://phoebefu6.github.io/learn-product-thinking-with-phoebe/courses/01-the-job-not-the-feature.html
- Product thinking 02: https://phoebefu6.github.io/learn-product-thinking-with-phoebe/courses/02-what-people-ask-for.html
- System design 01: https://phoebefu6.github.io/learn-system-design-with-phoebe/courses/01-requirements-to-constraints.html
- Data literacy 04: https://phoebefu6.github.io/learn-data-literacy-with-phoebe/courses/04-metrics-and-kpi-trees.html
- Data thinking 01: https://phoebefu6.github.io/learn-data-thinking-with-phoebe/courses/01-the-question-behind-the-question.html
- Tech project PMO 01: https://phoebefu6.github.io/learn-tech-project-pmo-with-phoebe/courses/01-frame-the-initiative.html
- Analytics engineering b8: https://phoebefu6.github.io/learn-analytics-engineering-with-phoebe/courses/b8-marts-and-questions.html
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chain and session titles

Footer left: "Session N of 6 · learn-requirements-specs-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>"
Footer right: "<a href="PREV">← Prev: <title></a> &nbsp;·&nbsp; <a href="NEXT">Next: <title> →</a>"
(session 6: "← Prev: The data side: metric definitions, grain, freshness, sources" and
"<a href="../index.html">Course home →</a>").

Files and titles (card titles, fixed; h1 may be phrased differently but keeps the substance):
1. `01-the-ask-behind-the-dashboard.html` · The ask behind "a dashboard, and maybe a model"
2. `02-user-stories-who-what-why.html` · User stories that say who, what and why
3. `03-acceptance-criteria-a-builder-can-test.html` · Acceptance criteria a builder can test
4. `04-the-spec-checker.html` · The bench: spec checker
5. `05-metric-definitions-grain-freshness.html` · The data side: metric definitions, grain, freshness, sources
6. `06-the-one-page-spec-and-sign-off.html` · The one-page spec, sign-off and change control

## Bench canon you may quote (printed by the checker widget)

Six Saffrondale rungs: ask 9 (13 words), first draft 19 (68), stories fixed 11 (116), criteria
testable 4 (176), metric defined 1 (238), signed spec 0 (259). "Add more words": signed 0 -> 11
(327 words: 3 not-minimal + 8 vague), draft 19 -> 32 (126 words). Real stories (440-story sample):
no reason 38.6%, two asks 27.7%, vague 10.7%, extra notes 1.8%, role or want missing 0.5%, no finding
41.6%. Session-specific canon is in your outline. Quote nothing else from the bench.
