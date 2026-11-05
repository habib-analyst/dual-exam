# PILOT_PREREG — Project #118 `dual-exam` (arXiv 2610.31066 v2)

Written BEFORE any pilot number was observed. Pilot seed 118001,
100 episodes per fault category (400 total; 200 single-fault episodes
for attribution accuracy).

## Fixed design (G0, not to be changed after seeing pilot numbers)
- Symbolic state tasks: 3 items into the goal container, colours preserved.
- Fault categories, equal quarters: none / agent / world / both.
- Agent fault: container confusion, prob 0.8 per place action.
- World fault: effect dropped, prob 0.8 per place action.
- Correction: retry prob 0.7 per visible discrepancy, max 2 retries/item.
- Track measurement noise: 3% outcome flips per isolated track.
- Coupled audit rule (primary): attribute world iff state_consistency <
  corrective_response, else agent; 0 visible discrepancies scores
  corrective_response = 0.0 ("no corrective response demonstrated").
  Sensitivity: the vacuous-1.0 reading is reported alongside, but the
  primary bar uses the 0.0 reading.
- Isolated rule: agent-track fail + world-track pass -> agent; world-track
  fail + agent-track pass -> world; both fail -> both; both pass -> neither.
  Tracks use only their own outcomes, never ground truth.

## Pilot gates (ALL must pass, else KILL fast -- no tuning after)
- P1 (disease, coupled failure): coupled success <= 0.55.
- P2 (disease, attribution ambiguity): coupled audit attribution accuracy
  on single-fault episodes <= 0.70.
- P3 (mechanism, isolation works): isolated attribution accuracy on
  single-fault episodes >= 0.80.
- P4 (attribution gap): isolated - coupled gap >= 0.20.

If P2 fails (the coupled audit already attributes well), there is no
attribution gap and the build is vacuous -- KILL, do not re-pick the audit
rule, the fault probabilities, or the task set to manufacture a gap.
If P3 fails (the tracks cannot separate components), KILL likewise.

## Scope limits (stated before any number)
- Scripted analog only. The paper's figures (150-case coupled pilot 0%
  success, world-state consistency 26.6%, agent corrective response 9.2%,
  Agent Index 31.3, WM Overall 21.7) are CONTEXT ONLY, never claimed as
  reproduced.
- The "world model" is a symbolic state simulator, a weak proxy for a
  video world model.
- Isolated tracks measure role-specific performance on separate cases;
  per the paper's own §2.2 caveat, they do NOT imply causal attribution
  of coupled failures. The claim is diagnostic value of the two-track
  protocol, not retrospective blame for a coupled run.
- Differentiation: component attribution in evaluation design, not
  harness x agent blame (#85, one track), not trace truth (#56), not
  detector disagreement (#77), not audit certification (#111).
