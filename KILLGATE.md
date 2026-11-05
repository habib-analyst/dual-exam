# KILLGATE — Project #118 `dual-exam` — PASS (all gates)

Source: arXiv 2610.31066 v2, "Dual Exam: Controlled Evaluation of
Multimodal Agents and World Models" (Rao et al.). Scripted analog;
$0, CPU only, no LLM calls, no images/video, no real telemetry.

## G0 — Harness: PASS
`src/dual_exam.py`: scripted agent + symbolic state simulator over
3-item goal-container tasks with planted decision errors (container
confusion) vs planted simulation errors (dropped effects), correction
retries, a coupled arm, and two isolated tracks (agent under a perfect
reference env; world under gold actions) with 3% measurement noise.

## G1 — Author-code recheck (fresh, by this builder, 2026-10-30): PASS
- Abstract page (arxiv.org/abs/2610.31066): title, authors (Zhefan Rao
  et al.), submitted 22 Oct 2026, last revised 28 Oct 2026 (v2) all match;
  NO author code link (only arXiv's own third-party toggles) and no
  release statement in the abstract.
- Full-text HTML v2 (1797 lines, find-tool validated): "github" matches
  ONLY task content (a GitHub-repo lookup task) + a SWE-bench citation;
  ZERO zenodo / 4open / "code is available" / "data is available" /
  supplement / "available at" / "we release" / anonymous matches;
  "replication" hits are methods words ("consistency check, not
  independent replication"), not a package.
- Conclusion: no author repo, no retrievable author package, no release
  sentence with a public location. G1 PASSES under both the narrow reading
  and the #100 lesson. No package was downloaded or inspected (none
  exists). If a located author package later appears, re-examine under
  the #100 precedent.

## Pilot gate: PASS (seed 118001, 100/category)
P1 coupled success 0.2525 (<= 0.55); P2 coupled audit accuracy 0.585
(<= 0.70); P3 isolated accuracy 0.965 (>= 0.80); P4 gap 0.38, CI
[0.31, 0.45] (>= 0.20). PILOT_PREREG.md was written before any pilot
number. The build is not vacuous: the coupled audit demonstrably
misattributes, and the tracks demonstrably separate.

## PREREG: locked before head-to-head, zero amendments
PILOT_PREREG < pilot < PREREG < headline by mtime. Decision rule "ANY
locked bar fails -> KILL". The only post-pilot code change recorded the
two track pass/fail booleans with identical RNG draw order (pilot numbers
recomputed identical, verified); no parameter, rule, or task-set change
after the pilot.

## G2 — Disease: PASS (3/3, fresh seed 118002, 250/category)
- D1: coupled success 0.269 (bar <= 0.40).
- D2: coupled audit attribution accuracy, single-fault: 0.572
  (bar <= 0.70).
- D3: track pass rates on the full mix: agent 0.489, world 0.500
  (bars >= 0.40 each) -- components show measurable signal while the
  coupled run fails.

## G3 — Mechanism + benign bound: PASS (5/5)
- M1: isolated attribution accuracy, single-fault: 0.932 (bar >= 0.85).
- M2: attribution gap 0.36, bootstrap CI [0.312, 0.408]
  (bars >= 0.20 / lo >= 0.10).
- M3: isolated accuracy per component: agent-only 0.94, world-only
  0.924 (bars >= 0.85 each).
- B1: clean-episode isolated "neither" rate 0.948 (bar >= 0.85);
  clean-episode coupled success 1.0 (bar >= 0.90).

## The failure mode, stated plainly
Coupled audit accuracy is 1.0 on agent-only episodes but 0.144 on
world-only episodes: world-model faults are systematically blamed on
the agent, because both faults manifest as final-state failure while
the confused agent shows no corrective response to demonstrate. Under
the vacuous-1.0 sensitivity reading, coupled accuracy would be 0.08 --
the primary 0.0 reading is the conservative one. The isolated tracks
attribute agent-only faults at 0.94 and world-only faults at 0.924.

## Determinism
SHA-256(results/headline.json) =
97f93e8211791bd40a1cf46ee541455bd0250aadf8dcd27217c9bb9879cced04.
Independent rerun on the same seed is byte-identical. Tests: 10 passed.

## Verdict: SHIP
REPO NEEDED: habib-analyst/dual-exam (builder does not push; the GitHub
App token cannot create repos).
