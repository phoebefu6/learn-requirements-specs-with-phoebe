/* rqs-live.js - the spec checker for learn-requirements-specs-with-phoebe, by Phoebe Fu.
   A real rule engine over text: it reads a story, a set of acceptance criteria or a whole one-page
   spec line by line, runs 14 rules and turns every finding into the question a builder would have
   to ask before starting. The word lists, field names and presets live in rqs-sample.js (generated
   from materials/rqs_reference.py, the Python twin); materials/compare-ladder.py checks that both
   engines print the same findings on every preset and on the real-story corpus.
   The stories in the corpus are real (Dalpiaz 2018, CC BY 4.0). Saffrondale Clinics is constructed.
   No dependencies. Runs in the browser and in node (module.exports). */
(function (root) {
  "use strict";

  function make(C) {
    var P = {};
    Object.keys(C.patterns).forEach(function (k) { P[k] = new RegExp(C.patterns[k], "i"); });
    var VAGUE = C.vague.map(function (v) { return { term: v[0], re: new RegExp(v[1], "i"), quantity: v[2], question: v[3] }; });
    var RULE_IDS = C.rules.map(function (r) { return r.id; });
    var QUESTION = {};
    C.rules.forEach(function (r) { QUESTION[r.id] = r.question; });

    function parse(text) {
      var out = [], section = null, chain = null;
      text.split("\n").forEach(function (raw, i) {
        var t = raw.trim();
        if (!t) return;
        var body = t.replace(P.bullet, "");
        var ln = { line: i + 1, body: body, kind: "text" };
        var m = P.field.exec(body);
        if (m && C.fields.indexOf(m[1].trim().toLowerCase()) >= 0) {
          var name = m[1].trim().toLowerCase();
          ln.kind = "field"; ln.field = name; ln.value = m[2].trim();
          section = Object.prototype.hasOwnProperty.call(C.sectionFields, name) ? C.sectionFields[name] : null;
          chain = null;
          out.push(ln); return;
        }
        var g = P.gherkin.exec(body);
        if (g) {
          var kw = g[1].toLowerCase();
          if (kw === "given" || kw === "when" || kw === "then") chain = kw;
          ln.kind = "criterion"; ln.kw = kw;
          ln.checked = kw === "then" || ((kw === "and" || kw === "but") && chain === "then");
          out.push(ln); return;
        }
        if (P.story_start.test(body) || P.story_want.test(body)) { ln.kind = "story"; out.push(ln); return; }
        if (section === "criteria") { ln.kind = "criterion"; ln.kw = "bullet"; ln.checked = true; }
        out.push(ln);
      });
      return out;
    }

    function vagueHits(body) {
      var hasDigit = P.digit.test(body), hits = [];
      VAGUE.forEach(function (v) { if (v.re.test(body) && !(v.quantity && hasDigit)) hits.push([v.term, v.question]); });
      return hits;
    }

    function storyFindings(body) {
      var f = [];
      var m = P.means.exec(body);
      if (!P.role.test(body) || !m) f.push(["well-formed", null, QUESTION["well-formed"]]);
      if (!P.ends.test(body)) f.push(["no-benefit", null, QUESTION["no-benefit"]]);
      if (m) {
        var rest = body.slice(m.index + m[0].length);
        var e = P.ends.exec(rest);
        var means = e ? rest.slice(0, e.index) : rest;
        if (P.compound.test(" " + means + " ")) f.push(["compound", null, QUESTION.compound]);
      }
      if (P.minimal.test(body.replace(/[.!? ]+$/, ""))) f.push(["not-minimal", null, QUESTION["not-minimal"]]);
      return f;
    }

    function fieldValue(lines, name) {
      for (var i = 0; i < lines.length; i++) if (lines[i].kind === "field" && lines[i].field === name && lines[i].value) return lines[i].value;
      return null;
    }

    function check(text) {
      var lines = parse(text), findings = [];
      function add(rule, line, term, question) { findings.push({ rule: rule, line: line, term: term || null, question: question || QUESTION[rule] }); }
      lines.forEach(function (ln) {
        var body = ln.body;
        if (ln.kind === "story") storyFindings(body).forEach(function (x) { add(x[0], ln.line, x[1], x[2]); });
        if (ln.kind === "criterion" && ln.checked) {
          if (!(P.digit.test(body) || P.quoted.test(body) || P.observable.test(body))) add("untestable", ln.line);
        }
        vagueHits(ln.kind === "field" ? ln.value : body).forEach(function (h) { add("vague", ln.line, h[0], h[1]); });
      });
      var dec = fieldValue(lines, "decision");
      if (!dec || !P.choice.test(dec)) add("no-decision", 0);
      if (!lines.some(function (l) { return l.kind === "story"; })) add("no-user", 0);
      if (!lines.some(function (l) { return l.kind === "criterion"; })) add("no-criteria", 0);
      if (P.data_product.test(text)) {
        var metric = fieldValue(lines, "metric");
        var defined = fieldValue(lines, "definition") || (fieldValue(lines, "numerator") && fieldValue(lines, "denominator"));
        if (!metric || !defined) add("metric-undefined", 0);
        if (!fieldValue(lines, "grain") && !P.grain_phrase.test(text)) add("no-grain", 0);
        var fr = fieldValue(lines, "freshness");
        if (!(fr && P.digit.test(fr)) && !lines.some(function (l) { return P.fresh_phrase.test(l.body); })) add("no-freshness", 0);
        if (!fieldValue(lines, "source") || !fieldValue(lines, "data owner")) add("no-source", 0);
      }
      var owner = fieldValue(lines, "decision owner"), signed = fieldValue(lines, "signed off");
      if (!(owner && P.letter.test(owner)) || !(signed && P.date.test(signed))) add("no-signoff", 0);

      findings.sort(function (a, b) {
        return (a.line - b.line) || (RULE_IDS.indexOf(a.rule) - RULE_IDS.indexOf(b.rule)) ||
          ((a.term || "") < (b.term || "") ? -1 : (a.term || "") > (b.term || "") ? 1 : 0);
      });
      var byRule = {};
      RULE_IDS.forEach(function (r) { byRule[r] = 0; });
      findings.forEach(function (x) { byRule[x.rule] += 1; });
      var words = text.trim() ? text.trim().split(/\s+/).length : 0;
      return { questions: findings.length, words: words, lines: lines.length, byRule: byRule, findings: findings };
    }

    function pad(text) {
      var kinds = {}, k = 0;
      parse(text).forEach(function (ln) { kinds[ln.line] = ln; });
      return text.split("\n").map(function (raw, i) {
        var ln = kinds[i + 1];
        if (ln && (ln.kind === "story" || (ln.kind === "criterion" && ln.checked))) {
          raw = raw.replace(/\s+$/, "") + " " + C.pad[k % C.pad.length]; k += 1;
        }
        return raw;
      }).join("\n");
    }

    function pct(count, n) { return n ? Math.floor((count * 2000 + n) / (2 * n)) / 10 : 0; }
    var CORPUS_RULES = ["well-formed", "no-benefit", "compound", "not-minimal", "vague"];

    function corpus(stories) {
      var n = stories.length, counts = {}, totalQ = 0, clean = 0;
      CORPUS_RULES.forEach(function (r) { counts[r] = 0; });
      stories.forEach(function (s) {
        var sf = storyFindings(s), vh = vagueHits(s);
        var rules = sf.map(function (x) { return x[0]; }).concat(vh.map(function () { return "vague"; }));
        totalQ += rules.length;
        var seen = {};
        rules.forEach(function (r) { if (!seen[r]) { seen[r] = 1; counts[r] += 1; } });
        if (!sf.length && !vh.length) clean += 1;
      });
      var rates = {};
      CORPUS_RULES.forEach(function (r) { rates[r] = { count: counts[r], pct: pct(counts[r], n) }; });
      return { n: n, rates: rates, clean: { count: clean, pct: pct(clean, n) }, questions: totalQ, perHundred: pct(totalQ, n) };
    }

    function ladder(presets, stories) {
      var out = {};
      presets.forEach(function (p) { out[p.id] = check(p.text); out[p.id + "+padded"] = check(pad(p.text)); });
      out.corpus = corpus(stories);
      return out;
    }

    return { rules: C.rules, parse: parse, check: check, pad: pad, corpus: corpus, ladder: ladder, storyFindings: storyFindings, vagueHits: vagueHits, CORPUS_RULES: CORPUS_RULES };
  }

  var API = { make: make };
  if (typeof module !== "undefined" && module.exports) { module.exports = API; return; }
  root.RQS = API;

  /* ------------------------------ the widget ------------------------------ */
  function h(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  var RULE_LABEL = { "well-formed": "Role or want missing", "no-benefit": "No reason given", "compound": "Two asks in one", "not-minimal": "Extra notes inside", "vague": "Vague word" };

  function mount(host, S, E) {
    var state = { preset: host.getAttribute("data-preset") || "draft", padded: false, custom: false, last: null, storyIx: 0 };
    var mode = host.getAttribute("data-mode") || "full";
    host.innerHTML = "";
    var head = h("div", "rqs-head");
    head.appendChild(h("h4", null, "The spec checker"));
    head.appendChild(h("p", "rqs-rail", "A real rule engine, running in this page: it reads your text line by line, applies 14 rules and turns every finding into the question a builder would have to ask. It checks wording and structure, not whether the request is a good idea. Saffrondale Clinics is a constructed example; the real stories are from Dalpiaz 2018 (CC BY 4.0). Rules marked lab-only are teaching rules, not a published standard."));
    host.appendChild(head);

    var presetRow = h("div", "rqs-presets");
    S.presets.forEach(function (p) {
      var b = h("button", "rqs-preset", p.label);
      b.type = "button"; b.setAttribute("data-id", p.id);
      b.addEventListener("click", function () { load(p.id); });
      presetRow.appendChild(b);
    });
    host.appendChild(presetRow);
    var note = h("p", "rqs-note"); host.appendChild(note);

    var ta = h("textarea", "rqs-text");
    ta.setAttribute("aria-label", "Spec text to check, one item per line");
    ta.spellcheck = false;
    host.appendChild(ta);
    var bar = h("div", "rqs-bar");
    var runBtn = h("button", "rqs-run", "Check my text"); runBtn.type = "button";
    var padBtn = h("button", "rqs-pad", "Add more words"); padBtn.type = "button";
    padBtn.setAttribute("aria-pressed", "false");
    bar.appendChild(runBtn); bar.appendChild(padBtn);
    host.appendChild(bar);

    var headline = h("div", "rqs-headline"); host.appendChild(headline);
    var list = h("ol", "rqs-findings"); host.appendChild(list);

    var corpusBox = null;
    if (mode === "full") {
      corpusBox = h("div", "rqs-corpus");
      host.appendChild(corpusBox);
    }

    function preset(id) { for (var i = 0; i < S.presets.length; i++) if (S.presets[i].id === id) return S.presets[i]; return S.presets[0]; }

    function load(id) {
      var p = preset(id);
      state.preset = p.id; state.custom = false; state.padded = false;
      state.base = p.text;
      render();
    }

    function render() {
      Array.prototype.forEach.call(presetRow.querySelectorAll(".rqs-preset"), function (b) { b.classList.toggle("is-on", b.getAttribute("data-id") === state.preset && !state.custom); });
      padBtn.classList.toggle("is-on", state.padded);
      padBtn.setAttribute("aria-pressed", state.padded ? "true" : "false");
      var base = state.base;
      var text = state.padded ? E.pad(base) : base;
      ta.value = text;
      note.textContent = state.custom ? "Your text." : preset(state.preset).note + (state.padded ? " Padded: one well-meaning sentence added to every story and checked criterion." : "");
      var r = E.check(text), plain = state.padded ? E.check(base) : null;
      state.last = r;
      headline.innerHTML = "";
      var big = h("div", "rqs-big");
      big.appendChild(h("b", "rqs-q", String(r.questions)));
      big.appendChild(h("span", null, r.questions === 1 ? " open builder question" : " open builder questions"));
      headline.appendChild(big);
      var two = h("p", "rqs-two");
      two.appendChild(h("span", null, r.words + (r.words === 1 ? " word, " : " words, ") + r.lines + (r.lines === 1 ? " line checked" : " lines checked")));
      if (plain) two.appendChild(h("span", "rqs-delta", "Before padding: " + plain.words + " words, " + plain.questions + " questions. More words, " + (r.questions > plain.questions ? "more" : r.questions === plain.questions ? "the same" : "fewer") + " questions."));
      headline.appendChild(two);
      if (r.questions === 0) headline.appendChild(h("p", "rqs-done", "Zero open questions: every rule passes. A builder can start without guessing."));
      list.innerHTML = "";
      r.findings.forEach(function (x) {
        var li = h("li", "rqs-f rqs-" + x.rule);
        var tag = h("span", "rqs-where", x.line ? "Line " + x.line : "Whole spec");
        li.appendChild(tag);
        var rule = null;
        for (var i = 0; i < E.rules.length; i++) if (E.rules[i].id === x.rule) rule = E.rules[i];
        li.appendChild(h("b", "rqs-rname", rule.name + (x.term ? ": \"" + x.term + "\"" : "")));
        li.appendChild(h("span", "rqs-ask", x.question));
        li.appendChild(h("span", "rqs-origin", rule.origin));
        list.appendChild(li);
      });
      host.setAttribute("data-questions", String(r.questions));
      host.setAttribute("data-words", String(r.words));
    }

    function renderCorpus() {
      if (!corpusBox) return;
      var stories = S.stories.map(function (s) { return s[1]; });
      var c = E.corpus(stories);
      corpusBox.innerHTML = "";
      corpusBox.appendChild(h("span", "rqs-clabel", "Real stories: base rate per rule"));
      corpusBox.appendChild(h("p", "rqs-cnote", c.n + " real user stories, a seeded sample of 20 from each of " + S.datasets.length + " public projects (" + S.totalStories + " stories in the full set). Source: " + S.source + ", " + S.licence + ". Changes: " + S.changes));
      var t = h("table", "clean rqs-table");
      var thead = h("thead"), tr0 = h("tr");
      ["Rule", "Stories that trigger it", "Share"].forEach(function (x) { tr0.appendChild(h("th", null, x)); });
      thead.appendChild(tr0); t.appendChild(thead);
      var tb = h("tbody");
      E.CORPUS_RULES.forEach(function (r) {
        var tr = h("tr");
        tr.appendChild(h("td", null, RULE_LABEL[r]));
        tr.appendChild(h("td", "rqs-num", c.rates[r].count + " of " + c.n));
        var td = h("td", "rqs-num"); td.appendChild(h("b", null, c.rates[r].pct.toFixed(1) + "%")); tr.appendChild(td);
        tb.appendChild(tr);
      });
      var trc = h("tr", "rqs-cleanrow");
      trc.appendChild(h("td", null, "No finding at all"));
      trc.appendChild(h("td", "rqs-num", c.clean.count + " of " + c.n));
      var tdc = h("td", "rqs-num"); tdc.appendChild(h("b", null, c.clean.pct.toFixed(1) + "%")); trc.appendChild(tdc);
      tb.appendChild(trc);
      t.appendChild(tb); corpusBox.appendChild(t);
      corpusBox.appendChild(h("p", "rqs-cnote", c.questions + " open questions across the " + c.n + " stories, " + c.perHundred.toFixed(1) + " per 100 stories. The story rules only: the spec-level rules need a whole spec."));
      var row = h("div", "rqs-bar");
      var draw = h("button", "rqs-preset", "Check the next real story"); draw.type = "button";
      var show = h("div", "rqs-story");
      row.appendChild(draw); corpusBox.appendChild(row); corpusBox.appendChild(show);
      function showStory() {
        var s = S.stories[state.storyIx];
        show.innerHTML = "";
        show.appendChild(h("span", "rqs-clabel", "Real story " + (state.storyIx + 1) + " of " + c.n + " · project " + S.datasets[s[0]]));
        show.appendChild(h("p", "rqs-quote", s[1]));
        var f = E.storyFindings(s[1]).map(function (x) { return x[0]; }).concat(E.vagueHits(s[1]).map(function (v) { return "vague: \"" + v[0] + "\""; }));
        show.appendChild(h("p", "rqs-cnote", f.length ? "Findings: " + f.map(function (x) { return RULE_LABEL[x] || ("Vague word" + x.slice(5)); }).join(", ") : "No finding from the story rules."));
      }
      draw.addEventListener("click", function () { state.storyIx = (state.storyIx * 37 + 11) % c.n; showStory(); });
      showStory();
      host.setAttribute("data-corpus-n", String(c.n));
    }

    runBtn.addEventListener("click", function () { state.custom = true; state.padded = false; state.base = ta.value; render(); });
    padBtn.addEventListener("click", function () { state.padded = !state.padded; render(); });
    load(state.preset);
    renderCorpus();
    return {
      load: load,
      setPadded: function (on) { state.padded = !!on; render(); return state.last; },
      runText: function (t) { state.base = t; state.custom = true; state.padded = false; render(); return state.last; },
      state: function () { return state.last; },
      corpus: function () { return E.corpus(S.stories.map(function (s) { return s[1]; })); }
    };
  }

  function init() {
    var S = root.RQS_SAMPLE;
    var hosts = document.querySelectorAll(".rqs-bench");
    var apis = [];
    if (!S) { Array.prototype.forEach.call(hosts, function (el) { el.textContent = "Bench data did not load."; }); return; }
    var E = make(S.constants);
    root.RQS_ENGINE = E;
    Array.prototype.forEach.call(hosts, function (el) { apis.push(mount(el, S, E)); });
    root.RQS_BENCH = apis[0] || null;
    root.RQS_BENCHES = apis;
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})(typeof window !== "undefined" ? window : this);
