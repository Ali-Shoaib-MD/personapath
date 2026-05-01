"""
Scoring utilities for the Big Five personality assessment.
"""

import numpy as np
from data.questions import QUESTIONS


def calculate_trait_scores(answers: dict) -> dict:
    """
    Calculate normalized trait scores (0–100) from raw Likert answers.
    
    Args:
        answers: dict mapping question_id -> score (1–5)
    
    Returns:
        dict mapping trait_name -> normalized score (0–100)
    """
    trait_scores = {}

    for trait, questions in QUESTIONS.items():
        raw_scores = []
        for q in questions:
            qid = q["id"]
            if qid in answers:
                score = answers[qid]
                # Reverse-score if needed (1→5, 2→4, 3→3, 4→2, 5→1)
                if q["reverse"]:
                    score = 6 - score
                raw_scores.append(score)

        if raw_scores:
            # Average raw score (1–5), then normalize to 0–100
            avg = np.mean(raw_scores)
            normalized = ((avg - 1) / 4) * 100
            trait_scores[trait] = round(normalized, 1)
        else:
            trait_scores[trait] = 50.0  # Default midpoint if no answers

    return trait_scores


def get_trait_vector(scores: dict) -> list:
    """
    Convert trait scores dict to ordered list for similarity calculations.
    Order: [Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism]
    """
    trait_order = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    return [scores.get(t, 50.0) for t in trait_order]


def get_personality_type(scores: dict) -> dict:
    """
    Derive a personality type label from trait scores.
    Returns a name, archetype, and description.
    """
    O = scores.get("Openness", 50)
    C = scores.get("Conscientiousness", 50)
    E = scores.get("Extraversion", 50)
    A = scores.get("Agreeableness", 50)
    N = scores.get("Neuroticism", 50)

    # Determine primary and secondary type
    if O > 75 and C > 70:
        return {
            "name": "The Architect",
            "emoji": "🏛️",
            "tagline": "Visionary builder of systems and ideas.",
            "description": (
                "You combine intellectual curiosity with structured discipline—a rare "
                "combination that allows you to both dream big and execute with precision."
            ),
        }
    elif O > 75 and E > 65:
        return {
            "name": "The Innovator",
            "emoji": "💡",
            "tagline": "Creative force who inspires change.",
            "description": (
                "You're a natural idea generator who loves sharing and championing new concepts. "
                "You energize the people around you with your enthusiasm and originality."
            ),
        }
    elif O > 75 and A > 70:
        return {
            "name": "The Sage",
            "emoji": "🦉",
            "tagline": "Thoughtful guide with deep wisdom.",
            "description": (
                "You blend intellectual depth with genuine warmth, making you a trusted advisor "
                "and thoughtful collaborator who sees the human side of every challenge."
            ),
        }
    elif C > 80 and N < 40:
        return {
            "name": "The Strategist",
            "emoji": "♟️",
            "tagline": "Calm, calculated, and always prepared.",
            "description": (
                "You excel at long-term planning and execution. Your emotional stability "
                "combined with high discipline makes you formidable under pressure."
            ),
        }
    elif E > 75 and A > 70:
        return {
            "name": "The Connector",
            "emoji": "🌐",
            "tagline": "Natural relationship-builder and leader.",
            "description": (
                "You thrive in social environments and have a genuine gift for bringing people "
                "together. Others are naturally drawn to your warmth and positive energy."
            ),
        }
    elif E < 40 and O > 70:
        return {
            "name": "The Visionary Introvert",
            "emoji": "🔭",
            "tagline": "Deep thinker with transformative ideas.",
            "description": (
                "Your quiet exterior masks a rich inner world full of original ideas. "
                "You do your best work in focused solitude, producing insights others miss."
            ),
        }
    elif A > 80 and C > 70:
        return {
            "name": "The Mentor",
            "emoji": "🌱",
            "tagline": "Dedicated guide who helps others grow.",
            "description": (
                "You combine genuine care for others with reliable follow-through. "
                "People trust you to show up and help them become their best selves."
            ),
        }
    elif N > 70 and O > 70:
        return {
            "name": "The Artist",
            "emoji": "🎭",
            "tagline": "Emotionally rich and creatively driven.",
            "description": (
                "Your emotional sensitivity fuels extraordinary creativity. "
                "You perceive nuance others miss and translate feeling into meaningful expression."
            ),
        }
    elif C > 80 and A > 75:
        return {
            "name": "The Steward",
            "emoji": "🛡️",
            "tagline": "Reliable guardian of people and purpose.",
            "description": (
                "You are the backbone of any team—dependable, principled, and genuinely invested "
                "in collective success. Others look to you when things get hard."
            ),
        }
    else:
        return {
            "name": "The Balanced Explorer",
            "emoji": "⚖️",
            "tagline": "Adaptable and multidimensional.",
            "description": (
                "You don't fit neatly into a single box—and that's your strength. "
                "Your balanced profile makes you versatile, adaptable, and effective across contexts."
            ),
        }


def get_burnout_risk(scores: dict) -> dict:
    """Estimate burnout vulnerability from trait scores."""
    N = scores.get("Neuroticism", 50)
    C = scores.get("Conscientiousness", 50)
    A = scores.get("Agreeableness", 50)
    E = scores.get("Extraversion", 50)

    # High Neuroticism + High Conscientiousness + High Agreeableness = higher risk
    risk_score = (N * 0.5) + (C * 0.25) + (A * 0.15) - (E * 0.1)
    risk_score = max(0, min(100, risk_score))

    if risk_score < 35:
        level, color, advice = "Low", "#00C9A7", "You show strong resilience patterns. Maintain your healthy boundaries."
    elif risk_score < 60:
        level, color, advice = "Moderate", "#FFB347", "Some vulnerability present. Regular recovery time is important for you."
    else:
        level, color, advice = "Elevated", "#FF6B6B", "Your profile suggests sensitivity to overwork. Prioritize self-care boundaries."

    return {"score": round(risk_score, 1), "level": level, "color": color, "advice": advice}


def get_leadership_style(scores: dict) -> dict:
    """Predict leadership style from trait profile."""
    O = scores.get("Openness", 50)
    C = scores.get("Conscientiousness", 50)
    E = scores.get("Extraversion", 50)
    A = scores.get("Agreeableness", 50)

    if E > 70 and A > 65:
        return {"style": "Transformational", "emoji": "🌟", "desc": "You inspire through vision, energy, and authentic connection."}
    elif C > 80 and E > 60:
        return {"style": "Commanding", "emoji": "⚔️", "desc": "You lead through clarity, decisiveness, and high standards."}
    elif A > 75 and C > 65:
        return {"style": "Servant Leader", "emoji": "🌱", "desc": "You lead by empowering others and building deep trust."}
    elif O > 80 and E > 55:
        return {"style": "Visionary", "emoji": "🔭", "desc": "You lead through big-picture thinking and inspiring possibilities."}
    elif C > 75 and A < 55:
        return {"style": "Pacesetter", "emoji": "⚡", "desc": "You lead by example, holding yourself and others to high standards."}
    else:
        return {"style": "Democratic", "emoji": "🤝", "desc": "You lead through consensus-building and collaborative decision-making."}
