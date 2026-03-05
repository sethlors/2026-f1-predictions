"""UI helper functions for the F1 Predictions app."""
from __future__ import annotations

import pandas as pd
from datetime import date
from utils.constants import TEAM_COLORS


# ---------------------------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------------------------

def driver_with_team(name: str, drivers_df: pd.DataFrame) -> str:
    """Return 'Name — Team' for display."""
    row = drivers_df[drivers_df["Driver Name"] == name]
    if row.empty:
        return name
    team = row.iloc[0]["Driver Team"]
    return f"{name}  —  {team}"


def pos_class(i: int) -> str:
    """Return CSS class for position badge based on position number."""
    if i == 1:
        return "pos-gold"
    if i == 2:
        return "pos-silver"
    if i == 3:
        return "pos-bronze"
    if i <= 10:
        return "pos-points"
    return "pos-rest"


def get_team_color(team_name: str) -> str:
    """Get the color for a team badge."""
    return TEAM_COLORS.get(team_name, "#484f58")


# ---------------------------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------------------------

def render_navbar(active: str = "home") -> str:
    """Render a sticky top navigation bar with F1 branding.

    Parameters
    ----------
    active : one of 'home', 'season', 'race', 'fun'
    """
    def _link(label: str, page_key: str, href: str, icon: str) -> str:
        cls = "nav-link active" if active == page_key else "nav-link"
        return f'<a href="{href}" target="_self" class="{cls}">{icon} {label}</a>'

    links = (
        _link("Home", "home", "/", "")
        + _link("Season", "season", "/Season_Predictions", "")
        + _link("Race", "race", "/Race_Predictions", "")
        + _link("Fun", "fun", "/Fun_Predictions", "")
    )

    return (
        '<nav class="f1-navbar">'
        '<div class="nav-inner">'
        '<div class="nav-brand">'
        '<span class="brand-mark">F1</span>'
        '<span class="brand-text">PREDICTIONS</span>'
        '<span class="brand-year">2026</span>'
        '</div>'
        f'<div class="nav-links">{links}</div>'
        '</div>'
        '</nav>'
        '<div class="nav-spacer"></div>'
    )


# ---------------------------------------------------------------------------
# Page structure
# ---------------------------------------------------------------------------

def render_page_header(title: str, subtitle: str) -> str:
    """Generate HTML for a page header with carbon-fiber texture."""
    return (
        f'<div class="page-header">'
        f"<h1>{title}</h1>"
        f"<p>{subtitle}</p>"
        f"</div>"
    )


def render_hero(title: str, subtitle: str = "") -> str:
    """Generate HTML for the home hero section."""
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    return (
        f'<div class="hero"><h1>{title}</h1>{sub_html}</div>'
    )


def render_countdown(race_name: str, countdown_text: str) -> str:
    """Generate HTML for the next-race countdown bar."""
    return (
        f'<div class="countdown-bar">'
        f'<span class="race-name">Next Race: <span>{race_name}</span></span>'
        f'<span class="days-left">{countdown_text}</span>'
        f"</div>"
    )


def render_stat_cards(stats: list[tuple]) -> str:
    """Generate stat card row. stats = [(value, label), ...]"""
    cards = "".join(
        f'<div class="stat-card">'
        f'<div class="stat-value">{val}</div>'
        f'<div class="stat-label">{label}</div>'
        f"</div>"
        for val, label in stats
    )
    return f'<div class="stat-row">{cards}</div>'


def render_nav_cards(cards: list[tuple[str, str, str, str]]) -> str:
    """Generate clickable navigation cards.

    cards = [(icon, title, desc, href), ...]
    """
    items = "".join(
        f'<a href="{href}" target="_self" class="nav-card-link">'
        f'<div class="nav-card">'
        f'<div class="card-icon">{icon}</div>'
        f"<h3>{title}</h3>"
        f"<p>{desc}</p>"
        f'<div class="card-arrow">→</div>'
        f"</div></a>"
        for icon, title, desc, href in cards
    )
    return f'<div class="nav-cards">{items}</div>'


def render_section_header(title: str) -> str:
    """Generate a styled section header with accent line."""
    return (
        f'<div class="section-header">'
        f"<h2>{title}</h2>"
        f'<div class="accent-line"></div>'
        f"</div>"
    )


def render_divider(accent: bool = False) -> str:
    """Generate a styled divider."""
    cls = "f1-divider-accent" if accent else "f1-divider"
    return f'<div class="{cls}"></div>'


