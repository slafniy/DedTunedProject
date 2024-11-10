import typing as t
import pandas as pd
import numpy as np


def aggregated_stats_from_raw(raw_data: t.List[t.List[float]]) -> pd.DataFrame:
        """
        Return DataFrame with aggregated statistics
        columns are aggregate over all iterations, rows are combat parameters.
        E.g. in combat we have mean DPR and percentile_10 DRP - aggregated data over combat turns
        And overall we can aggregate this per-combat stats, e.g. "mean value of combat_percentile_90 over all combats"
        """
        df = pd.DataFrame(raw_data)

        dpr_stats_per_combat = pd.DataFrame({
            'combat_DRP_mean': df.mean(axis=1),
            'combat_DRP_median': df.median(axis=1),
            'combat_DRP_percentile_90': df.apply(lambda row: np.percentile(row, 90), axis=1),
            'combat_DRP_percentile_10': df.apply(lambda row: np.percentile(row, 10), axis=1),
            'combat_DRP_max': df.max(axis=1),
            'combat_DRP_min': df.min(axis=1)
        })

        dpr_stats_overall = pd.DataFrame({
            'overall_mean': dpr_stats_per_combat.mean(),
            'overall_median': dpr_stats_per_combat.median(),
            'overall_percentile_10': dpr_stats_per_combat.apply(lambda col: np.percentile(col, 10), axis=0),
            'overall_percentile_90': dpr_stats_per_combat.apply(lambda col: np.percentile(col, 90), axis=0),
            'overall_max': dpr_stats_per_combat.max(),
            'overall_min': dpr_stats_per_combat.min()
        })

        return dpr_stats_overall


def get_series_median_and_percentiles(name: str, stats_overall: pd.DataFrame) -> dict:
    """Return dictionary with keys name, median, percentile_10, percentile_90"""
    combat_DPR_mean_stats = stats_overall.T

    return {
        'name': name,
        'median': combat_DPR_mean_stats.combat_DRP_mean.loc['overall_median'],
        'percentile_10': combat_DPR_mean_stats.combat_DRP_mean.loc['overall_percentile_10'],
        'percentile_90': combat_DPR_mean_stats.combat_DRP_mean.loc['overall_percentile_90']
    }


