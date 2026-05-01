"""
AI-style narrative generator for personality summaries.
Uses template logic to produce psychologically intelligent, non-repetitive descriptions.
"""

import random


def generate_narrative(scores: dict, personality_type: dict) -> str:
    """
    Generate a multi-paragraph personality narrative from trait scores.
    Combines different templates based on score levels to avoid repetition.
    """
    O = scores.get("Openness", 50)
    C = scores.get("Conscientiousness", 50)
    E = scores.get("Extraversion", 50)
    A = scores.get("Agreeableness", 50)
    N = scores.get("Neuroticism", 50)

    paragraphs = []

    # ── Paragraph 1: Core intellectual nature ──────────────────────────────
    if O > 80:
        p1_options = [
            "Your mind operates at the intersection of curiosity and depth. You are drawn to ideas that challenge assumptions and resist easy answers—the kind of intellectual explorer who finds more joy in the question than the resolution.",
            "You possess an unusually rich inner world, one that hungers for novelty, pattern, and meaning. Abstract concepts energize you, and you often find conventional thinking too limiting to hold your attention for long.",
        ]
    elif O > 55:
        p1_options = [
            "You balance imaginative thinking with practical grounding. While you appreciate new ideas and creative approaches, you also know when to anchor your thinking in what works. This blend makes you both innovative and effective.",
            "Your intellectual curiosity is selective and purposeful—you explore new territory when it serves your goals, and you bring genuine creativity to the problems that matter most to you.",
        ]
    else:
        p1_options = [
            "You are a pragmatic thinker who values proven approaches over untested theories. Your strength lies in execution and mastery—you go deep rather than wide, building expertise others can rely on.",
            "You approach the world concretely and analytically. Where others chase abstractions, you prefer tangible results. Your focus and reliability make you someone people can genuinely count on.",
        ]
    paragraphs.append(random.choice(p1_options))

    # ── Paragraph 2: Drive and discipline ──────────────────────────────────
    if C > 80:
        p2_options = [
            "Discipline is not a struggle for you—it is a language you speak fluently. You set high standards for yourself and follow through with quiet determination. This reliability isn't just a trait; it's a form of integrity.",
            "You are the kind of person who finishes what they start. Your combination of ambition and follow-through is rare, and it consistently sets you apart in environments that reward sustained effort.",
        ]
    elif C > 55:
        p2_options = [
            "You strike a productive balance between structure and spontaneity. You can commit to a plan and see it through, but you're flexible enough to adapt when circumstances change—a balance that serves you well.",
            "Your approach to goals is measured and realistic. You know how to prioritize, pace yourself, and deliver—without the rigidity that sometimes hampers highly conscientious individuals.",
        ]
    else:
        p2_options = [
            "You operate better in fluid, open-ended environments than in rigid structures. You bring creativity and adaptability to whatever you do, though you may benefit from systems that channel your energy effectively.",
            "Your spontaneity and flexibility are genuine assets in dynamic environments. You think on your feet and adapt quickly—skills that matter enormously in fast-changing contexts.",
        ]
    paragraphs.append(random.choice(p2_options))

    # ── Paragraph 3: Social energy and connection ──────────────────────────
    if E > 75:
        p3_options = [
            "Socially, you are a natural energizer. You draw people in and make them feel seen, valued, and engaged. For you, other people are not a cost to manage but a genuine source of vitality.",
            "You are at your best in the company of others. Your social confidence is genuine—not a performance—and you have an intuitive ability to read and shape the emotional tenor of a room.",
        ]
    elif E > 45:
        p3_options = [
            "You are comfortably ambiverted: capable of deep social engagement when the context is right, but equally at home in focused solitude. You conserve your energy wisely and bring quality over quantity to your relationships.",
            "You move comfortably between social engagement and introspection. You can hold your own in any room, but you also know that some of your best thinking happens when you're alone with your ideas.",
        ]
    else:
        p3_options = [
            "Your introversion is not withdrawal—it's depth. You invest in fewer relationships, but those you maintain are rich with meaning. Your most powerful insights tend to emerge in quiet, reflective states.",
            "You prefer depth over breadth in your social life. While you may not seek the spotlight, the people who truly know you find your company remarkably substantive and rewarding.",
        ]
    paragraphs.append(random.choice(p3_options))

    # ── Paragraph 4: Emotional landscape ───────────────────────────────────
    if N > 65:
        p4_options = [
            "Emotionally, you feel things with uncommon intensity. This sensitivity is a double-edged gift: it makes you deeply empathetic and perceptive, but it can also leave you more exposed to the friction of daily life. Learning to channel rather than suppress this sensitivity is often a key theme in your development.",
            "Your emotional range is wide and real. You are not someone who glosses over difficulty—you sit with complexity, process it, and eventually integrate it. This depth, though sometimes costly, also drives much of your insight.",
        ]
    elif N > 40:
        p4_options = [
            "You are emotionally aware without being overwhelmed. You notice stress and difficulty, but you have developed the resilience to move through challenges without being derailed by them.",
            "Your emotional life is present but managed. You feel the full range of human experience and have enough self-awareness to work with your emotions rather than against them.",
        ]
    else:
        p4_options = [
            "You possess an unusual degree of emotional steadiness. Under pressure, you are the calm that others seek. Your equanimity is not coldness—it is the result of a genuinely secure inner foundation.",
            "Your emotional stability is one of your most reliable assets. In turbulent situations, you provide the kind of grounded presence that allows those around you to think clearly and act well.",
        ]
    paragraphs.append(random.choice(p4_options))

    # ── Paragraph 5: Closing synthesis ─────────────────────────────────────
    closing_options = [
        f"Taken together, your profile suggests someone who is {personality_type['tagline'].lower()} Your greatest leverage lies at the intersection of your strongest traits—use them intentionally, and they become a genuine competitive advantage.",
        f"Your personality type—{personality_type['name']}—captures something real about how you move through the world. The profiles that resonate most powerfully are the ones that make you want to live more fully into your strengths.",
        f"The pattern of your scores points toward a distinctive way of engaging with the world. Lean into what comes naturally to you, and work thoughtfully on the edges—not to change who you are, but to expand what you're capable of.",
    ]
    paragraphs.append(random.choice(closing_options))

    return "\n\n".join(paragraphs)


