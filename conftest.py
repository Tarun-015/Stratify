"""
Shared pytest fixtures for Stratify tests.
These fixtures are automatically available in all test files.
"""
import pytest
import pandas as pd
import numpy as np


# ── Tournament fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def sample_tournaments_df():
    """Minimal valid tournaments DataFrame matching your CSV schema."""
    return pd.DataFrame({
        "tournament_name": ["The International", "ESL One", "BLAST Premier", "PGL Major", "DreamHack"],
        "game":            ["Dota 2", "CS2", "CS2", "CS2", "Dota 2"],
        "prize_pool_usd":  [40_000_000, 1_000_000, 500_000, 1_250_000, 300_000],
        "year":            [2023, 2023, 2023, 2022, 2022],
        "participants":    [16, 16, 24, 24, 16],
        "editions":        [12, 8, 6, 5, 9],
        "region":          ["Global", "EU", "EU", "Global", "EU"],
    })


@pytest.fixture
def empty_tournaments_df():
    """Empty DataFrame with correct columns — tests edge case handling."""
    return pd.DataFrame(columns=[
        "tournament_name", "game", "prize_pool_usd",
        "year", "participants", "editions", "region"
    ])


# ── Teams fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def sample_teams_df():
    """Minimal valid teams DataFrame."""
    return pd.DataFrame({
        "team_name":       ["Team Liquid", "Navi", "FaZe Clan", "Cloud9", "G2 Esports"],
        "game":            ["CS2", "CS2", "CS2", "CS2", "CS2"],
        "total_earnings":  [5_000_000, 4_200_000, 3_800_000, 2_100_000, 3_300_000],
        "tournaments_won": [12, 10, 8, 5, 9],
        "tournaments_played": [40, 38, 35, 30, 36],
        "region":          ["NA", "EU", "EU", "NA", "EU"],
    })


# ── YouTube / Creator fixtures ────────────────────────────────────────────────

@pytest.fixture
def sample_creators_df():
    """Minimal valid YouTube creators DataFrame."""
    return pd.DataFrame({
        "channel_name":    ["Shroud", "Ninja", "pokimane", "Valkyrae", "TimTheTatman"],
        "subscribers":     [10_600_000, 24_000_000, 9_300_000, 3_900_000, 7_300_000],
        "total_views":     [3_200_000_000, 24_000_000_000, 1_400_000_000, 800_000_000, 2_100_000_000],
        "avg_views":       [450_000, 820_000, 310_000, 280_000, 390_000],
        "videos_per_month":[8, 12, 15, 10, 9],
        "game_category":   ["FPS", "Battle Royale", "Variety", "Battle Royale", "Variety"],
        "growth_rate_pct": [2.1, -0.8, 1.4, 3.2, 1.8],
    })


# ── Games / Genre fixtures ────────────────────────────────────────────────────

@pytest.fixture
def sample_games_df():
    """Minimal valid games DataFrame."""
    return pd.DataFrame({
        "game_name":       ["Fortnite", "CS2", "Dota 2", "League of Legends", "Valorant"],
        "genre":           ["Battle Royale", "FPS", "MOBA", "MOBA", "FPS"],
        "active_players":  [3_500_000, 1_200_000, 800_000, 7_500_000, 2_000_000],
        "total_earnings":  [100_000_000, 200_000_000, 300_000_000, 90_000_000, 50_000_000],
        "tournaments_2023":[50, 120, 80, 90, 60],
        "hype_score":      [7.2, 8.5, 6.8, 7.9, 8.1],
        "release_year":    [2017, 2012, 2013, 2009, 2020],
    })


# ── Numeric edge-case fixtures ────────────────────────────────────────────────

@pytest.fixture
def single_row_df(sample_tournaments_df):
    """Tests that models handle single-row inputs gracefully."""
    return sample_tournaments_df.head(1)


@pytest.fixture
def df_with_nulls(sample_creators_df):
    """DataFrame containing NaN values — tests null handling."""
    df = sample_creators_df.copy()
    df.loc[0, "growth_rate_pct"] = float("nan")
    df.loc[2, "avg_views"] = float("nan")
    return df


@pytest.fixture
def df_with_zeros(sample_teams_df):
    """DataFrame with zero values — tests division-by-zero safety."""
    df = sample_teams_df.copy()
    df.loc[0, "tournaments_played"] = 0
    return df
