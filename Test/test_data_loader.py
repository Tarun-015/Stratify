"""
Tests for data loading and schema validation.
Ensures your CSV files have the right columns, types, and no critical nulls.
"""
import pytest
import pandas as pd
import numpy as np


# ── Schema validation helpers ─────────────────────────────────────────────────

TOURNAMENT_REQUIRED_COLS = [
    "tournament_name", "game", "prize_pool_usd",
    "year", "participants", "editions"
]

TEAM_REQUIRED_COLS = [
    "team_name", "game", "total_earnings",
    "tournaments_won", "tournaments_played"
]

CREATOR_REQUIRED_COLS = [
    "channel_name", "subscribers", "total_views",
    "avg_views", "videos_per_month", "game_category"
]

GAME_REQUIRED_COLS = [
    "game_name", "genre", "active_players",
    "total_earnings", "hype_score"
]


# ── Tournament data tests ─────────────────────────────────────────────────────

class TestTournamentSchema:
    def test_has_required_columns(self, sample_tournaments_df):
        for col in TOURNAMENT_REQUIRED_COLS:
            assert col in sample_tournaments_df.columns, f"Missing column: {col}"

    def test_prize_pool_is_positive(self, sample_tournaments_df):
        assert (sample_tournaments_df["prize_pool_usd"] > 0).all(), \
            "All prize pools must be positive"

    def test_year_is_reasonable(self, sample_tournaments_df):
        assert sample_tournaments_df["year"].between(2000, 2030).all(), \
            "Year values out of expected range"

    def test_participants_is_positive_integer(self, sample_tournaments_df):
        assert (sample_tournaments_df["participants"] > 0).all()
        assert sample_tournaments_df["participants"].dtype in [int, "int64", "int32"]

    def test_no_null_in_critical_columns(self, sample_tournaments_df):
        critical = ["tournament_name", "game", "prize_pool_usd"]
        for col in critical:
            assert sample_tournaments_df[col].notna().all(), \
                f"Null values found in critical column: {col}"

    def test_no_duplicate_entries(self, sample_tournaments_df):
        dupes = sample_tournaments_df.duplicated(subset=["tournament_name", "year"])
        assert not dupes.any(), "Duplicate tournament+year entries found"

    def test_empty_dataframe_handled(self, empty_tournaments_df):
        assert len(empty_tournaments_df) == 0
        for col in TOURNAMENT_REQUIRED_COLS:
            assert col in empty_tournaments_df.columns


# ── Teams data tests ──────────────────────────────────────────────────────────

class TestTeamSchema:
    def test_has_required_columns(self, sample_teams_df):
        for col in TEAM_REQUIRED_COLS:
            assert col in sample_teams_df.columns, f"Missing column: {col}"

    def test_earnings_non_negative(self, sample_teams_df):
        assert (sample_teams_df["total_earnings"] >= 0).all()

    def test_win_rate_computable(self, sample_teams_df):
        """tournaments_won must never exceed tournaments_played."""
        assert (sample_teams_df["tournaments_won"] <= sample_teams_df["tournaments_played"]).all(), \
            "tournaments_won cannot exceed tournaments_played"

    def test_no_null_team_names(self, sample_teams_df):
        assert sample_teams_df["team_name"].notna().all()

    def test_division_by_zero_safety(self, df_with_zeros):
        """Win rate calculation should not crash when tournaments_played = 0."""
        df = df_with_zeros.copy()
        df["win_rate"] = df.apply(
            lambda r: r["tournaments_won"] / r["tournaments_played"]
            if r["tournaments_played"] > 0 else 0.0,
            axis=1
        )
        assert df["win_rate"].notna().all()
        assert (df["win_rate"] >= 0).all()


# ── Creator data tests ────────────────────────────────────────────────────────

class TestCreatorSchema:
    def test_has_required_columns(self, sample_creators_df):
        for col in CREATOR_REQUIRED_COLS:
            assert col in sample_creators_df.columns, f"Missing column: {col}"

    def test_subscribers_positive(self, sample_creators_df):
        assert (sample_creators_df["subscribers"] > 0).all()

    def test_avg_views_non_negative(self, sample_creators_df):
        assert (sample_creators_df["avg_views"] >= 0).all()

    def test_null_handling_in_growth_rate(self, df_with_nulls):
        """Model must handle NaN growth_rate_pct gracefully."""
        cleaned = df_with_nulls["growth_rate_pct"].fillna(0.0)
        assert cleaned.notna().all()

    def test_no_duplicate_channels(self, sample_creators_df):
        assert not sample_creators_df["channel_name"].duplicated().any()

    def test_videos_per_month_reasonable(self, sample_creators_df):
        assert sample_creators_df["videos_per_month"].between(0, 365).all()


# ── Games data tests ──────────────────────────────────────────────────────────

class TestGameSchema:
    def test_has_required_columns(self, sample_games_df):
        for col in GAME_REQUIRED_COLS:
            assert col in sample_games_df.columns, f"Missing column: {col}"

    def test_hype_score_in_range(self, sample_games_df):
        assert sample_games_df["hype_score"].between(0, 10).all(), \
            "Hype score must be between 0 and 10"

    def test_active_players_positive(self, sample_games_df):
        assert (sample_games_df["active_players"] > 0).all()

    def test_genre_not_empty(self, sample_games_df):
        assert sample_games_df["genre"].notna().all()
        assert (sample_games_df["genre"].str.strip() != "").all()
