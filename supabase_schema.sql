-- =========================================================================
-- Supabase Schema for 2026 F1 Predictions
-- Run this in the Supabase SQL Editor to create all tables.
-- =========================================================================

-- Drivers reference data
CREATE TABLE IF NOT EXISTS drivers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    driver_name TEXT NOT NULL UNIQUE,
    driver_number INT NOT NULL,
    driver_team TEXT NOT NULL
);

-- Constructors reference data
CREATE TABLE IF NOT EXISTS constructors (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    team_color TEXT NOT NULL
);

-- Races reference data
CREATE TABLE IF NOT EXISTS races (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    round_number TEXT NOT NULL UNIQUE,
    race_name TEXT NOT NULL,
    race_date TEXT NOT NULL
);

-- Season Predictions (one row per user)
CREATE TABLE IF NOT EXISTS season_predictions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "user" TEXT NOT NULL UNIQUE,
    "D1"  TEXT, "D2"  TEXT, "D3"  TEXT, "D4"  TEXT, "D5"  TEXT,
    "D6"  TEXT, "D7"  TEXT, "D8"  TEXT, "D9"  TEXT, "D10" TEXT,
    "D11" TEXT, "D12" TEXT, "D13" TEXT, "D14" TEXT, "D15" TEXT,
    "D16" TEXT, "D17" TEXT, "D18" TEXT, "D19" TEXT, "D20" TEXT,
    "D21" TEXT, "D22" TEXT,
    "C1"  TEXT, "C2"  TEXT, "C3"  TEXT, "C4"  TEXT, "C5"  TEXT,
    "C6"  TEXT, "C7"  TEXT, "C8"  TEXT, "C9"  TEXT, "C10" TEXT,
    "C11" TEXT
);

-- Race Predictions (one row per user + race)
CREATE TABLE IF NOT EXISTS race_predictions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    race TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "P1"  TEXT, "P2"  TEXT, "P3"  TEXT, "P4"  TEXT, "P5"  TEXT,
    "P6"  TEXT, "P7"  TEXT, "P8"  TEXT, "P9"  TEXT, "P10" TEXT,
    "P11" TEXT, "P12" TEXT, "P13" TEXT, "P14" TEXT, "P15" TEXT,
    "P16" TEXT, "P17" TEXT, "P18" TEXT, "P19" TEXT, "P20" TEXT,
    "P21" TEXT, "P22" TEXT,
    UNIQUE (race, "user")
);

-- Fun Predictions (append-only, one row per prediction)
CREATE TABLE IF NOT EXISTS fun_predictions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "user" TEXT NOT NULL,
    prediction TEXT NOT NULL,
    date_created TEXT NOT NULL
);

-- Disable Row Level Security (trusted friends-only app)
ALTER TABLE drivers              DISABLE ROW LEVEL SECURITY;
ALTER TABLE constructors         DISABLE ROW LEVEL SECURITY;
ALTER TABLE races                DISABLE ROW LEVEL SECURITY;
ALTER TABLE season_predictions   DISABLE ROW LEVEL SECURITY;
ALTER TABLE race_predictions     DISABLE ROW LEVEL SECURITY;
ALTER TABLE fun_predictions      DISABLE ROW LEVEL SECURITY;

