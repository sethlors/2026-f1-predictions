"""Data loading and saving utilities."""
import os
import pandas as pd

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_drivers() -> pd.DataFrame:
    """Load drivers data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "drivers.csv"))


def load_constructors() -> pd.DataFrame:
    """Load constructors data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "constructors.csv"))


def load_races() -> pd.DataFrame:
    """Load races data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "races.csv"))


def load_season_predictions() -> pd.DataFrame:
    """Load season predictions data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))


def save_season_predictions(df: pd.DataFrame) -> None:
    """Save season predictions data to CSV."""
    df.to_csv(os.path.join(DATA_DIR, "season_predictions.csv"), index=False)


def load_race_predictions() -> pd.DataFrame:
    """Load race predictions data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))


def save_race_predictions(df: pd.DataFrame) -> None:
    """Save race predictions data to CSV."""
    df.to_csv(os.path.join(DATA_DIR, "race_predictions.csv"), index=False)


def load_fun_predictions() -> pd.DataFrame:
    """Load fun predictions data from CSV."""
    return pd.read_csv(os.path.join(DATA_DIR, "fun_predictions.csv"))


def save_fun_predictions(df: pd.DataFrame) -> None:
    """Save fun predictions data to CSV."""
    df.to_csv(os.path.join(DATA_DIR, "fun_predictions.csv"), index=False)
