"""Dual Exam analog (project #118): two-track component isolation vs coupled evaluation.

Scripted analog only. Symbolic state tasks: 3 items must end in the goal
container with colours preserved. No LLM, no images/video, no real telemetry.
The "world model" is a symbolic state simulator -- a weak proxy for a video
world model, stated everywhere.

Fault model (fixed in G0, before any pilot number):
- Per-episode fault category, seeded: none / agent / world / both (equal quarters).
- Agent fault: systematic container confusion -- at each place action the
  agent chooses the decoy container with prob AGENT_CONFUSION (else goal).
  The agent's expectation is the decoy, so it "corrects" goal placements
  into the decoy. It never perceives its own confusion as a discrepancy
  except when it accidentally places in the goal container.
- World fault: persistent per-action corruption -- at each place action the
  world drops the effect with prob WORLD_DROP (else applies it). The agent
  sees the mismatch and retries (prob CORRECT_P, max MAX_RETRIES per item);
  retries are subject to the same drop probability.
- Track measurement noise: each isolated-track outcome is flipped with prob
  TRACK_NOISE (reference mechanisms are not assumed error-free, paper §6.3).

Attribution rules (fixed in G0):
- Coupled audit rule (primary coupled baseline): from the coupled trajectory
  only, state_consistency = fraction of 6 final checks passed (3 locations +
  3 colours); corrective_response = corrections attempted / discrepancies
  visible, with 0 visible discrepancies scored as 0.0 ("no corrective
  response demonstrated"). Attribute to world if consistency < response,
  else to agent. (Sensitivity: the vacuous-1.0 reading is reported alongside.)
- Isolated rule: agent-track fail + world-track pass -> agent; world-track
  fail + agent-track pass -> world; both fail -> both; both pass -> neither.
  Tracks use only their own track outcomes, never ground truth.
"""

import json
import random

ITEMS = ["passport", "medicine", "charger"]
GOAL = "backpack_C"
DECOY = "pouch_D"
COLOURS = {"passport": "blue", "medicine": "white", "charger": "black"}

AGENT_CONFUSION = 0.8
WORLD_DROP = 0.8
CORRECT_P = 0.7
MAX_RETRIES = 2
TRACK_NOISE = 0.03
FAULTS = ["none", "agent", "world", "both"]


def _place(agent_fault, world_fault, rng):
    """Simulate one coupled episode. Returns dict of trajectory facts."""
    # state: item -> (location, colour); start: origin
    loc = {it: "origin" for it in ITEMS}
    colour = dict(COLOURS)
    discrepancies = 0
    corrections = 0
    for item in ITEMS:
        # agent chooses a container
        if agent_fault and rng.random() < AGENT_CONFUSION:
            chosen = DECOY
        else:
            chosen = GOAL
        expected = chosen  # agent's expectation is its own choice
        attempts = 0
        while True:
            attempts += 1
            # world applies (or drops) the placement
            if world_fault and rng.random() < WORLD_DROP:
                applied = loc[item]  # effect dropped: stays put
            else:
                applied = chosen
            loc[item] = applied
            if applied != expected:
                discrepancies += 1
                if attempts <= MAX_RETRIES and rng.random() < CORRECT_P:
                    corrections += 1
                    # retry: agent re-issues the same choice
                    continue
            break
    checks = sum(1 for it in ITEMS if loc[it] == GOAL)
    checks += sum(1 for it in ITEMS if colour[it] == COLOURS[it])
    success = all(loc[it] == GOAL for it in ITEMS) and all(
        colour[it] == COLOURS[it] for it in ITEMS
    )
    consistency = checks / 6.0
    response = (corrections / discrepancies) if discrepancies else 0.0
    response_vacuous = (corrections / discrepancies) if discrepancies else 1.0
    return {
        "success": success,
        "consistency": consistency,
        "response": response,
        "response_vacuous": response_vacuous,
        "discrepancies": discrepancies,
        "corrections": corrections,
        "locations": loc,
    }


def coupled_attribution(ep):
    """Naive audit rule: blame the component with the worse audit score."""
    return "world" if ep["consistency"] < ep["response"] else "agent"


def coupled_attribution_vacuous(ep):
    return "world" if ep["consistency"] < ep["response_vacuous"] else "agent"


def _track_outcome(fault_present, rng):
    """Isolated-track pass/fail for one component.

    The track directly measures its component: it fails iff the component is
    faulty (agent confusion under a perfect reference env; world drops under
    gold actions), modulo TRACK_NOISE measurement flips.
    """
    failed = fault_present
    if rng.random() < TRACK_NOISE:
        failed = not failed
    return not failed  # True = track passes


