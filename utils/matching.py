"""
Career and personality matching using cosine similarity.
"""

import numpy as np
from data.careers import CAREERS
from data.personalities import FAMOUS_PERSONALITIES


def cosine_similarity(v1: list, v2: list) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(v1, dtype=float)
    b = np.array(v2, dtype=float)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def match_careers(user_vector: list, top_n: int = 5) -> list:
    """
    Match user trait vector against career profiles.
    
    Returns list of dicts sorted by match_score descending.
    """
    results = []
    for name, career in CAREERS.items():
        sim = cosine_similarity(user_vector, career["traits"])
        # Scale to percentage with a floor/ceiling so it feels meaningful
        pct = round(min(99, max(60, sim * 100)), 1)
        # Generate match explanation based on top contributing traits
        explanation = _career_explanation(user_vector, career["traits"], name)
        results.append({
            "name": name,
            "score": pct,
            "raw_sim": sim,
            "emoji": career["emoji"],
            "tagline": career["tagline"],
            "description": career["description"],
            "work_style": career["work_style"],
            "environment": career["environment"],
            "strengths": career["strengths"],
            "explanation": explanation,
        })

    results.sort(key=lambda x: x["raw_sim"], reverse=True)

    # Rescale top 5 so top match is high (85–99 range)
    if results:
        top_raw = results[0]["raw_sim"]
        for r in results:
            scaled = (r["raw_sim"] / top_raw) * 97
            r["score"] = round(min(99, max(55, scaled)), 1)

    return results[:top_n]


def match_personalities(user_vector: list, top_n: int = 4) -> list:
    """
    Match user against famous personalities using cosine similarity.
    """
    results = []
    for name, person in FAMOUS_PERSONALITIES.items():
        sim = cosine_similarity(user_vector, person["traits"])
        pct = round(sim * 100, 1)
        results.append({
            "name": name,
            "score": pct,
            "raw_sim": sim,
            "emoji": person["emoji"],
            "field": person["field"],
            "descriptor": person["descriptor"],
            "bio": person["bio"],
            "quote": person["quote"],
            "known_for": person["known_for"],
        })

    results.sort(key=lambda x: x["raw_sim"], reverse=True)

    # Rescale
    if results:
        top_raw = results[0]["raw_sim"]
        for r in results:
            scaled = (r["raw_sim"] / top_raw) * 94
            r["score"] = round(min(97, max(50, scaled)), 1)

    return results[:top_n]


def _career_explanation(user: list, ideal: list, career_name: str) -> str:
    """Generate a human-readable explanation for a career match."""
    trait_names = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    trait_labels = {
        "Openness": ("intellectual curiosity", "practical focus"),
        "Conscientiousness": ("strong discipline", "flexible approach"),
        "Extraversion": ("social energy", "reflective depth"),
        "Agreeableness": ("collaborative warmth", "analytical independence"),
        "Neuroticism": ("emotional sensitivity", "emotional resilience"),
    }

    # Find top 2 contributing traits (where user aligns closest to ideal)
    diffs = [abs(user[i] - ideal[i]) for i in range(len(trait_names))]
    best_indices = sorted(range(len(diffs)), key=lambda i: diffs[i])[:2]

    reasons = []
    for idx in best_indices:
        trait = trait_names[idx]
        user_val = user[idx]
        label = trait_labels[trait][0] if user_val > 50 else trait_labels[trait][1]
        reasons.append(label)

    if len(reasons) >= 2:
        return f"Your {reasons[0]} and {reasons[1]} align closely with this role's core demands."
    elif len(reasons) == 1:
        return f"Your {reasons[0]} makes this a natural fit."
    return "Your personality profile aligns well with this career path."
