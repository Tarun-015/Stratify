"""
Tests for the Tournament Stability Score model.
"""
import pytest
import pandas as pd
import numpy as np


def compute_tournament_stability(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder — replace with your actual model import."""
    df = df.copy()
    max_editions = df["editions"].max() or 1
    max_prize    = df["prize_pool_usd"].max() or 1

    df["longevity_score"]  = df["editions"] / max_editions
    df["prize_consistency"]= df["prize_pool_usd"] / max_prize
    df["stability_score"]  = round(
        (df["longevity_score"] * 0.6 + df["prize_consistency"] * 0.4) * 10, 2
    ).clip(0, 10)

    df["stability_label"] = df["stability_score"].apply(
        lambda s: "stable" if s >= 7 else ("moderate" if s >= 4 else "at_risk")
    )
    return df[["tournament_name", "stability_score", "stability_label", "editions"]]


class TestTournamentStabilityScore:

    def test_output_has_required_columns(self, sample_tournaments_df):
        result = compute_tournament_stability(sample_tournaments_df)
        for col in ["tournament_name", "stability_score", "stability_label"]:
            assert col in result.columns

    def test_stability_score_in_range(self, sample_tournaments_df):
        result = compute_tournament_stability(sample_tournaments_df)
        assert result["stability_score"].between(0, 10).all()

    def test_stability_label_valid(self, sample_tournaments_df):
        result = compute_tournament_stability(sample_tournaments_df)
        valid = {"stable", "moderate", "at_risk"}
        actual = set(result["stability_label"].unique())
        assert actual.issubset(valid)

    def test_older_tournament_more_stable(self):
        """More editions should yield higher stability."""
        df = pd.DataFrame({
            "tournament_name": ["Old", "New"],
            "game":            ["Dota 2", "Valorant"],
            "prize_pool_usd":  [1_000_000, 1_000_000],
            "year":            [2023, 2023],
            "participants":    [16, 16],
            "editions":        [12, 1],
            "region":          ["Global", "NA"],
        })
        result = compute_tournament_stability(df)
        old_score = result[result["tournament_name"] == "Old"]["stability_score"].iloc[0]
        new_score = result[result["tournament_name"] == "New"]["stability_score"].iloc[0]
        assert old_score > new_score

    def test_empty_df_returns_empty(self, empty_tournaments_df):
        empty_tournaments_df["editions"] = pd.Series(dtype=float)
        empty_tournaments_df["prize_pool_usd"] = pd.Series(dtype=float)
        result = compute_tournament_stability(empty_tournaments_df)
        assert len(result) == 0

    def test_no_null_scores(self, sample_tournaments_df):
        result = compute_tournament_stability(sample_tournaments_df)
        assert result["stability_score"].notna().all()

    def test_single_row_input(self, single_row_df):
        result = compute_tournament_stability(single_row_df)
        assert len(result) == 1
        assert result.iloc[0]["stability_score"] == 10.0
