// Node twin of materials/rqs_reference.py: runs the browser engine (assets/rqs-live.js) headless.
//   node materials/rqs-node.js ladder > node.json    every preset, plain and padded, + the real-story corpus
//   node materials/rqs-node.js test                  the shared rule unit tests (rqs_rule_tests.json)
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const RQS = require(path.join(ROOT, "assets/rqs-live.js"));
const txt = fs.readFileSync(path.join(ROOT, "assets/rqs-sample.js"), "utf8");
const S = JSON.parse(txt.slice(txt.indexOf("window.RQS_SAMPLE = ") + 20, txt.lastIndexOf(";")));
const E = RQS.make(S.constants);
const cmd = process.argv[2] || "ladder";
if (cmd === "ladder") {
  process.stdout.write(JSON.stringify(E.ladder(S.presets, S.stories.map(s => s[1])), null, 1));
} else {
  const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "rqs_rule_tests.json"), "utf8"));
  let fails = 0;
  for (const c of cases) {
    const got = E.check(c.text).byRule[c.rule] > 0;
    if (got !== c.fires) { fails++; console.log("FAIL", c.rule, c.desc); }
  }
  console.log(`${cases.length - fails}/${cases.length} cases pass in node`);
  process.exit(fails ? 1 : 0);
}