def generate_work_environment_analysis(scores: dict) -> list:
    """Generate work environment compatibility ratings."""
    O = scores.get("Openness", 50)
    C = scores.get("Conscientiousness", 50)
    E = scores.get("Extraversion", 50)
    A = scores.get("Agreeableness", 50)
    N = scores.get("Neuroticism", 50)

    environments = [
        {
            "name": "Remote / Async",
            "score": min(95, (100 - E) * 0.5 + C * 0.3 + O * 0.2),
            "emoji": "🏠",
        },
        {
            "name": "Open Office / Collaborative",
            "score": min(95, E * 0.5 + A * 0.3 + (100 - N) * 0.2),
            "emoji": "👥",
        },
        {
            "name": "High-Pressure / Fast-Paced",
            "score": min(95, C * 0.4 + (100 - N) * 0.4 + E * 0.2),
            "emoji": "⚡",
        },
        {
            "name": "Research / Deep Work",
            "score": min(95, O * 0.4 + C * 0.3 + (100 - E) * 0.3),
            "emoji": "🔬",
        },
        {
            "name": "Creative / Experimental",
            "score": min(95, O * 0.5 + (100 - C) * 0.2 + E * 0.3),
            "emoji": "🎨",
        },
        {
            "name": "Structured / Process-Driven",
            "score": min(95, C * 0.5 + (100 - O) * 0.2 + (100 - N) * 0.3),
            "emoji": "📋",
        },
    ]

    for env in environments:
        env["score"] = round(env["score"], 1)

    return sorted(environments, key=lambda x: x["score"], reverse=True)
