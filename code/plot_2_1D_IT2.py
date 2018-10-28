from plotly import tools
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np

# r = np.linspace(0, 10, 100)
# t = np.linspace(0, 2 * np.pi, 240)

x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)

xGrid, yGrid = np.meshgrid(x,y)

z1 = np.maximum(np.minimum(1 - abs(xGrid)/5, 1 - abs(yGrid)/5), xGrid*0)
z2 = np.maximum(np.minimum(1 - abs(xGrid)/3, 1 - abs(yGrid)/3), xGrid*0)

# rGrid, tGrid = np.meshgrid(r, t)
#
# x = rGrid * np.cos(tGrid)
# y = rGrid * np.sin(tGrid)
# z1 = np.maximum(1 - rGrid/5, rGrid * 0)
# z2 = np.maximum(1 - rGrid/3, rGrid * 0)

surface1 = go.Surface(x=x, y=y, z=z1, opacity=0.7,colorscale='Viridis',colorbar=dict(showticklabels=False))
surface2 = go.Surface(x=x, y=y, z=z2, opacity=1, colorscale='Viridis',colorbar=dict(nticks=5))
data = [surface1, surface2]

layout = go.Layout(
    title='2 1D IT2 Fuzzy FMF',
    scene=dict(
        xaxis=dict(
            title='y₁',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)',
            range=[-5,5],
        ),
        yaxis=dict(
            title='y₂',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)',
            range=[-5,5],
        ),
        zaxis=dict(
            title='μ(y₁,y₂)',
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='Parametric_plot',auto_open=False, image='png', image_width=800, image_height=600)
