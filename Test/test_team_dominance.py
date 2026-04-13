"""
Tests for the Team Dominance Index model.
"""
import pytest
import pandas as pd


def compute_team_dominance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder mirroring your model's interface.
    Replace with: from src.stratify.models.team_dominance import TeamDominanceIndex
    """
    df = df.copy()
    df["win_rate"] = df.apply(
        lambda r: r["tournaments_won"] / r["tournaments_played"]
        if r["tournaments_played"] > 0 else 0.0,
        axis=1
    )
    max_earnings = df["total_earnings"].max() or 1
    df["earnings_norm"] = df["total_earnings"] / max_earnings

    df["dominance_index"] = round(
        (df["win_rate"] * 0.5 + df["earnings_norm"] * 0.5) * 10, 2
    )
    df["dominance_index"] = df["dominance_index"].clip(0, 10)
    df["rank"] = df["dominance_index"].rank(ascending=False, method="min").astype(int)
    return df[["team_name", "game", "dominance_index", "rank", "win_rate"]]


class TestTeamDominanceIndex:

    def test_output_has_required_columns(self, sample_teams_df):
        result = compute_team_dominance(sample_teams_df)
        for col in ["team_name", "dominance_index", "rank", "win_rate"]:
            assert col in result.columns

    def test_dominance_score_in_range(self, sample_teams_df):
        result = compute_team_dominance(sample_teams_df)
        assert result["dominance_index"].between(0, 10).all(), \
            "Dominance index must be 0–10"

    def test_rank_starts_at_one(self, sample_teams_df):
        result = compute_team_dominance(sample_teams_df)
        assert result["rank"].min() == 1

    def test_rank_is_unique_per_team(self, sample_teams_df):
        result = compute_team_dominance(sample_teams_df)
        assert result["rank"].nunique() == len(result)

    def test_win_rate_between_zero_and_one(self, sample_teams_df):
        result = compute_team_dominance(sample_teams_df)
        assert result["win_rate"].between(0, 1).all()

    def test_zero_tournaments_played_safe(self, df_with_zeros):
        """Should not raise ZeroDivisionError."""
        result = compute_team_dominance(df_with_zeros)
        assert result["win_rate"].notna().all()
        assert result["dominance_index"].notna().all()

    def test_higher_win_rate_yields_higher_score(self):
        """Team with 100% win rate should outscore team with 0%."""
        df = pd.DataFrame({
            "team_name": ["WinnerTeam", "LoserTeam"],
            "game": ["CS2", "CS2"],
            "total_earnings": [1_000_000, 1_000_000],
            "tournaments_won": [10, 0],
            "tournaments_played": [10, 10],
            "region": ["EU", "EU"],
        })
        result = compute_team_dominance(df)
        winner = result[result["team_name"] == "WinnerTeam"]["dominance_index"].iloc[0]
        loser  = result[result["team_name"] == "LoserTeam"]["dominance_index"].iloc[0]
        assert winner > loser

    def test_single_team_input(self):
        df = pd.DataFrame({
            "team_name": ["Solo Team"],
            "game": ["Dota 2"],
            "total_earnings": [500_000],
            "tournaments_won": [3],
            "tournaments_played": [10],
            "region": ["NA"],
        })
        result = compute_team_dominance(df)
        assert len(result) == 1
        assert result.iloc[0]["rank"] == 1
