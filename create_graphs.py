import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def update_graph(figure,colors,title):
    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=title,
        title_x=0.5,
        font=dict(
            size=14,
            color=colors['marker']
        ),
        xaxis=dict(showline=True),
        yaxis=dict(showline=True)
        # xaxis_tickangle=-45
    )
    figure.update_traces(
        marker_color=colors['marker']
    )
    return figure


def generate_bubble_chart(df,colors,title):
    figure=px.scatter(
        df,
        x=df.columns[0],
        y=df.columns[1],
        size=df.columns[2],
        width=1400
    )
    figure=update_graph(figure,colors,title)
    figure.update_xaxes(showgrid=False, zeroline=False)
    # figure.update_yaxes(showgrid=False, zeroline=False)
    figure=figure.update_layout(
        xaxis_tickangle=-45
    )
    return figure


def generate_bar_chart(df,colors,title):
    figure=px.bar(
        df,
        x=df.columns[0],
        y=df.columns[1]
    )
    figure=update_graph(figure,colors,title)
    return figure