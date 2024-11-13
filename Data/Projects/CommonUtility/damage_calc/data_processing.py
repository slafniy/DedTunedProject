import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def process(raw_data):
    df = pd.DataFrame(raw_data)
    df = _get_per_round_stats(df)
    df = _get_overall_stats(df)
    return df


def _get_per_round_stats(df):
    return df.groupby(['iteration_number', 'level', 'name', 'target_ac']).agg(
        mean_round_damage=('round_damage', 'mean')
    ).reset_index()


def _get_overall_stats(df):
    return df.groupby(['level', 'name', 'target_ac']).agg(
        mean_DPR=('mean_round_damage', 'mean')
    ).reset_index()


def get_plot(df_overall: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    unique_combinations = df_overall[['name', 'target_ac']].drop_duplicates()

    for _, row in unique_combinations.iterrows():
        name_value = row['name']
        target_ac_value = row['target_ac']

        df_filtered = df_overall[(df_overall['name'] == name_value) & (df_overall['target_ac'] == target_ac_value)]

        color_index = unique_combinations.index[(unique_combinations['name'] == name_value) &
                                                (unique_combinations['target_ac'] == target_ac_value)].tolist()[0]
        color = px.colors.qualitative.Set1[color_index % len(px.colors.qualitative.Set1)]

        fig.add_trace(go.Scatter(
            x=df_filtered['level'],
            y=df_filtered['mean_DPR'],
            mode='lines+markers',
            name=f'AC{target_ac_value} {name_value}',
            line=dict(color=color)
        ))

    fig.update_layout(height=800)

    return fig
