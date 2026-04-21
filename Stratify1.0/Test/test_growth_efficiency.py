"""
Tests for Growth Efficiency Index model.
"""
import pytest
import pandas as pd
import numpy as np


def compute_growth_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder — replace with your actual model import."""
    df = df.copy()
    df["engagement_rate"] = df["avg_views"] / df["subscribers"].replace(0, np.nan)
    max_growth = df["growth_rate_pct"].abs().max() or 1
    df["growth_norm"] = df["growth_rate_pct"] / max_growth

    df["gei"] = round(
        (df["engagement_rate"].fillna(0) * 0.5 + df["growth_norm"].fillna(0) * 0.5) * 100, 1
    ).clip(0, 100)

    df["tier"] = pd.cut(
        df["gei"],
        bins=[-1, 33, 66, 100],
        labels=["low", "medium", "high"]
    )
    return df[["channel_name", "gei", "tier", "engagement_rate"]]


class TestGrowthEfficiencyIndex:

    def test_output_has_required_columns(self, sample_creators_df):
        result = compute_growth_efficiency(sample_creators_df)
        for col in ["channel_name", "gei", "tier"]:
            assert col in result.columns

    def test_gei_in_range(self, sample_creators_df):
        result = compute_growth_efficiency(sample_creators_df)
        assert result["gei"].between(0, 100).all(), "GEI must be 0–100"

    def test_tier_valid_values(self, sample_creators_df):
        result = compute_growth_efficiency(sample_creators_df)
        valid = {"low", "medium", "high"}
        actual = set(result["tier"].dropna().unique())
        assert actual.issubset(valid)

    def test_null_growth_rate_handled(self, df_with_nulls):
        """NaN growth_rate_pct must not crash or produce NaN GEI."""
        result = compute_growth_efficiency(df_with_nulls)
        assert result["gei"].notna().all()

    def test_row_count_preserved(self, sample_creators_df):
        result = compute_growth_efficiency(sample_creators_df)
        assert len(result) == len(sample_creators_df)

    def test_higher_engagement_scores_higher(self):
        base = pd.DataFrame({
            "channel_name":    ["High", "Low"],
            "subscribers":     [1_000_000, 1_000_000],
            "total_views":     [500_000_000, 500_000_000],
            "avg_views":       [500_000, 10_000],
            "videos_per_month":[10, 10],
            "game_category":   ["FPS", "FPS"],
            "growth_rate_pct": [5.0, 5.0],
        })
        result = compute_growth_efficiency(base)
        high_gei = result[result["channel_name"] == "High"]["gei"].iloc[0]
        low_gei  = result[result["channel_name"] == "Low"]["gei"].iloc[0]
        assert high_gei >= low_gei
