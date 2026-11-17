# Learn Requirements & Specs with Phoebe

Six 45-minute sessions on writing requirements for data products you are not coding yourself:
the decision behind the ask, user stories, acceptance criteria a builder can test, metric
definitions with grain and freshness, and a signed one-page spec. A spec is finished when the
builder has no questions left.

- Running case: Saffrondale Clinics, a constructed network of six outpatient clinics (no real
  clinic, no patient data).
- Bench (session 4): a real spec checker in the browser. 14 rules, each finding printed as the
  question a builder would have to ask; base rates on 440 real user stories; an "Add more words"
  button that shows length is not precision.
- Real stories: Dalpiaz, F. (2018). Requirements data sets (user stories). Mendeley Data,
  doi:10.17632/7zbk8zsd8y.2, CC BY 4.0. Changes: ASCII-folded, trimmed, seeded sample of 20 per
  data set (440 of 1,680).
- `assets/rqs-live.js` (engine + widget) and `materials/rqs_reference.py` (Python twin) print
  identical findings; check with `materials/compare-ladder.py`.

Static HTML, no build step. Open `index.html`. By Phoebe Fu.