def render_footer() -> str:
    """Generate the app footer."""
    return (
        '<div class="app-footer">'
        'Built by <a href="https://github.com/sethlors" target="_blank">sethlors</a>'
        " · 2026 F1 Predictions"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Custom toast notifications (replaces st.success / st.error / st.info)
# ---------------------------------------------------------------------------

def render_toast(message: str, kind: str = "info") -> str:
    """Generate a custom toast notification.

    kind : 'success' | 'error' | 'info' | 'warning'
    """
    icons = {"success": "+", "error": "x", "info": "i", "warning": "!"}
    icon = icons.get(kind, "i")
    return (
        f'<div class="toast toast-{kind}">'
        f'<span class="toast-icon">{icon}</span>'
        f'<span class="toast-msg">{message}</span>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------

def render_empty_state(message: str, icon: str = "") -> str:
    """Render a styled empty state placeholder."""
    return (
        f'<div class="empty-state">'
        f'<div class="empty-icon">{icon}</div>'
        f'<div class="empty-msg">{message}</div>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Race calendar
# ---------------------------------------------------------------------------

def render_race_calendar(races_df: pd.DataFrame, max_races: int | None = None) -> str:
    """Render a grid of race calendar cards."""
    today = date.today()
    cards: list[str] = []
    found_next = False
    df = races_df if max_races is None else races_df.head(max_races)

    for _, row in df.iterrows():
        rnd = row["Round Number"]
        name = row["Race Name"]
        race_date_str = row["Race Date"]

        try:
            from datetime import datetime
            race_date = datetime.strptime(race_date_str, "%m/%d/%Y").date()
        except Exception:
            race_date = None

        extra_cls = ""
        if race_date:
            if race_date < today:
                extra_cls = "is-past"
            elif not found_next and race_date >= today:
                extra_cls = "is-next"
                found_next = True

        cards.append(
            f'<div class="calendar-race {extra_cls}">'
            f'<div class="calendar-round">{rnd}</div>'
            f'<div class="calendar-name">{name}</div>'
            f'<div class="calendar-date">{race_date_str}</div>'
            f"</div>"
        )

    return f'<div class="calendar-grid">{"".join(cards)}</div>'


# ---------------------------------------------------------------------------
# Podium display
# ---------------------------------------------------------------------------

def render_podium(
    drivers: list[str],
    driver_teams: dict[str, str],
) -> str:
    """Render a podium visualization for the top 3 drivers."""
    if len(drivers) < 3:
        return ""

    def _slot(driver: str, pos: int, css_cls: str) -> str:
        team = driver_teams.get(driver, "")
        color = TEAM_COLORS.get(team, "#484f58")
        return (
            f'<div class="podium-slot {css_cls}">'
            f'<div class="podium-driver">{driver}</div>'
            f'<div class="podium-team" style="color:{color};">{team}</div>'
            f'<div class="podium-block">{pos}</div>'
            f"</div>"
        )

    # Order: P2 (left), P1 (center), P3 (right)
    return (
        '<div class="podium-container">'
        + _slot(drivers[1], 2, "podium-2nd")
        + _slot(drivers[0], 1, "podium-1st")
        + _slot(drivers[2], 3, "podium-3rd")
        + "</div>"
    )


# ---------------------------------------------------------------------------
# Timing tower
# ---------------------------------------------------------------------------

def render_timing_tower(
    user: str,
    positions: list[str],
    pos_values: dict[str, str],
    driver_teams: dict[str, str],
    championship_label: str = "Drivers",
    placeholder: str = "-- Select --",
) -> str:
    """Render an F1-style timing tower for a user's predictions."""
    avatar_letter = user[0].upper() if user else "?"

    header = (
        f'<div class="timing-tower-header">'
        f'<div class="user-avatar">{avatar_letter}</div>'
        f'<div class="user-info">'
        f'<div class="user-label">{user}</div>'
        f'<div class="championship-label">{championship_label} Championship</div>'
        f"</div></div>"
    )

    rows: list[str] = []
    for i, pos in enumerate(positions, 1):
        name = pos_values.get(pos, "")
        if not name or name == placeholder:
            continue

        pc = pos_class(i)
        podium_cls = ""
        if i == 1:
            podium_cls = "podium-1"
        elif i == 2:
            podium_cls = "podium-2"
        elif i == 3:
            podium_cls = "podium-3"

        if championship_label == "Constructors":
            color = TEAM_COLORS.get(name, "#484f58")
            rows.append(
                f'<div class="timing-row {podium_cls}">'
                f'<div class="t-pos"><span class="pos-label {pc}">P{i}</span></div>'
                f'<div class="t-color-bar" style="background:{color};"></div>'
                f'<div class="t-driver" style="color:{color};">{name}</div>'
                f"</div>"
            )
        else:
            team = driver_teams.get(name, "")
            color = TEAM_COLORS.get(team, "#484f58")
            rows.append(
                f'<div class="timing-row {podium_cls}">'
                f'<div class="t-pos"><span class="pos-label {pc}">P{i}</span></div>'
                f'<div class="t-color-bar" style="background:{color};"></div>'
                f'<div class="t-driver">{name}</div>'
                f'<div class="t-team" style="color:{color};">{team}</div>'
                f"</div>"
            )

    body = f'<div class="timing-tower-body">{"".join(rows)}</div>'
    return f'<div class="timing-tower">{header}{body}</div>'
