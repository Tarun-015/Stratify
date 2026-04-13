"""
Tests for the Engagement Clustering model.
"""
import pytest
import pandas as pd
import numpy as np


def compute_engagement_clusters(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Placeholder using simple quantile-based clustering.
    Replace with your actual KMeans import once restructured.
    """
    df = df.copy()
    df["engagement_rate"] = (df["avg_views"] / df["subscribers"].replace(0, np.nan)).fillna(0)

    df["cluster"] = pd.qcut(
        df["engagement_rate"],
        q=min(n_clusters, len(df)),
        labels=list(range(min(n_clusters, len(df)))),
        duplicates="drop"
    ).astype(int)

    cluster_labels = {0: "low_engagement", 1: "mid_engagement", 2: "high_engagement"}
    df["cluster_label"] = df["cluster"].map(cluster_labels).fillna("high_engagement")
    return df[["channel_name", "cluster", "cluster_label", "engagement_rate"]]


class TestEngagementClustering:

    def test_output_has_required_columns(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        for col in ["channel_name", "cluster", "cluster_label"]:
            assert col in result.columns

    def test_cluster_ids_are_integers(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        assert result["cluster"].dtype in ["int32", "int64", int]

    def test_cluster_count_within_bounds(self, sample_creators_df):
        n = 3
        result = compute_engagement_clusters(sample_creators_df, n_clusters=n)
        assert result["cluster"].nunique() <= n

    def test_all_rows_assigned_cluster(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        assert result["cluster"].notna().all()

    def test_row_count_preserved(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        assert len(result) == len(sample_creators_df)

    def test_cluster_labels_are_strings(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        assert pd.api.types.is_string_dtype(result["cluster_label"])

    def test_n_clusters_one_works(self, sample_creators_df):
        """Edge case: n_clusters=1 should assign all to same cluster."""
        result = compute_engagement_clusters(sample_creators_df, n_clusters=1)
        assert result["cluster"].nunique() == 1

    def test_engagement_rate_non_negative(self, sample_creators_df):
        result = compute_engagement_clusters(sample_creators_df)
        assert (result["engagement_rate"] >= 0).all()
