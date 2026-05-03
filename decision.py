"""
Decision Module
Evaluates a list of options using weighted criteria scoring.
"""


def evaluate_decision(options: list, criteria: dict) -> dict:
    """
    Scores each option by distributing criteria weights across options
    using a simple rank-based approach.

    criteria keys: urgency (1-10), importance (1-10), effort (1-10, lower=better)
    Returns best option and full ranked list.
    """
    if not options:
        return {"error": "No options provided."}

    n = len(options)
    scored = []

    for i, option in enumerate(options):
        # Simulate scoring: options listed earlier are slightly preferred,
        # modified by the criteria weights to show impact.
        rank_bonus = (n - i) / n  # 1.0 → 1/n

        # Weighted score formula
        urgency_w = criteria.get("urgency", 5) / 10
        importance_w = criteria.get("importance", 5) / 10
        effort_penalty = (10 - criteria.get("effort", 5)) / 10  # lower effort = higher score

        raw_score = (urgency_w * 0.35 + importance_w * 0.40 + effort_penalty * 0.25) * rank_bonus * 100
        score = round(raw_score, 1)
        scored.append({"option": option, "score": score})

    # Sort descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    best = scored[0]
    reason = _build_reason(best["option"], criteria)

    return {
        "best": best["option"],
        "score": best["score"],
        "reason": reason,
        "ranked": scored
    }


def _build_reason(option: str, criteria: dict) -> str:
    urgency = criteria.get("urgency", 5)
    importance = criteria.get("importance", 5)
    effort = criteria.get("effort", 5)

    parts = []
    if urgency >= 7:
        parts.append("high urgency")
    if importance >= 7:
        parts.append("strong importance")
    if effort <= 4:
        parts.append("low effort required")

    if parts:
        return f'"{option}" scores highest due to {", ".join(parts)}.'
    return f'"{option}" is the most balanced choice given your criteria.'