# Official course map - learn-requirements-specs-with-phoebe

Internal build document (never linked from an audience page). Written 2026-11-16 before any page.
Bucket sys, single-track 6 x 45 min, audience both (requesters and builders), public.

Angle: a spec is finished when the builder has no questions left. Across the six sessions: how many
questions would a builder have to ask before starting, and which of them would they guess instead?

Running case: **Constructed Saffrondale example** - Saffrondale Clinics, 6 outpatient clinics
(constructed; no real patient data). The ask: "a no-show dashboard, and maybe a model". The running
artifact is Saffrondale's one-page spec, which grows each session. The constructed decision owner is
Amara Osei, clinic operations lead (fictional). Every mention on a page says "constructed".

## Evidence tiers

- **Read at source** - the text was fetched and read on 2026-11-16 (quote under 15 words).
- **Reported** - a secondary source or a title page only; say "reported" on the page.
- **Constructed** - Saffrondale and everything in it.
- **Measured** - printed by the session 4 bench (canon below); only these numbers may be quoted.

## Verified facts

### User stories and INVEST
- Bill Wake, "INVEST in Good Stories, and SMART Tasks", xp123.com, 17 August 2003. **Read at source.**
  Independent, Negotiable, Valuable, Estimable, Small ("at most a few person-weeks"), Testable.
  "A good story is testable." Also SMART for tasks: Specific, Measurable, Achievable, Relevant,
  Time-boxed. Wake also says non-functional requirements (performance, usability) can be treated
  as needing tests (read at source, paraphrase). Note: Lucassen et al. 2016 expand the S as "Scalable"; Wake's own article says Small.
  Teach Wake's word.
- Agile Alliance glossary, "User Stories". **Read at source.** Origins listed: 1998 (XP, "like use
  cases"), 2001 role-feature-benefit template and the "3 C's" model, 2003 INVEST, 2006
  Given-When-Then. Pitfalls listed include treating a story as a document, and that detail should
  grow as the story nears implementation. "A user story is not a document." The page does not name
  who coined the 3 C's (Ron Jeffries is the usual attribution: **reported**, do not state as read).
- Mike Cohn, "Advantages of the As a user, I want user story template", Mountain Goat Software blog.
  **Read at source.** Template created by Rachel Davies at Connextra (UK) in the early 2000s. Cohn
  does not consider "so that" mandatory ("sometimes it just doesn't add any value") yet writes it in
  62 of 64 stories in a recent backlog.
- Paul Adams, "How we accidentally invented Job Stories", Intercom blog, 28 June 2016. **Read at
  source.** Format: When ___, I want to ___, so I can ___. Critique of user stories: formatted to
  describe functionality rather than motivation. Alan Klement named and popularised the format
  (**reported** from search results).
- Mike Cohn, "Job Stories Offer a Viable Alternative to User Stories". **Read at source.** Writes
  both; job stories likely the better approach when users' needs are not very distinct.
- CONTESTED (teach the disagreement, never resolve): stories for data work at all. Story camp:
  role-feature-benefit keeps the who and why on the card (Cohn). Job-story camp: the situation
  and motivation matter more than the persona (Adams). Plain problem statement camp: for a
  dashboard or a metric the user is often one person, so a decision statement may carry more than a
  story. Also contested: whether "so that" is required (QUS: ends optional, "optimally"; Cohn: not
  mandatory; the bench's no-benefit rule is lab-only and says so).

### Quality User Story framework (QUS) and AQUSA
- Lucassen, G., Dalpiaz, F., van der Werf, J.M.E.M., Brinkkemper, S. (2016). Improving agile
  requirements: the Quality User Story framework and tool. Requirements Engineering 21, 383-403.
  doi:10.1007/s00766-016-0250-x. **Read at source** (author manuscript PDF on Dalpiaz's Utrecht page;
  the Springer page is behind a login redirect, so cite the journal version for page numbers).
- 13 criteria in three groups. Syntactic: Well-formed (role and means), Atomic (exactly one
  feature), Minimal (nothing more than role, means and ends). Semantic: Conceptually sound,
  Problem-oriented, Unambiguous, Conflict-free. Pragmatic: Full sentence, Estimatable, Unique,
  Uniform, Independent, Complete.
- AQUSA v1 implements the syntactic criteria plus some pragmatic ones and EXCLUDES the semantic ones
  ("they require deep understanding of requirements' content"). Atomic check: conjunctions
  "and, &, +, or" in role or means, then a parser checks both sides. Minimal: text after a dot,
  hyphen, question mark or asterisk, and text in brackets.
- Evaluation: 1,023 user stories from 18 organisations. Overall recall 93.8%, precision 72.2%
  (micro). Per criterion (Table 5): Atomic recall 82.9% precision 51.18%; Minimal 95.5% / 69.52%;
  Well-formed 95.7% / 42.31%; Uniform 95.4% / 87.09%; Unique 100% / 100%. Goal named: the "Berry
  Recall Condition" (close to 100% recall for an NLP tool in RE to be useful).
- Teaching use: a lint that catches most defects still raises false alarms, and the semantic
  defects (ambiguity) are exactly the ones a tool struggles with. The bench's "compound" rule is
  cruder than AQUSA's Atomic check (no parser), so it over-flags: say so.

### Acceptance criteria, Gherkin, definition of done
- Cucumber, Gherkin reference. **Read at source.** Keywords: Feature, Rule, Example/Scenario,
  Given, When, Then, And, But, Background, Scenario Outline/Template, Examples. Given = initial
  context; When = an event or action; Then = an expected outcome. "You should only verify an outcome
  that is observable for the user." Rule (Gherkin 6+) = one business rule, grouping its examples.
- Agile Alliance glossary, "Given When Then". **Read at source.** "A template intended to guide the
  writing of acceptance tests for a User Story." Dated 2006 on the user-stories page. The page does
  not name Dan North / Chris Matts: attribution **reported**.
- Agile Alliance glossary, "Definition of Done". **Read at source.** A list of criteria that must be
  met before an increment is done; 2002 Wake raised inconsistent meanings of "done"; 2005 Scrum
  trainings ran DoD exercises; by 2007 widespread. Pitfall: unwritten DoD loses most of its value.
  DoD applies to every item; acceptance criteria are per story (the distinction is the common
  practitioner reading; the glossary page itself does not compare them).

### Requirements characteristics
- ISO/IEC/IEEE 29148:2018, clause 5.2.5 "Characteristics of individual requirements" and 5.2.6
  "...of a set of requirements". Clause numbers **read at source** (table of contents of the iTeh
  sample); the characteristic list (necessary, appropriate, unambiguous, complete, singular,
  feasible, verifiable, correct, conforming) is **reported**. Say "reported".

### Data side
- dbt Semantic Layer, "Metrics overview" (docs.getdbt.com). **Read at source.** Metric fields: name
  (required), description, type (required), label, config, filter. Types: simple, ratio, cumulative,
  derived, conversion. A ratio metric requires numerator and denominator; a top-level filter applies
  to both, a filter inside one side applies to that side only. Native time grain is set on the time
  dimension column; the rollup grain (day, week, month) is chosen at query time. Cited as ONE format
  for writing a metric down; never taught (analytics engineering owns it).
- Pushkarna, M., Zaldivar, A., Kjartansson, O. (2022). Data Cards: Purposeful and Transparent Dataset
  Documentation for Responsible AI. FAccT 2022; arXiv:2204.01075. **Read at source** (arXiv abstract):
  summaries of upstream sources, collection and annotation methods, intended use and decisions that
  affect model performance; lessons from deploying over 20 Data Cards. Venue: the arXiv page says
  submitted to FAccT 2022; the ACM page returned 403 (published proceedings DOI
  10.1145/3531146.3533231 **reported**).
- Dantas, L.F., Fleck, J.L., Cyrino Oliveira, F.L., Hamacher, S. (2018). No-shows in appointment
  scheduling - a systematic literature review. Health Policy 122(4), 412-421.
  doi:10.1016/j.healthpol.2018.02.002. **Read at source** (PubMed abstract): 727 records retrieved,
  105 studies analysed; average no-show rate "of the order of 23%", highest in Africa (43.0%),
  lowest in Oceania (13.2%); most common determinants: high lead time and prior no-show history.
  The abstract does NOT discuss how studies define a no-show: never claim it does. The "same name,
  two numbers" lesson on session 5 is carried by the constructed two-analyst example.

### Real-world failure story
- NASA Mars Climate Orbiter Mishap Investigation Board, Phase I Report (10 November 1999). **Read at
  source** (llis.nasa.gov PDF). Contact lost 23 September 1999. Root cause: ground software
  "SM_FORCES" produced thruster impulse data in English units (pound-force seconds) instead of the
  metric units (newton-seconds) the Software Interface Specification required; the trajectory
  modelers assumed metric "per the requirements". Small-forces delta-V low by a factor of 4.45.
  Lesson used here: the requirement WAS written; nobody checked the delivered file against it.
  Acceptance criteria are how a written requirement gets checked (session 3).

### The real-story corpus
- Dalpiaz, F. (2018). Requirements data sets (user stories). Mendeley Data. Current version 2
  (2024-12-19), doi:10.17632/7zbk8zsd8y.2 (version 1, 2018: doi:10.17632/7zbk8zsd8y.1). **Read at
  source** (public API). Licence **CC BY 4.0** (read on the record). 22 files, 1,680 non-empty story
  lines (the description says "22 data set of 50+ requirements each"). Curator note: gathered from
  web sources, non-recent data, a subset sampled. Originally used for ambiguity detection with
  REVV-Light. Downloaded files' sha256 matched the API listing (22 of 22).
- Shipped sample: ASCII-folded, 20 per data set with random.Random(2018), 440 stories,
  assets/rqs-sample.js 74.5 KB. Changes listed on the widget (CC BY asks for it).

## Bench canon (session 4, measured; python == node, 803 values, planted fault caught)

Spec checker, 14 rules. Headline = open builder questions (one per finding).

| Rung (Constructed Saffrondale example) | Open questions | Words | Padded ("Add more words") |
|---|---|---|---|
| 1 The one-line ask | 9 | 13 | 9 (13 words; nothing to pad) |
| 2 First draft | 19 | 68 | 32 (126 words) |
| 3 Stories fixed | 11 | 116 | 23 (174 words) |
| 4 Criteria testable | 4 | 176 | 15 (244 words) |
| 5 Metric defined | 1 | 238 | 12 (306 words) |
| 6 Signed spec | 0 | 259 | 11 (327 words) |

Per-rule on rungs:
- Ask 9: no-decision, no-user, vague "maybe", no-criteria, metric-undefined, no-grain, no-freshness,
  no-source, no-signoff.
- First draft 19: no-decision 1, no-benefit 3, compound 1, vague 6 (real-time, user-friendly, fast,
  easy, accurate, up to date), untestable 3, metric-undefined, no-grain, no-freshness, no-source,
  no-signoff.
- Stories fixed 11: vague 3 (easy, accurate, up to date), untestable 3, + the 5 data/sign-off rules.
- Criteria testable 4: metric-undefined, no-grain, no-source, no-signoff (freshness passes via the
  criterion "no older than 24 hours").
- Metric defined 1: no-signoff. Signed 0.
- Signed + padded 11: not-minimal 3, vague 8. (Padding with "accurate and up to date" next to a
  number does not fire the quantity words: honest nuance.)
- Teaching point: the one-line ask scores LOWER (9) than the first draft (19). The checker can only
  count what is written; writing surfaced the hidden questions. The number that matters is the one
  at handover.

Real-story base rates (440-story sample, printed by the widget):
| Rule | Stories | Share |
|---|---|---|
| Role or want missing (well-formed) | 2 | 0.5% |
| No reason given (no-benefit, lab-only) | 170 | 38.6% |
| Two asks in one (compound) | 122 | 27.7% |
| Extra notes inside (not-minimal) | 8 | 1.8% |
| Vague word | 47 | 10.7% |
| No finding at all | 183 | 41.6% |
350 open questions across 440 stories, 79.5 per 100 stories.

Full corpus (python only, NOT printed by the widget, map reference only, never quote on a page):
1,680 stories: well-formed 0.4%, no-benefit 42.3%, compound 26.9%, not-minimal 1.8%, vague 10.5%,
clean 39.8%. The sample tracks the full set within 4 points on every rule.

Vague words found most in the sample: easy 17, quick 10, accurate 5, up to date 4.

Planted fault: adding the criterion line "- The page loads fast." to the signed spec gives 2
questions (vague "fast" + untestable). Appending ", fast" to the receptionist criterion gives 0:
that line already carries a number (20), so the quantity word is exempt. Python check, 2026-11-16.

## Per-session coverage

1. **The ask behind "a dashboard, and maybe a model"** (green). Decision a data product serves, who
   acts, what changes; a guessed requirement and its cost (builder guesses vs asks). Product-thinking
   recap in one card + link. Real world: Mars Climate Orbiter is s3's; s1 uses Dantas 2018 (no-shows
   are a real, costly problem: average of the order of 23%) and the Agile Alliance pitfall.
   Build-along: Saffrondale's ask -> decision statement (rung 1 -> the Decision line). Checker
   rung 1 = 9 questions.
2. **User stories that say who, what and why** (green). Connextra template (Cohn), 3 C's (glossary,
   attribution reported), INVEST (Wake), splitting, stories vs tasks (Wake SMART tasks), QUS
   criteria. Contested: stories for data work; job stories (Adams, Cohn). Build-along: rewrite 5
   vague stories (constructed). Rungs 2 -> 3 (19 -> 11).
