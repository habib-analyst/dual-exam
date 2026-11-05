# dual-exam (project #118)

Scripted analog of arXiv 2610.31066 v2 ("Dual Exam"): two-track component
isolation (agent vs world model) vs coupled evaluation, over symbolic
state tasks. The "world model" is a symbolic state simulator -- a weak
proxy for a video world model, stated everywhere. No LLM, no GPU, $0.

## Run
- Pilot: `python3 src/dual_exam.py 118001 100` (seed, episodes per fault
  category). Pilot gates live in `PILOT_PREREG.md` (written before any
  pilot number).
- Head-to-head: `python3 src/dual_exam.py 118002 250` (fresh seed).
- Tests: `python3 -m pytest tests/ -q` (10 tests).

## Headline (fresh seed 118002, 1000 episodes)
- Coupled success 0.269; coupled audit attribution accuracy 0.572
  (agent-only 1.0, world-only 0.144 -- world faults blamed on the agent).
- Isolated attribution accuracy 0.932 (agent-only 0.94, world-only 0.924).
- Attribution gap +0.36, bootstrap CI [0.312, 0.408].
- Benign: clean episodes attributed "neither" 0.948, coupled success 1.0.

## Scope honesty
Paper figures (0% coupled pilot success, 26.6% / 9.2% component scores,
indices 31.3 / 21.7) are context only, never claimed as reproduced.
Isolated tracks measure role-specific performance on separate cases; per
the paper's §2.2 caveat, they do NOT imply causal attribution of coupled
failures. The claim is diagnostic value of the two-track protocol.
