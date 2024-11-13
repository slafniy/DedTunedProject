import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def process(raw_data):
    df = pd.DataFrame(raw_data)
    df = _get_per_round_stats(df)
    df = _get_overall_stats(df)
    return df


def _get_per_round_stats(df):
    return df.groupby(['iteration_number', 'level', 'name']).agg(
        mean_round_damage=('round_damage', 'mean')
    ).reset_index()


def _get_overall_stats(df):
    return df.groupby(['level', 'name']).agg(
        mean_DPR=('mean_round_damage', 'mean')
    ).reset_index()


def get_plot(df_overall: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    for name_value in df_overall['name'].unique():
        df_name = df_overall[df_overall['name'] == name_value]
        color = px.colors.qualitative.Set1[df_overall['name'].unique().tolist().index(name_value)]

        fig.add_trace(go.Scatter(
            x=df_name['level'],
            y=df_name['mean_DPR'],
            mode='lines+markers',
            name=f'{name_value} Mean DPR',
            line=dict(color=color)
        ))

    fig.update_layout(height=800)

    return fig