3. **Acceptance criteria a builder can test** (yellow). Given/When/Then (Gherkin reference),
   rule-based criteria (Rule keyword), non-functional criteria (freshness, latency, access), DoD
   (glossary). Real world: Mars Climate Orbiter. Build-along: criteria for the no-show dashboard.
   Rungs 3 -> 4 (11 -> 4).
4. **The bench: spec checker** (orange). All rungs, the anti-lever, the real-story base rates, the
   AQUSA comparison (precision 72.2%, Atomic 51.18%).
5. **The data side: metric definitions, grain, freshness, sources** (orange). Metric definition
   (numerator, denominator, filters, time window, grain), dbt ratio metric as one format, the
   "same name, two numbers" failure (constructed two-analyst example: the analysts' numbers are
   constructed, labelled), freshness SLA, source and owner, Data Cards for model requirements.
   Rungs 4 -> 5 (4 -> 1).
6. **The one-page spec, sign-off and change control** (red). One-page template, decision owner
   sign-off, versioned changes, what triggers a re-sign; capstone: signed spec scored 0, then the
   padded version 11. Link system-design 01 for what happens next.

## Seams (pick the side out loud, absolute links, never reteach)
- AI PM a3 / b5: https://phoebefu6.github.io/learn-ai-pm-with-phoebe/courses/a3-specs-and-accountability.html ,
  https://phoebefu6.github.io/learn-ai-pm-with-phoebe/courses/b5-the-spec-and-the-scorer.html
  (specs for AI products; here: data products written by non-coders).