def isolated_attribution(agent_fault, world_fault, rng):
    agent_pass = _track_outcome(agent_fault, rng)
    world_pass = _track_outcome(world_fault, rng)
    return _attribution_from_tracks(agent_pass, world_pass)


def _attribution_from_tracks(agent_pass, world_pass):
    if not agent_pass and world_pass:
        return "agent"
    if agent_pass and not world_pass:
        return "world"
    if not agent_pass and not world_pass:
        return "both"
    return "neither"


def run_episode(fault, rng):
    agent_fault = fault in ("agent", "both")
    world_fault = fault in ("world", "both")
    ep = _place(agent_fault, world_fault, rng)
    ep["fault"] = fault
    ep["coupled_attr"] = coupled_attribution(ep)
    ep["coupled_attr_vacuous"] = coupled_attribution_vacuous(ep)
    agent_pass = _track_outcome(agent_fault, rng)
    world_pass = _track_outcome(world_fault, rng)
    ep["agent_pass"] = agent_pass
    ep["world_pass"] = world_pass
    ep["isolated_attr"] = _attribution_from_tracks(agent_pass, world_pass)
    return ep


def run(seed, n_per_fault):
    """Run n_per_fault episodes per fault category. Returns summary dict."""
    rng = random.Random(seed)
    episodes = []
    for fault in FAULTS:
        for _ in range(n_per_fault):
            episodes.append(run_episode(fault, rng))
    return summarise(episodes, seed)


def summarise(episodes, seed):
    def rate(rows, key):
        return sum(1 for r in rows if r[key]) / len(rows) if rows else 0.0

    single = [e for e in episodes if e["fault"] in ("agent", "world")]
    clean = [e for e in episodes if e["fault"] == "none"]
    out = {"seed": seed, "n": len(episodes)}
    out["coupled_success"] = rate(episodes, "success")
    out["agent_track_pass_rate"] = rate(episodes, "agent_pass")
    out["world_track_pass_rate"] = rate(episodes, "world_pass")
    out["coupled_success_by_fault"] = {
        f: rate([e for e in episodes if e["fault"] == f], "success") for f in FAULTS
    }
    # component-track pass rates on the full mix (like paper's non-zero
    # component scores beside a failing coupled run) -- recomputed from
    # isolated attributions is not possible, so track them via fresh draws:
    out["coupled_attr_accuracy_single"] = sum(
        1 for e in single if e["coupled_attr"] == e["fault"]
    ) / len(single)
    out["coupled_attr_accuracy_single_vacuous"] = sum(
        1 for e in single if e["coupled_attr_vacuous"] == e["fault"]
    ) / len(single)
    out["isolated_attr_accuracy_single"] = sum(
        1 for e in single if e["isolated_attr"] == e["fault"]
    ) / len(single)
    for fault in ("agent", "world"):
        rows = [e for e in single if e["fault"] == fault]
        out[f"coupled_attr_accuracy_{fault}"] = sum(
            1 for e in rows if e["coupled_attr"] == fault
        ) / len(rows)
        out[f"isolated_attr_accuracy_{fault}"] = sum(
            1 for e in rows if e["isolated_attr"] == fault
        ) / len(rows)
    out["benign_neither_rate"] = sum(
        1 for e in clean if e["isolated_attr"] == "neither"
    ) / len(clean)
    out["benign_coupled_success"] = rate(clean, "success")
    out["gap"] = (
        out["isolated_attr_accuracy_single"] - out["coupled_attr_accuracy_single"]
    )
    return out


def bootstrap_gap(seed, n_per_fault, resamples=2000, boot_seed=999):
    """Paired bootstrap CI for (isolated - coupled) attribution accuracy."""
    rng = random.Random(seed)
    episodes = []
    for fault in FAULTS:
        for _ in range(n_per_fault):
            episodes.append(run_episode(fault, rng))
    single = [e for e in episodes if e["fault"] in ("agent", "world")]
    brng = random.Random(boot_seed)
    diffs = []
    for _ in range(resamples):
        sample = [single[brng.randrange(len(single))] for _ in single]
        iso = sum(1 for e in sample if e["isolated_attr"] == e["fault"]) / len(sample)
        coup = sum(1 for e in sample if e["coupled_attr"] == e["fault"]) / len(sample)
        diffs.append(iso - coup)
    diffs.sort()
    lo = diffs[int(0.025 * resamples)]
    hi = diffs[int(0.975 * resamples)]
    base = summarise(episodes, seed)
    base["gap_ci95"] = [lo, hi]
    return base


if __name__ == "__main__":
    import sys

    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 118001
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    print(json.dumps(bootstrap_gap(seed, n), indent=2))
