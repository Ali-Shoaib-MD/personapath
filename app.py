"""
PersonaPath — Psychology-Based Personality & Career Matching Platform
A polished MVP built with Streamlit + Plotly.
"""

import streamlit as st
import sys
import os

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="PersonaPath",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ──────────────────────────────────────────────────────────────────
from data.questions import QUESTIONS, TRAIT_DESCRIPTIONS
from utils.scoring import (
    calculate_trait_scores,
    get_trait_vector,
    get_personality_type,
    get_burnout_risk,
    get_leadership_style,
)
from utils.matching import match_careers, match_personalities
from utils.visualization import radar_chart, trait_bars, career_match_bar, comparison_radar
from utils.narrative import generate_narrative, generate_work_environment_analysis
from utils.report import generate_markdown_report

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0D0D1A 0%, #0F1629 50%, #0D1A24 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122A 0%, #0F1629 100%);
    border-right: 1px solid rgba(108,99,255,0.2);
}

/* ── Cards ── */
.persona-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.2s ease;
}

.persona-card:hover {
    border-color: rgba(108,99,255,0.5);
    background: rgba(108,99,255,0.06);
}

.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
}

.trait-chip {
    display: inline-block;
    background: rgba(108,99,255,0.2);
    border: 1px solid rgba(108,99,255,0.4);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #A8A4FF;
    margin: 3px;
}

/* ── Hero ── */
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6C63FF, #00C9A7, #FFB347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #9090B0;
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.6rem;
    font-weight: 600;
    color: #E8E8F0;
    margin-bottom: 4px;
}

.section-sub {
    color: #7070A0;
    font-size: 0.95rem;
    margin-bottom: 24px;
}

/* ── Progress bar override ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6C63FF, #00C9A7);
    border-radius: 10px;
}

/* ── Radio buttons — group label AND every option label ── */
.stRadio > label,
.stRadio label,
.stRadio div[role="radiogroup"] label,
.stRadio div[data-testid="stMarkdownContainer"] p,
[data-testid="stRadio"] label,
[data-testid="stRadio"] span {
    color: #D8D8F0 !important;
}

/* ── All generic Streamlit text/markdown ── */
.stMarkdown p,
.stMarkdown li,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown table,
.stMarkdown td,
.stMarkdown th,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] blockquote,
[data-testid="stMarkdownContainer"] code,
[data-testid="stMarkdownContainer"] pre {
    color: #D8D8F0 !important;
}

/* ── Expander header and content ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
.streamlit-expanderHeader,
.streamlit-expanderHeader p {
    color: #D8D8F0 !important;
}

[data-testid="stExpander"] > div > div p,
[data-testid="stExpander"] > div > div li,
[data-testid="stExpander"] > div > div h1,
[data-testid="stExpander"] > div > div h2,
[data-testid="stExpander"] > div > div h3,
[data-testid="stExpander"] > div > div table,
[data-testid="stExpander"] > div > div td,
[data-testid="stExpander"] > div > div th,
[data-testid="stExpander"] > div > div blockquote,
[data-testid="stExpander"] > div > div code {
    color: #D8D8F0 !important;
}

/* ── Table borders inside markdown ── */
[data-testid="stMarkdownContainer"] table {
    border-collapse: collapse;
    width: 100%;
}
[data-testid="stMarkdownContainer"] th {
    background: rgba(108,99,255,0.2) !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    padding: 8px 12px !important;
    color: #E8E8F0 !important;
}
[data-testid="stMarkdownContainer"] td {
    border: 1px solid rgba(255,255,255,0.1) !important;
    padding: 7px 12px !important;
}
[data-testid="stMarkdownContainer"] tr:nth-child(even) td {
    background: rgba(255,255,255,0.03) !important;
}

/* ── Blockquotes ── */
[data-testid="stMarkdownContainer"] blockquote {
    border-left: 3px solid #6C63FF !important;
    padding-left: 16px !important;
    color: #B0B0D0 !important;
    font-style: italic;
}

/* ── Inline code ── */
[data-testid="stMarkdownContainer"] code {
    background: rgba(108,99,255,0.15) !important;
    border-radius: 4px;
    padding: 1px 6px;
    color: #A8A4FF !important;
}

/* ── Success / info / warning boxes ── */
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #1a1a2e !important;
}

