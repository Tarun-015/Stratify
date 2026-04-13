"""
Tests for the Prize-to-Hype Ratio model.
"""
import pytest
import pandas as pd
import numpy as np


def compute_prize_hype_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder — replace with your actual model import."""
    df = df.copy()
    max_prize = df["prize_pool_usd"].max() or 1
    df["prize_norm"] = df["prize_pool_usd"] / max_prize * 10
    df["ratio"]      = round(df["prize_norm"] / df["hype_score"].replace(0, np.nan), 3)
    df["ratio"]      = df["ratio"].fillna(0)

    df["verdict"] = df["ratio"].apply(
        lambda r: "underhyped" if r > 1.2 else ("overhyped" if r < 0.8 else "balanced")
    )
    return df[["tournament_name", "ratio", "verdict", "prize_pool_usd"]]


class TestPrizeHypeRatio:

    def test_output_has_required_columns(self, sample_tournaments_df):
        merged = sample_tournaments_df.copy()
        merged["hype_score"] = [8.5, 6.0, 7.2, 7.8, 5.5]
        result = compute_prize_hype_ratio(merged)
        for col in ["tournament_name", "ratio", "verdict"]:
            assert col in result.columns

    def test_verdict_valid_values(self, sample_tournaments_df):
        df = sample_tournaments_df.copy()
        df["hype_score"] = [8.5, 6.0, 7.2, 7.8, 5.5]
        result = compute_prize_hype_ratio(df)
        valid = {"overhyped", "underhyped", "balanced"}
        assert set(result["verdict"].unique()).issubset(valid)

    def test_ratio_non_negative(self, sample_tournaments_df):
        df = sample_tournaments_df.copy()
        df["hype_score"] = [8.5, 6.0, 7.2, 7.8, 5.5]
        result = compute_prize_hype_ratio(df)
        assert (result["ratio"] >= 0).all()

    def test_zero_hype_score_safe(self, sample_tournaments_df):
        """Zero hype score must not raise ZeroDivisionError."""
        df = sample_tournaments_df.copy()
        df["hype_score"] = 0.0
        result = compute_prize_hype_ratio(df)
        assert result["ratio"].notna().all()

    def test_high_prize_low_hype_is_underhyped(self):
        df = pd.DataFrame({
            "tournament_name": ["BigPrize"],
            "game":            ["Dota 2"],
            "prize_pool_usd":  [40_000_000],
            "year":            [2023],
            "participants":    [16],
            "editions":        [12],
            "region":          ["Global"],
            "hype_score":      [1.0],
        })
        result = compute_prize_hype_ratio(df)
        assert result.iloc[0]["verdict"] == "underhyped"

    def test_low_prize_high_hype_is_overhyped(self):
        df = pd.DataFrame({
            "tournament_name": ["BigTournament", "HypeTournament"],
            "game":            ["Dota 2", "Mobile Game"],
            "prize_pool_usd":  [10_000_000, 10_000],
            "year":            [2023, 2023],
            "participants":    [16, 16],
            "editions":        [5, 1],
            "region":          ["Global", "NA"],
            "hype_score":      [5.0, 9.5],
        })
        result = compute_prize_hype_ratio(df)
        hype_verdict = result[result["tournament_name"] == "HypeTournament"]["verdict"].iloc[0]
        assert hype_verdict == "overhyped"

    def test_row_count_preserved(self, sample_tournaments_df):
        df = sample_tournaments_df.copy()
        df["hype_score"] = [8.5, 6.0, 7.2, 7.8, 5.5]
        result = compute_prize_hype_ratio(df)
        assert len(result) == len(df)
