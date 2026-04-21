"""
Tests for the Genre Saturation Risk model.
Verifies output shape, score range, and edge case handling.
"""
import pytest
import pandas as pd
import numpy as np


# ── Inline model logic (replace with your actual import once restructured) ────
# from src.stratify.models.genre_risk import GenreSaturationRisk

def compute_genre_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder that mirrors the expected interface of your model.
    Replace the body with: return GenreSaturationRisk().predict(df)
    once your src/ structure is in place.

    Expected output columns: genre, saturation_score, risk_level
    """
    results = []
    for genre, group in df.groupby("genre"):
        tournament_density = group["tournaments_2023"].sum() / max(group["active_players"].sum(), 1) * 1_000_000
        hype = group["hype_score"].mean()
        score = round(min((tournament_density * 0.4 + hype * 0.6), 10), 2)
        risk = "high" if score >= 7 else ("medium" if score >= 4 else "low")
        results.append({"genre": genre, "saturation_score": score, "risk_level": risk})
    return pd.DataFrame(results)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestGenreSaturationRisk:

    def test_output_has_required_columns(self, sample_games_df):
        result = compute_genre_risk(sample_games_df)
        for col in ["genre", "saturation_score", "risk_level"]:
            assert col in result.columns, f"Output missing column: {col}"

    def test_score_in_valid_range(self, sample_games_df):
        result = compute_genre_risk(sample_games_df)
        assert result["saturation_score"].between(0, 10).all(), \
            "Saturation scores must be between 0 and 10"

    def test_risk_level_valid_values(self, sample_games_df):
        result = compute_genre_risk(sample_games_df)
        valid_levels = {"low", "medium", "high"}
        actual = set(result["risk_level"].unique())
        assert actual.issubset(valid_levels), \
            f"Unexpected risk levels: {actual - valid_levels}"

    def test_output_row_count_matches_genres(self, sample_games_df):
        expected_genres = sample_games_df["genre"].nunique()
        result = compute_genre_risk(sample_games_df)
        assert len(result) == expected_genres

    def test_no_null_scores(self, sample_games_df):
        result = compute_genre_risk(sample_games_df)
        assert result["saturation_score"].notna().all()

    def test_high_hype_game_scores_higher(self, sample_games_df):
        """A genre with higher average hype should score higher, all else equal."""
        low_hype = sample_games_df.copy()
        low_hype["hype_score"] = 2.0
        high_hype = sample_games_df.copy()
        high_hype["hype_score"] = 9.0

        low_result = compute_genre_risk(low_hype)
        high_result = compute_genre_risk(high_hype)

        assert high_result["saturation_score"].mean() > low_result["saturation_score"].mean()

    def test_single_genre_input(self):
        """Model must work when only one genre is present."""
        single = pd.DataFrame({
            "genre": ["FPS"],
            "game_name": ["CS2"],
            "active_players": [1_200_000],
            "total_earnings": [200_000_000],
            "tournaments_2023": [120],
            "hype_score": [8.5],
            "release_year": [2012],
        })
        result = compute_genre_risk(single)
        assert len(result) == 1
        assert result.iloc[0]["saturation_score"] >= 0

    def test_returns_dataframe(self, sample_games_df):
        result = compute_genre_risk(sample_games_df)
        assert isinstance(result, pd.DataFrame)