/* ── Download button text ── */
[data-testid="stDownloadButton"] button {
    color: white !important;
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p {
    color: #D8D8F0 !important;
}

/* ── Match score badge ── */
.score-badge {
    font-size: 2rem;
    font-weight: 700;
    color: #6C63FF;
}

/* ── Quote style ── */
.quote-block {
    border-left: 3px solid #6C63FF;
    padding: 12px 20px;
    background: rgba(108,99,255,0.08);
    border-radius: 0 12px 12px 0;
    font-style: italic;
    color: #C0C0E0;
    margin: 12px 0;
}

/* ── Tag chips ── */
.tag-row {
    margin: 8px 0;
}

/* ── Divider ── */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.5), transparent);
    margin: 32px 0;
}

/* ── Type name display ── */
.type-name {
    font-size: 2.4rem;
    font-weight: 700;
    color: #E8E8F0;
}

.type-tagline {
    font-size: 1.1rem;
    color: #9090B0;
    font-style: italic;
}

button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF, #4ECDC4) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ──────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "home",
        "answers": {},
        "current_question_flat_idx": 0,
        "scores": None,
        "assessment_complete": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()


# ── Sidebar Navigation ────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 20px 0 10px;'>
            <div style='font-size:2.5rem;'>🧠</div>
            <div style='font-size:1.3rem; font-weight:700; color:#E8E8F0;'>PersonaPath</div>
            <div style='font-size:0.75rem; color:#6060A0; letter-spacing:1px;'>PERSONALITY SCIENCE</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(108,99,255,0.2);'>", unsafe_allow_html=True)

        pages = {
            "home": ("🏠", "Home"),
            "assessment": ("📝", "Assessment"),
            "results": ("📊", "Your Results"),
            "careers": ("💼", "Career Matches"),
            "famous": ("🌟", "Famous Matches"),
            "report": ("📄", "Download Report"),
        }

        for key, (icon, label) in pages.items():
            is_active = st.session_state.page == key
            disabled = key in ("results", "careers", "famous", "report") and not st.session_state.assessment_complete

            style = "background:rgba(108,99,255,0.25);border:1px solid rgba(108,99,255,0.5);" if is_active else ""
            opacity = "opacity:0.35;" if disabled else ""

            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                disabled=disabled,
            ):
                st.session_state.page = key
                st.rerun()

        if st.session_state.assessment_complete and st.session_state.scores:
            st.markdown("<hr style='border-color:rgba(108,99,255,0.2);'>", unsafe_allow_html=True)
            scores = st.session_state.scores
            st.markdown("<div style='font-size:0.75rem; color:#6060A0; letter-spacing:1px; text-align:center; margin-bottom:12px;'>YOUR TRAITS</div>", unsafe_allow_html=True)
            for trait, score in scores.items():
                color = TRAIT_DESCRIPTIONS[trait]["color"]
                icon = TRAIT_DESCRIPTIONS[trait]["icon"]
                bar_width = int(score)
                st.markdown(f"""
                <div style='margin-bottom:10px;'>
                    <div style='display:flex; justify-content:space-between; font-size:11px; color:#9090B0; margin-bottom:3px;'>
                        <span>{icon} {trait[:4]}</span><span>{score:.0f}</span>
                    </div>
                    <div style='height:4px; background:rgba(255,255,255,0.08); border-radius:4px;'>
                        <div style='height:4px; width:{bar_width}%; background:{color}; border-radius:4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ── Page: Home ─────────────────────────────────────────────────────────────────
def page_home():
    col1, col2 = st.columns([1.3, 1], gap="large")
    with col1:
        st.markdown("""
        <div style='padding: 40px 0 20px;'>
            <div class='hero-title'>Discover the psychology<br>behind your ideal career.</div>
            <div class='hero-subtitle' style='margin-top: 16px; font-size: 1.1rem; max-width: 520px; line-height: 1.7;'>
                PersonaPath uses the scientifically validated Big Five model to map your unique 
                personality profile and match you to careers, environments, and historical figures 
                who share your cognitive DNA.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(3)
        features = [
            ("🧬", "Science-Based", "Built on the Big Five (OCEAN) model"),
            ("💼", "Career Matching", "Cosine-similarity career fit engine"),
            ("🌟", "Famous Matches", "See who shares your personality"),
        ]
        for col, (icon, title, desc) in zip(cols, features):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:1.8rem;'>{icon}</div>
                    <div style='font-weight:600; color:#E8E8F0; margin:6px 0 4px;'>{title}</div>
                    <div style='font-size:0.8rem; color:#7070A0;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨  Begin Assessment  →", type="primary", use_container_width=False):
            st.session_state.page = "assessment"
            st.session_state.answers = {}
            st.session_state.current_question_flat_idx = 0
            st.rerun()

    with col2:
        # Demo radar chart
        demo_scores = {"Openness": 82, "Conscientiousness": 71, "Extraversion": 55, "Agreeableness": 68, "Neuroticism": 38}
        fig = radar_chart(demo_scores)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style='text-align:center; font-size:0.8rem; color:#5050A0;'>
            Sample personality profile — yours awaits.
        </div>
        """, unsafe_allow_html=True)


# ── Page: Assessment ───────────────────────────────────────────────────────────
def page_assessment():
    # Flatten questions into a list
    all_questions = []
    for trait, qs in QUESTIONS.items():
        for q in qs:
            all_questions.append((trait, q))

    total = len(all_questions)
    idx = st.session_state.current_question_flat_idx

    if idx >= total:
        # Assessment complete
        _finish_assessment()
        return

    # Header
    st.markdown("""
    <div style='padding-top:20px;'>
        <div class='section-header'>📝 Personality Assessment</div>
        <div class='section-sub'>Answer honestly — there are no right or wrong answers.</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress
    progress = idx / total
    st.progress(progress)
    st.markdown(f"<div style='color:#7070A0; font-size:0.85rem; text-align:right; margin-top:4px;'>Question {idx + 1} of {total}</div>", unsafe_allow_html=True)

    trait, question = all_questions[idx]
    qid = question["id"]

    # Trait indicator
    color = TRAIT_DESCRIPTIONS[trait]["color"]
    icon = TRAIT_DESCRIPTIONS[trait]["icon"]
    st.markdown(f"""
    <div style='margin:24px 0 12px;'>
        <span style='background:rgba(108,99,255,0.15); border:1px solid {color}40; border-radius:20px; 
               padding:4px 14px; font-size:0.8rem; color:{color};'>
            {icon} {trait}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Question card
    st.markdown(f"""
    <div class='persona-card' style='margin:8px 0 24px; padding:32px;'>
        <div style='font-size:1.25rem; color:#E8E8F0; font-weight:500; line-height:1.6;'>
            {question['text']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scale labels
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div style='color:#6060A0; font-size:0.8rem;'>← Strongly Disagree</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown("<div style='color:#6060A0; font-size:0.8rem; text-align:right;'>Strongly Agree →</div>", unsafe_allow_html=True)

    # Radio scale
    current_val = st.session_state.answers.get(qid, 3)
    options = ["1 — Strongly Disagree", "2 — Disagree", "3 — Neutral", "4 — Agree", "5 — Strongly Agree"]
    default_idx = current_val - 1

    selected = st.radio(
        "Your response:",
        options,
        index=default_idx,
        horizontal=True,
        label_visibility="collapsed",
    )
    selected_val = int(selected[0])
    st.session_state.answers[qid] = selected_val

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation buttons
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        if idx > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_question_flat_idx -= 1
                st.rerun()
    with c3:
        label = "Finish ✓" if idx == total - 1 else "Next →"
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.current_question_flat_idx += 1
            st.rerun()


def _finish_assessment():
    """Process answers and compute all results."""
    with st.spinner("Analyzing your personality profile..."):
        scores = calculate_trait_scores(st.session_state.answers)
        st.session_state.scores = scores
        st.session_state.assessment_complete = True

    st.success("✅ Assessment complete! Your profile is ready.")
    st.balloons()
    if st.button("View My Results →", type="primary"):
        st.session_state.page = "results"
        st.rerun()


# ── Page: Results ──────────────────────────────────────────────────────────────
def page_results():
    scores = st.session_state.scores
    if not scores:
        st.warning("Complete the assessment first.")
        return

    personality_type = get_personality_type(scores)
    burnout = get_burnout_risk(scores)
    leadership = get_leadership_style(scores)
    narrative = generate_narrative(scores, personality_type)
    environments = generate_work_environment_analysis(scores)

    st.markdown("""
    <div style='padding-top:20px;'>
        <div class='section-header'>📊 Your Personality Profile</div>
        <div class='section-sub'>Based on your Big Five assessment responses.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Type card ──
    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        st.markdown(f"""
        <div class='persona-card' style='text-align:center; padding:40px 24px;'>
            <div style='font-size:4rem; margin-bottom:12px;'>{personality_type['emoji']}</div>
            <div class='type-name'>{personality_type['name']}</div>
            <div class='type-tagline'>{personality_type['tagline']}</div>
            <div style='margin-top:20px; color:#B0B0D0; font-size:0.9rem; line-height:1.7;'>
                {personality_type['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Bonus metrics
        st.markdown(f"""
        <div class='persona-card' style='padding:20px;'>
            <div style='font-weight:600; color:#E8E8F0; margin-bottom:16px;'>🔋 Burnout Vulnerability</div>
            <div style='display:flex; align-items:center; gap:12px;'>
                <div style='font-size:1.5rem; font-weight:700; color:{burnout["color"]};'>{burnout["level"]}</div>
                <div style='font-size:0.85rem; color:#9090B0;'>{burnout["score"]:.0f}/100</div>
            </div>
            <div style='height:4px; background:rgba(255,255,255,0.08); border-radius:4px; margin:8px 0;'>
                <div style='height:4px; width:{burnout["score"]}%; background:{burnout["color"]}; border-radius:4px;'></div>
            </div>
            <div style='font-size:0.8rem; color:#7070A0; margin-top:8px;'>{burnout["advice"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='persona-card' style='padding:20px;'>
            <div style='font-weight:600; color:#E8E8F0; margin-bottom:12px;'>👑 Leadership Style</div>
            <div style='font-size:1.5rem; font-weight:700; color:#6C63FF;'>{leadership["emoji"]} {leadership["style"]}</div>
            <div style='font-size:0.85rem; color:#9090B0; margin-top:8px;'>{leadership["desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.plotly_chart(radar_chart(scores), use_container_width=True, config={"displayModeBar": False})
        st.plotly_chart(trait_bars(scores), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Trait breakdown ──
    st.markdown("<div class='section-header' style='font-size:1.3rem;'>Trait Breakdown</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (trait, score) in enumerate(scores.items()):
        desc = TRAIT_DESCRIPTIONS[trait]
        level_text = desc["high"] if score >= 55 else desc["low"]
        with cols[i]:
            st.markdown(f"""
            <div class='persona-card' style='text-align:center; padding:20px 12px;'>
                <div style='font-size:1.8rem;'>{desc["icon"]}</div>
                <div style='font-weight:600; color:#E8E8F0; font-size:0.9rem; margin:6px 0 4px;'>{trait}</div>
                <div style='font-size:1.6rem; font-weight:700; color:{desc["color"]};'>{score:.0f}</div>
                <div style='font-size:0.72rem; color:#7070A0; margin-top:8px; line-height:1.5;'>{level_text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Narrative ──
    st.markdown("""
    <div class='section-header' style='font-size:1.3rem;'>📖 Your Personality Narrative</div>
    <div class='section-sub'>A psychologically grounded portrait of how you engage with the world.</div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='persona-card' style='padding:32px;'>
        <div style='color:#C8C8E0; font-size:0.95rem; line-height:1.85;'>
            {"</div><div style='margin-top:16px; color:#C8C8E0; font-size:0.95rem; line-height:1.85;'>".join(narrative.split(chr(10)+chr(10)))}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Work environments ──
    st.markdown("""
    <div class='section-header' style='font-size:1.3rem;'>🏢 Work Environment Compatibility</div>
    <div class='section-sub'>How well different settings match your trait profile.</div>
    """, unsafe_allow_html=True)
    env_cols = st.columns(3)
    for i, env in enumerate(environments):
        with env_cols[i % 3]:
            color = "#00C9A7" if env["score"] >= 75 else ("#FFB347" if env["score"] >= 55 else "#FF6B6B")
            st.markdown(f"""
            <div class='persona-card' style='padding:18px 20px;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                    <span style='font-size:0.9rem; color:#E8E8F0;'>{env["emoji"]} {env["name"]}</span>
                    <span style='font-weight:700; color:{color};'>{env["score"]:.0f}%</span>
                </div>
                <div style='height:5px; background:rgba(255,255,255,0.07); border-radius:5px;'>
                    <div style='height:5px; width:{env["score"]}%; background:{color}; border-radius:5px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Page: Careers ──────────────────────────────────────────────────────────────
def page_careers():
    scores = st.session_state.scores
    if not scores:
        st.warning("Complete the assessment first.")
        return

    user_vector = get_trait_vector(scores)
    career_matches = match_careers(user_vector, top_n=5)

    st.markdown("""
    <div style='padding-top:20px;'>
        <div class='section-header'>💼 Career Compatibility Matches</div>
        <div class='section-sub'>Ranked by psychological alignment using cosine similarity on the Big Five.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.plotly_chart(career_match_bar(career_matches), use_container_width=True, config={"displayModeBar": False})

    with col2:
        top = career_matches[0]
        st.markdown(f"""
        <div class='persona-card' style='padding:24px;'>
            <div style='font-size:0.75rem; color:#6C63FF; letter-spacing:1px; margin-bottom:8px;'>TOP MATCH</div>
            <div style='font-size:1.5rem; font-weight:700; color:#E8E8F0;'>{top["emoji"]} {top["name"]}</div>
            <div style='color:#9090B0; font-style:italic; margin:6px 0 12px;'>{top["tagline"]}</div>
            <div style='font-size:3rem; font-weight:800; color:#6C63FF; margin:16px 0;'>{top["score"]:.1f}%</div>
            <div style='color:#B0B0D0; font-size:0.9rem; line-height:1.7;'>{top["description"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Career cards ──
    for rank, match in enumerate(career_matches, 1):
        from data.careers import CAREERS
        ideal_traits = CAREERS[match["name"]]["traits"]

        with st.expander(f"#{rank}  {match['emoji']}  {match['name']} — {match['score']:.1f}% Match", expanded=(rank == 1)):
            c1, c2 = st.columns([1, 1.2])
            with c1:
                st.markdown(f"""
                <div class='persona-card' style='padding:20px;'>
                    <div style='font-weight:600; color:#E8E8F0; margin-bottom:10px;'>About this role</div>
                    <div style='color:#B0B0D0; font-size:0.9rem; line-height:1.7; margin-bottom:14px;'>{match['description']}</div>
                    <div style='font-size:0.82rem;'>
                        <div style='color:#7070A0; margin-bottom:4px;'>📌 Work Style</div>
                        <div style='color:#C0C0E0; margin-bottom:12px;'>{match['work_style']}</div>
                        <div style='color:#7070A0; margin-bottom:4px;'>🏢 Environment</div>
                        <div style='color:#C0C0E0; margin-bottom:12px;'>{match['environment']}</div>
                        <div style='color:#7070A0; margin-bottom:4px;'>✅ Why You Match</div>
                        <div style='color:#C0C0E0;'>{match['explanation']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.8rem; color:#7070A0; margin:8px 0 4px;'>Core Strengths</div>", unsafe_allow_html=True)
                tags = " ".join([f"<span class='trait-chip'>{s}</span>" for s in match["strengths"]])
                st.markdown(f"<div class='tag-row'>{tags}</div>", unsafe_allow_html=True)

            with c2:
                fig = comparison_radar(scores, ideal_traits, match["name"])
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Page: Famous Matches ───────────────────────────────────────────────────────
def page_famous():
    scores = st.session_state.scores
    if not scores:
        st.warning("Complete the assessment first.")
        return

    user_vector = get_trait_vector(scores)
    matches = match_personalities(user_vector, top_n=4)

    st.markdown("""
    <div style='padding-top:20px;'>
        <div class='section-header'>🌟 Famous Personality Matches</div>
        <div class='section-sub'>Historical figures and icons who share your psychological fingerprint.</div>
    </div>
    """, unsafe_allow_html=True)

    top = matches[0]
    st.markdown(f"""
    <div class='persona-card' style='padding:32px; margin-bottom:28px;'>
        <div style='font-size:0.75rem; color:#FFB347; letter-spacing:1.5px; margin-bottom:12px;'>⭐ YOUR CLOSEST MATCH</div>
        <div style='display:flex; align-items:center; gap:20px; flex-wrap:wrap;'>
            <div style='font-size:4rem;'>{top["emoji"]}</div>
            <div>
                <div style='font-size:2rem; font-weight:700; color:#E8E8F0;'>{top["name"]}</div>
                <div style='color:#9090B0; font-size:0.95rem;'>{top["descriptor"]} · {top["field"]}</div>
                <div style='font-size:2.4rem; font-weight:800; color:#FFB347; margin-top:4px;'>{top["score"]:.1f}% similarity</div>
            </div>
        </div>
        <div class='quote-block' style='margin-top:20px;'>"{top["quote"]}"</div>
        <div style='color:#B0B0D0; font-size:0.9rem; margin-top:16px;'>{top["bio"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Other matches
    cols = st.columns(3)
    for i, match in enumerate(matches[1:]):
        with cols[i]:
            tags = " ".join([f"<span class='trait-chip'>{k}</span>" for k in match["known_for"]])
            st.markdown(f"""
            <div class='persona-card' style='padding:22px;'>
                <div style='font-size:2.2rem; margin-bottom:10px;'>{match["emoji"]}</div>
                <div style='font-weight:700; color:#E8E8F0; font-size:1.05rem;'>{match["name"]}</div>
                <div style='color:#7070A0; font-size:0.8rem; margin-bottom:10px;'>{match["descriptor"]}</div>
                <div style='font-size:1.8rem; font-weight:700; color:#6C63FF;'>{match["score"]:.1f}%</div>
                <div style='font-size:0.8rem; color:#9090B0; margin:10px 0;'>{match["bio"][:100]}…</div>
                <div class='quote-block' style='font-size:0.78rem;'>"{match["quote"][:80]}…"</div>
                <div style='margin-top:10px;'>{tags}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # Side-by-side trait comparison with top match
    st.markdown(f"""
    <div class='section-header' style='font-size:1.3rem;'>Trait Comparison: You vs {top["name"]}</div>
    """, unsafe_allow_html=True)

    from data.personalities import FAMOUS_PERSONALITIES
    top_traits = FAMOUS_PERSONALITIES[top["name"]]["traits"]
    fig = comparison_radar(scores, top_traits, top["name"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Page: Report ───────────────────────────────────────────────────────────────
def page_report():
    scores = st.session_state.scores
    if not scores:
        st.warning("Complete the assessment first.")
        return

    user_vector = get_trait_vector(scores)
    personality_type = get_personality_type(scores)
    career_matches = match_careers(user_vector, top_n=5)
    personality_matches = match_personalities(user_vector, top_n=4)
    narrative = generate_narrative(scores, personality_type)
    burnout = get_burnout_risk(scores)
    leadership = get_leadership_style(scores)

    report_md = generate_markdown_report(
        scores, personality_type, career_matches, personality_matches,
        narrative, burnout, leadership,
    )

    st.markdown("""
    <div style='padding-top:20px;'>
        <div class='section-header'>📄 Download Your Report</div>
        <div class='section-sub'>A complete summary of your personality profile and career analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        st.markdown(f"""
        <div class='persona-card' style='padding:32px;'>
            <div style='font-weight:700; color:#E8E8F0; font-size:1.1rem; margin-bottom:16px;'>📋 Report Includes</div>
            <div style='font-size:0.9rem; color:#C0C0E0; line-height:2;'>
                ✅ &nbsp;Personality type: <strong>{personality_type['name']}</strong><br>
                ✅ &nbsp;Full Big Five trait scores<br>
                ✅ &nbsp;Top 5 career matches with explanations<br>
                ✅ &nbsp;Famous personality comparisons<br>
                ✅ &nbsp;AI-style narrative summary<br>
                ✅ &nbsp;Burnout vulnerability & leadership style<br>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="⬇️  Download Markdown Report",
            data=report_md,
            file_name="personapath_report.md",
            mime="text/markdown",
            type="primary",
            use_container_width=True,
        )

    with col2:
        st.markdown("""
        <div class='persona-card' style='padding:24px;'>
            <div style='font-weight:600; color:#E8E8F0; margin-bottom:12px;'>🔁 Retake Assessment</div>
            <div style='color:#9090B0; font-size:0.85rem; margin-bottom:16px;'>
                Personality can shift over time or with different life contexts.
                Feel free to retake to see how your profile evolves.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Start Over", use_container_width=True):
            for key in ["answers", "scores", "assessment_complete", "current_question_flat_idx"]:
                st.session_state[key] = {} if key == "answers" else (False if key == "assessment_complete" else (None if key == "scores" else 0))
            st.session_state.page = "home"
            st.rerun()

    with st.expander("📋 Preview Report"):
        st.markdown("""
        <div style='background:rgba(232,232,240,0.07); border:1px solid rgba(108,99,255,0.2);
                    border-radius:12px; padding:28px 32px; margin-top:8px;'>
        """, unsafe_allow_html=True)
        st.markdown(report_md)
        st.markdown("</div>", unsafe_allow_html=True)


# ── Main Router ────────────────────────────────────────────────────────────────
def main():
    sidebar()

    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "assessment":
        page_assessment()
    elif page == "results":
        page_results()
    elif page == "careers":
        page_careers()
    elif page == "famous":
        page_famous()
    elif page == "report":
        page_report()


if __name__ == "__main__":
    main()
