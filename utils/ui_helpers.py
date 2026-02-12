"""UI helper functions for the F1 Predictions app."""
import pandas as pd
from utils.constants import TEAM_COLORS


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
    return TEAM_COLORS.get(team_name, "#666666")


def render_page_header(title: str, subtitle: str) -> str:
    """Generate HTML for a page header."""
    return f"""
    <div class="page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """
