"""Shared constants used across the application."""

# User configuration
USERS = ["Seth", "Colin"]

# Team colors for badges and styling
TEAM_COLORS = {
    "McLaren": "#FF8700",
    "Mercedes": "#00D2BE",
    "Red Bull": "#1E41FF",
    "Ferrari": "#DC0000",
    "Williams": "#005AFF",
    "Racing Bulls": "#2B4562",
    "Aston Martin": "#006F62",
    "Haas": "#B6BABD",
    "Audi": "#C0C0C0",
    "Alpine": "#0090FF",
    "Cadillac": "#FFD700",
}

# Season predictions configuration
NUM_DRIVERS = 22
NUM_CONSTRUCTORS = 11
DRIVER_POSITIONS = [f"D{i}" for i in range(1, NUM_DRIVERS + 1)]
CONSTRUCTOR_POSITIONS = [f"C{i}" for i in range(1, NUM_CONSTRUCTORS + 1)]
PLACEHOLDER = "-- Select --"

# Race configuration
NUM_RACES = 24
