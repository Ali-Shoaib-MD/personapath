"""
Big Five Personality Assessment Questions
Each trait has 6 questions with reverse-scored items marked.
"""

QUESTIONS = {
    "Openness": [
        {"id": "O1", "text": "I enjoy exploring unconventional or abstract ideas.", "reverse": False},
        {"id": "O2", "text": "I am curious about many different things.", "reverse": False},
        {"id": "O3", "text": "I find artistic and creative expression meaningful.", "reverse": False},
        {"id": "O4", "text": "I prefer sticking to familiar routines over new experiences.", "reverse": True},
        {"id": "O5", "text": "I enjoy thinking about philosophical or theoretical problems.", "reverse": False},
        {"id": "O6", "text": "I find it difficult to imagine things from different perspectives.", "reverse": True},
    ],
    "Conscientiousness": [
        {"id": "C1", "text": "I complete tasks thoroughly and pay close attention to details.", "reverse": False},
        {"id": "C2", "text": "I follow a clear plan when working toward my goals.", "reverse": False},
        {"id": "C3", "text": "I often leave things unfinished or disorganized.", "reverse": True},
        {"id": "C4", "text": "I hold myself to high standards in my work.", "reverse": False},
        {"id": "C5", "text": "I procrastinate on important tasks more than I should.", "reverse": True},
        {"id": "C6", "text": "I am dependable and others can count on me.", "reverse": False},
    ],
    "Extraversion": [
        {"id": "E1", "text": "I feel energized when spending time with groups of people.", "reverse": False},
        {"id": "E2", "text": "I tend to take charge in social situations.", "reverse": False},
        {"id": "E3", "text": "I find social events draining rather than energizing.", "reverse": True},
        {"id": "E4", "text": "I enjoy being the center of attention.", "reverse": False},
        {"id": "E5", "text": "I prefer working alone over collaborating in teams.", "reverse": True},
        {"id": "E6", "text": "I find it easy to start conversations with new people.", "reverse": False},
    ],
    "Agreeableness": [
        {"id": "A1", "text": "I genuinely care about the well-being of others.", "reverse": False},
        {"id": "A2", "text": "I am willing to compromise to avoid conflict.", "reverse": False},
        {"id": "A3", "text": "I can be critical or skeptical of other people's motives.", "reverse": True},
        {"id": "A4", "text": "I enjoy cooperating with others to achieve shared goals.", "reverse": False},
        {"id": "A5", "text": "I sometimes prioritize my own needs over others' feelings.", "reverse": True},
        {"id": "A6", "text": "I believe most people have good intentions.", "reverse": False},
    ],
    "Neuroticism": [
        {"id": "N1", "text": "I often feel anxious or worried about things.", "reverse": False},
        {"id": "N2", "text": "My mood changes frequently throughout the day.", "reverse": False},
        {"id": "N3", "text": "I remain calm and composed under pressure.", "reverse": True},
        {"id": "N4", "text": "I sometimes feel overwhelmed by everyday stressors.", "reverse": False},
        {"id": "N5", "text": "I recover quickly from setbacks or disappointments.", "reverse": True},
        {"id": "N6", "text": "I tend to dwell on negative experiences longer than necessary.", "reverse": False},
    ],
}

TRAIT_DESCRIPTIONS = {
    "Openness": {
        "high": "Intellectually curious, imaginative, and drawn to novel experiences.",
        "low": "Practical, conventional, and focused on concrete realities.",
        "icon": "🔭",
        "color": "#6C63FF",
    },
    "Conscientiousness": {
        "high": "Organized, disciplined, and highly goal-oriented.",
        "low": "Flexible, spontaneous, and adaptive to changing circumstances.",
        "icon": "📐",
        "color": "#00C9A7",
    },
    "Extraversion": {
        "high": "Energized by social interaction, assertive and expressive.",
        "low": "Reflective, self-sufficient, and comfortable in solitude.",
        "icon": "⚡",
        "color": "#FFB347",
    },
    "Agreeableness": {
        "high": "Cooperative, empathetic, and trusting of others.",
        "low": "Independent, analytical, and direct in communication.",
        "icon": "🤝",
        "color": "#FF6B9D",
    },
    "Neuroticism": {
        "high": "Emotionally sensitive, with heightened awareness of stress.",
        "low": "Emotionally stable, resilient, and even-tempered.",
        "icon": "🌊",
        "color": "#4ECDC4",
    },
}
