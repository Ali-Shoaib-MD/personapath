"""
Plotly visualization functions for PersonaPath.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np


TRAIT_COLORS = {
    "Openness": "#6C63FF",
    "Conscientiousness": "#00C9A7",
    "Extraversion": "#FFB347",
    "Agreeableness": "#FF6B9D",
    "Neuroticism": "#4ECDC4",
}

BG_COLOR = "rgba(0,0,0,0)"
FONT_COLOR = "#E8E8F0"
GRID_COLOR = "rgba(255,255,255,0.08)"


def radar_chart(scores: dict) -> go.Figure:
    """Create a beautiful radar/spider chart for Big Five scores."""
    traits = list(scores.keys())
    values = list(scores.values())
    # Close the loop
    values_closed = values + [values[0]]
    traits_closed = traits + [traits[0]]

    fig = go.Figure()

    # Filled area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=traits_closed,
        fill="toself",
        fillcolor="rgba(108, 99, 255, 0.2)",
        line=dict(color="#6C63FF", width=2.5),
        name="Your Profile",
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>",
    ))

    # Outer ring markers
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=traits,
        mode="markers",
        marker=dict(
            size=10,
            color=[TRAIT_COLORS[t] for t in traits],
            symbol="circle",
            line=dict(width=2, color="white"),
        ),
        name="Traits",
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(20, 20, 40, 0.5)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=FONT_COLOR),
                gridcolor=GRID_COLOR,
                linecolor=GRID_COLOR,
                tickvals=[20, 40, 60, 80, 100],
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color=FONT_COLOR, family="Inter, sans-serif"),
                gridcolor=GRID_COLOR,
                linecolor=GRID_COLOR,
            ),
        ),
        showlegend=False,
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=60, r=60, t=40, b=40),
        height=420,
    )
    return fig


def comparison_radar(user_scores: dict, target_traits: list, target_name: str) -> go.Figure:
    """Radar chart comparing user to a career or famous person."""
    traits = list(user_scores.keys())
    user_vals = list(user_scores.values())
    user_closed = user_vals + [user_vals[0]]
    target_closed = target_traits + [target_traits[0]]
    traits_closed = traits + [traits[0]]

    fig = go.Figure()

    # Target profile
    fig.add_trace(go.Scatterpolar(
        r=target_closed,
        theta=traits_closed,
        fill="toself",
        fillcolor="rgba(255, 179, 71, 0.15)",
        line=dict(color="#FFB347", width=2, dash="dot"),
        name=target_name,
        hovertemplate=f"<b>{target_name}</b><br>%{{theta}}: %{{r:.0f}}<extra></extra>",
    ))

    # User profile
    fig.add_trace(go.Scatterpolar(
        r=user_closed,
        theta=traits_closed,
        fill="toself",
        fillcolor="rgba(108, 99, 255, 0.2)",
        line=dict(color="#6C63FF", width=2.5),
        name="You",
        hovertemplate="<b>You</b><br>%{theta}: %{r:.0f}<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(20, 20, 40, 0.5)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color=FONT_COLOR),
                gridcolor=GRID_COLOR,
                linecolor=GRID_COLOR,
                tickvals=[25, 50, 75, 100],
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color=FONT_COLOR),
                gridcolor=GRID_COLOR,
                linecolor=GRID_COLOR,
            ),
        ),
        showlegend=True,
        legend=dict(
            font=dict(color=FONT_COLOR, size=12),
            bgcolor="rgba(0,0,0,0)",
            x=0.85, y=1.1,
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=60, r=80, t=40, b=40),
        height=380,
    )
    return fig


def trait_bars(scores: dict) -> go.Figure:
    """Horizontal bar chart of trait scores."""
    traits = list(scores.keys())
    values = list(scores.values())
    colors = [TRAIT_COLORS[t] for t in traits]

    fig = go.Figure(go.Bar(
        x=values,
        y=traits,
        orientation="h",
        marker=dict(
            color=colors,
            opacity=0.85,
            line=dict(width=0),
        ),
        text=[f"{v:.0f}" for v in values],
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=13),
        hovertemplate="<b>%{y}</b>: %{x:.1f}<extra></extra>",
    ))

    fig.update_layout(
        xaxis=dict(
            range=[0, 115],
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            showgrid=True,
            title=dict(text="Score (0–100)", font=dict(color=FONT_COLOR)),
        ),
        yaxis=dict(
            tickfont=dict(size=13, color=FONT_COLOR),
            showgrid=False,
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=20, r=40, t=20, b=20),
        height=280,
        bargap=0.35,
    )
    return fig


def career_match_bar(career_matches: list) -> go.Figure:
    """Horizontal bar chart showing top career matches."""
    names = [m["name"] for m in reversed(career_matches)]
    scores = [m["score"] for m in reversed(career_matches)]
    emojis = [m["emoji"] for m in reversed(career_matches)]

    # Gradient colors for bars
    bar_colors = ["#6C63FF", "#00C9A7", "#FFB347", "#FF6B9D", "#4ECDC4"]
    bar_colors_reversed = bar_colors[:len(names)]

    fig = go.Figure(go.Bar(
        x=scores,
        y=[f"{e} {n}" for e, n in zip(emojis, names)],
        orientation="h",
        marker=dict(
            color=bar_colors_reversed,
            opacity=0.85,
        ),
        text=[f"{s:.1f}%" for s in scores],
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=12),
        hovertemplate="<b>%{y}</b><br>Match: %{x:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        xaxis=dict(
            range=[0, 110],
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title=dict(text="Compatibility %", font=dict(color=FONT_COLOR)),
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=FONT_COLOR),
            showgrid=False,
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=20, r=60, t=10, b=20),
        height=280,
        bargap=0.3,
    )
    return fig