- Product thinking 01-02: https://phoebefu6.github.io/learn-product-thinking-with-phoebe/courses/01-the-job-not-the-feature.html ,
  https://phoebefu6.github.io/learn-product-thinking-with-phoebe/courses/02-what-people-ask-for.html
  (s1 recaps in one card).
- System design 01: https://phoebefu6.github.io/learn-system-design-with-phoebe/courses/01-requirements-to-constraints.html (s6 links).
- Data literacy 04 metrics: https://phoebefu6.github.io/learn-data-literacy-with-phoebe/courses/04-metrics-and-kpi-trees.html
- Data thinking 01: https://phoebefu6.github.io/learn-data-thinking-with-phoebe/courses/01-the-question-behind-the-question.html
- Tech project PMO 01: https://phoebefu6.github.io/learn-tech-project-pmo-with-phoebe/courses/01-frame-the-initiative.html
- Analytics engineering b8 (semantic layer): https://phoebefu6.github.io/learn-analytics-engineering-with-phoebe/courses/b8-marts-and-questions.html
- Asking the right questions as a DA, s6 (the brief): https://phoebefu6.github.io/learn-asking-right-questions-as-da-with-phoebe/courses/06-the-mock-meeting-and-the-brief.html
  (not in the brief's seam table; found by grep. They own the discovery meeting; here: the written spec).

## Not covered (honest list)
- Jira, Linear, Confluence, Azure DevOps templates: named as a category in Self-study only.
- Use cases (Cockburn), formal SRS documents, requirements traceability matrices, model-based RE.
- Estimation and story points; backlog prioritisation methods (product-thinking owns cut decisions).
- BDD tooling (running Gherkin with Cucumber); only the writing of criteria is taught.
- ISO 29148 in depth (reported list only); regulated-domain requirements (medical device, safety).
- The semantic QUS criteria beyond Unambiguous are taught as a checklist, not checked by the bench.

## Citation appendix (exact form for pages)
- Wake, B. (2003). INVEST in Good Stories, and SMART Tasks. xp123.com.
- Agile Alliance. Glossary: User Stories; Given When Then; Definition of Done. agilealliance.org.
- Cohn, M. Advantages of the "As a user, I want" user story template. mountaingoatsoftware.com.
- Cohn, M. Job Stories Offer a Viable Alternative to User Stories. mountaingoatsoftware.com.
- Adams, P. (2016). How we accidentally invented Job Stories. Intercom blog.
- Lucassen, G., Dalpiaz, F., van der Werf, J.M.E.M., Brinkkemper, S. (2016). Improving agile
  requirements: the Quality User Story framework and tool. Requirements Engineering 21, 383-403.
- Cucumber. Gherkin reference. cucumber.io/docs/gherkin/reference.
- ISO/IEC/IEEE 29148:2018, clause 5.2.5 (reported).
- dbt Labs. Metrics overview, dbt Semantic Layer. docs.getdbt.com.
- Pushkarna, M., Zaldivar, A., Kjartansson, O. (2022). Data Cards. FAccT 2022 / arXiv:2204.01075.
- Dantas, L.F. et al. (2018). No-shows in appointment scheduling. Health Policy 122(4), 412-421.
- NASA (1999). Mars Climate Orbiter Mishap Investigation Board Phase I Report.
- Dalpiaz, F. (2018). Requirements data sets (user stories). Mendeley Data, doi:10.17632/7zbk8zsd8y.2. CC BY 4.0.
