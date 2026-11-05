import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dual_exam import (  # noqa: E402
    FAULTS,
    coupled_attribution,
    isolated_attribution,
    run,
    run_episode,
    summarise,
)


def test_determinism():
    a = run(118001, 50)
    b = run(118001, 50)
    assert a == b


def test_fault_categories_present():
    rng = random.Random(7)
    seen = {run_episode(f, rng)["fault"] for f in FAULTS}
    assert seen == set(FAULTS)


def test_clean_episodes_succeed_coupled():
    # No faults, no noise in the coupled run: goal always met.
    rng = random.Random(3)
    for _ in range(50):
        ep = run_episode("none", rng)
        assert ep["success"] is True


def test_agent_fault_breaks_goal():
    # Systematic confusion puts items in the decoy, so the goal fails.
    rng = random.Random(11)
    fails = sum(1 for _ in range(50) if not run_episode("agent", rng)["success"])
    assert fails >= 45  # confusion 0.8/item; near-always fails


def test_coupled_attribution_rule():
    # Lower-score-wins: consistency below response -> world, else agent.
    assert coupled_attribution({"consistency": 0.5, "response": 1.0}) == "world"
    assert coupled_attribution({"consistency": 0.8, "response": 0.5}) == "agent"
    assert coupled_attribution({"consistency": 0.5, "response": 0.5}) == "agent"


def test_isolated_attribution_uses_tracks_only():
    # With zero track noise the rule maps track outcomes to components.
    import dual_exam

    old = dual_exam.TRACK_NOISE
    dual_exam.TRACK_NOISE = 0.0
    try:
        rng = random.Random(1)
        assert isolated_attribution(True, False, rng) == "agent"
        assert isolated_attribution(False, True, rng) == "world"
        assert isolated_attribution(True, True, rng) == "both"
        assert isolated_attribution(False, False, rng) == "neither"
    finally:
        dual_exam.TRACK_NOISE = old


def test_world_fault_visible_to_agent():
    # A dropped placement must surface as a visible discrepancy sometimes.
    rng = random.Random(5)
    seen = sum(1 for _ in range(50) if run_episode("world", rng)["discrepancies"] > 0)
    assert seen >= 40


def test_agent_fault_hides_discrepancy():
    # Confused agent expects the decoy, so most agent-fault runs show few
    # visible discrepancies relative to world-fault runs.
    rng = random.Random(9)
    a = sum(run_episode("agent", rng)["discrepancies"] for _ in range(50))
    w = sum(run_episode("world", rng)["discrepancies"] for _ in range(50))
    assert a < w


def test_summary_keys():
    s = run(118001, 20)
    for k in (
        "coupled_success",
        "coupled_attr_accuracy_single",
        "isolated_attr_accuracy_single",
        "gap",
        "benign_neither_rate",
    ):
        assert k in s
    assert 0.0 <= s["gap"] <= 1.0


def test_gap_is_not_hardcoded():
    # Different seeds give different (non-identical) gaps.
    assert run(118001, 50)["gap"] != run(118002, 50)["gap"]
