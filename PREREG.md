# PREREG — Project #118 `dual-exam` (arXiv 2610.31066 v2)

Locked AFTER the pilot run and BEFORE any head-to-head run.
Decision rule: **ANY locked bar fails → KILL, no amendments.**
Post-hoc amendments are impermissible (the #97 veto).

## Pilot (seed 118001, 100 episodes per fault category, already observed)
- Coupled success 0.2525 (by fault: none 1.0, agent 0.0, world 0.01, both 0.0).
- Coupled audit attribution accuracy, single-fault: 0.585 overall
  (agent-only 1.0, world-only 0.17); vacuous-1.0 sensitivity: 0.085.
- Isolated attribution accuracy, single-fault: 0.965
  (agent-only 0.99, world-only 0.94).
- Attribution gap 0.38, bootstrap CI [0.31, 0.45].
- Track pass rates on the full mix: agent 0.4875, world 0.4875.
- Benign: isolated "neither" rate 0.91, coupled success on clean 1.0.
- Pilot gates P1-P4 all passed (see PILOT_PREREG.md). No parameter,
  rule, or task-set change was made after the pilot; the only code change
  after the pilot was recording the two track pass/fail booleans (same RNG
  draw order -- pilot numbers recomputed identical, verified).

## Head-to-head protocol (fresh seed 118002, 250 episodes per fault
category = 1000 total, 500 single-fault; paired bootstrap 2000, seed 999)
Same fixed design as PILOT_PREREG.md: fault quarters, confusion 0.8,
drop 0.8, retry prob 0.7 (max 2/item), track noise 3%, coupled audit rule
(0.0 reading for zero visible discrepancies; vacuous-1.0 as sensitivity
only), isolated rule from track outcomes only.

## G2 — Disease bars (coupled evaluation cannot diagnose)
- D1: coupled success <= 0.40 (pilot 0.2525).
- D2: coupled audit attribution accuracy on single-fault episodes
  <= 0.70 (pilot 0.585).
- D3: component tracks non-degenerate on the full mix: agent-track pass
  rate >= 0.40 AND world-track pass rate >= 0.40 (pilot 0.4875 each) --
  components show measurable signal while the coupled run fails.

## G3 — Load-bearing mechanism + benign bound
- M1: isolated attribution accuracy on single-fault episodes >= 0.85
  (pilot 0.965).
- M2: attribution gap (isolated - coupled) >= 0.20 AND bootstrap CI
  lower bound >= 0.10 (pilot 0.38, CI lo 0.31).
- M3: isolated attribution accuracy per component: agent-only >= 0.85
  AND world-only >= 0.85 (pilot 0.99 / 0.94).
- B1 (benign bound): clean-episode isolated "neither" rate >= 0.85
  (pilot 0.91) AND clean-episode coupled success >= 0.90 (pilot 1.0).

## Differentiation (stated before head-to-head, carried into PAPER.md)
- vs #85 harness-vcr: that attributes model-vs-harness blame on ONE
  track; this is two-track component isolation (agent vs world model).
- vs #56 tool-trace-audit: trace truth, not evaluation design.
- vs #77 detector-truth-gap: detector disagreement, not component
  isolation. vs #111 blindfold: certifier randomness, not adjudication
  or evaluation structure.

## Scope limits (stated before head-to-head)
- Scripted analog only. Paper figures (0% coupled pilot success, 26.6%
  state consistency, 9.2% corrective response, indices 31.3 / 21.7) are
  CONTEXT ONLY, never claimed as reproduced.
- The "world model" is a symbolic state simulator, a weak proxy for a
  video world model.
- Isolated tracks measure role-specific performance on separate cases;
  per the paper's §2.2 caveat, they do NOT imply causal attribution of
  coupled failures. The claim is diagnostic value of the two-track
  protocol.
