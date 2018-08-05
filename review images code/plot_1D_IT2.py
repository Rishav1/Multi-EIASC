from plotly import tools
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np

x = np.linspace(-6, 6, 1001)

z1 = np.maximum(1 - abs(x)/5, x*0)
z2 = np.maximum(1 - abs(x)/3, x*0)

trace1 = go.Scatter(
    x = x,
    y = z1,
    marker=dict(
        size=4,
        cmax=39,
        cmin=0,
        color=np.floor(z1*40),
        colorbar=dict(
            title='Membership',
            tickvals=[],
        ),
        colorscale='Viridis'
    ),
    mode='markers',
)

trace2 = go.Scatter(
    x = x,
    y = z2,
    marker=dict(
        size=4,
        cmax=39,
        cmin=0,
        color=np.floor(z2*40),
        colorbar=dict(
            title='Membership',
            tickvals=[],
        ),
        colorscale='Viridis'
    ),
    mode='markers',
)

data = [trace1, trace2]

layout= go.Layout(
    title= '1D IT2 Fuzzy FMF',
    hovermode= 'closest',
    xaxis= dict(
        title='y₁',
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
        range=[-6,6],
    ),
    yaxis=dict(
        title='μ(y₁)',
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= False
)


# layout = go.Layout(
#     title='1D IT2 Fuzzy FMF',
#     showlegend=False,
#     scene=dict(
#         xaxis=dict(
#             title='y₁',
#             gridcolor='rgb(255, 255, 255)',
#             zerolinecolor='rgb(255, 255, 255)',
#             showbackground=True,
#             backgroundcolor='rgb(230, 230,230)',
#             range=[-6,6],
#         ),
#         yaxis=dict(
#             title='μ(y₁)',
#             gridcolor='rgb(255, 255, 255)',
#             zerolinecolor='rgb(255, 255, 255)',
#             showbackground=True,
#             backgroundcolor='rgb(230, 230,230)',
#         ),
#         # zaxis=dict(
#         #     title='μ(y₁,y₂)',
#         #     gridcolor='rgb(255, 255, 255)',
#         #     zerolinecolor='rgb(255, 255, 255)',
#         #     showbackground=True,
#         #     backgroundcolor='rgb(230, 230,230)'
#         # )
#     )
# )

fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='Parametric_plot',auto_open=False, image='png', image_width=800, image_height=600)
