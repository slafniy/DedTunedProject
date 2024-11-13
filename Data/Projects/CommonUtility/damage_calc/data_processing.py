import typing as t
import pandas as pd
import numpy as np


def get_per_round_stats(df):
    return df.groupby(['iteration_number', 'level', 'name']).agg(
        mean_round_damage=('round_damage', 'mean'),
        # median_round_damage=('round_damage', 'median'),
        # max_round_damage=('round_damage', 'max'),
        # percentile_10_round_damage=('round_damage', lambda x: x.quantile(0.1)),
        # percentile_90_round_damage=('round_damage', lambda x: x.quantile(0.9))
    ).reset_index()


def get_overall_stats(df):
    return df.groupby(['level', 'name']).agg(
        mean_DPR=('mean_round_damage', 'mean'),
        # median_DPR=('median_round_damage', 'mean'),
        # percentile_10_DPR=('percentile_10_round_damage', 'mean'),
        # percentile_90_DPR=('percentile_90_round_damage', 'mean')
    ).reset_index()
