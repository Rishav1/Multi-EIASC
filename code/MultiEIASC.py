import numpy as np
from plotly import tools
import plotly.offline as offline
import plotly.graph_objs as go
import pandas as pd


LOWX = -5
HIGHX = 5
LOWY = -5
HIGHY = 5
FINE = 100
T_FINE = 360
UMFfactor = 1
LMFfactor = 0.6

X = np.linspace(LOWX, HIGHX, FINE)
Y = np.linspace(LOWY, HIGHY, FINE)


Xgrid, Ygrid = np.meshgrid(X,Y)


def plot_boundary(Xgrid, Ygrid, UMFgrid, LMFgrid):

    CENTROID_BOUND_x, CENTROID_BOUND_y = EIASC2D(Xgrid, Ygrid, UMFgrid, LMFgrid)

    UMFsurf = go.Surface(x=Xgrid, y=Ygrid, z=UMFgrid, opacity=0.5,colorscale='Viridis',colorbar=dict(showticklabels=False))
    LMFsurf = go.Surface(x=Xgrid, y=Ygrid, z=LMFgrid, opacity=0.8, colorscale='Viridis')
    CENTbound = go.Scatter3d(x=CENTROID_BOUND_x, y=CENTROID_BOUND_y, z=np.array([0] * CENTROID_BOUND_x.size), showlegend=False, mode='markers', marker=dict(size=2, color='red', line=dict(color='red', width=0.5)))

    data = [UMFsurf, LMFsurf, CENTbound]

    print(CENTROID_BOUND_x, CENTROID_BOUND_y)

    layout = go.Layout(
        title='EIASC on 2D IT2 Fuzzy FMF',
        scene=dict(
            xaxis=dict(
                title='y₁',
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)',
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
                backgroundcolor='rgb(230, 230,230)',
            )
        )
    )

    fig = go.Figure(data=data, layout=layout)
    offline.plot(fig, filename='EIASC_fast',auto_open=False, image='png', image_width=800, image_height=600)
    return

def gaussian(factor):
    return factor * np.exp(- (np.square(Xgrid) + np.square(Ygrid)) / 15 )

def volcano(factor):
    global X
    global Y
    global Xgrid
    global Ygrid

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv')
    df = df / df.max()
    X = np.linspace(LOWX, HIGHX, df.shape[1])
    Y = np.linspace(LOWY, HIGHY, df.shape[0])

    Xgrid, Ygrid = np.meshgrid(X,Y)

    return df.values * factor



def EIASC2D(Xgrid, Ygrid, UMFgrid, LMFgrid):
    Xgrid = Xgrid.flatten()
    Ygrid = Ygrid.flatten()

    UMFgrid = UMFgrid.flatten()
    LMFgrid = LMFgrid.flatten()


    THETA = np.linspace(0, 2 * np.pi, T_FINE)
    CENTROID_BOUND_x = np.array([])
    CENTROID_BOUND_y = np.array([])

    CEN_idx = 0

    for theta in THETA:
        # Xlin = Xgrid * np.cos(theta) + Ygrid * np.sin(theta)
        Ylin = - Xgrid * np.sin(theta) + Ygrid * np.cos(theta)

        # CEN, CEN_idx = EIASC(Ylin, UMFgrid, LMFgrid, CEN_idx)
        CEN, CEN_idx = EIASC_fast(Ylin, UMFgrid, LMFgrid, CEN_idx)

        DENO = np.sum(np.append((- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) > CEN) * UMFgrid,
        (- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) <= CEN) * LMFgrid))
        CEN_T_x = np.sum(np.append((- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) > CEN) * Xgrid * UMFgrid,
        (- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) <= CEN) * Xgrid * LMFgrid))
        CEN_T_y = np.sum(np.append((- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) > CEN) * Ygrid * UMFgrid,
        (- Xgrid * np.sin(theta) + Ygrid * np.cos(theta) <= CEN) * Ygrid * LMFgrid))


        CENTROID_BOUND_x = np.append(CENTROID_BOUND_x, CEN_T_x/DENO)
        CENTROID_BOUND_y = np.append(CENTROID_BOUND_y, CEN_T_y/DENO)

    return CENTROID_BOUND_x, CENTROID_BOUND_y

def EIASC(Ylin, UMFgrid, LMFgrid, CEN_idx):
    YsortInd = np.argsort(Ylin)
    Ysort = Ylin[YsortInd]
    UMFsort = UMFgrid[YsortInd]
    LMFsort = LMFgrid[YsortInd]

    for i in range(len(Ysort)):
        FULC = np.sum(np.append(Ysort[:i] * LMFsort[:i], Ysort[i:] * UMFsort[i:]))
        DENO = np.sum(np.append(LMFsort[:i], UMFsort[i:]))

        if FULC/DENO < Ysort[i]:
            return Ysort[i], i

def EIASC_fast(Ylin, UMFgrid, LMFgrid, CEN_idx):
    YsortInd = np.argsort(Ylin)
    Ysort = Ylin[YsortInd]
    UMFsort = UMFgrid[YsortInd]
    LMFsort = LMFgrid[YsortInd]

    FULC = np.sum(np.append(Ysort[:CEN_idx] * LMFsort[:CEN_idx], Ysort[CEN_idx:] * UMFsort[CEN_idx:]))
    DENO = np.sum(np.append(LMFsort[:CEN_idx], UMFsort[CEN_idx:]))

    if FULC/DENO > Ysort[CEN_idx]:
        while FULC/DENO > Ysort[CEN_idx]:
            CEN_idx = CEN_idx + 1
            
            FULC = np.sum(np.append(Ysort[:CEN_idx] * LMFsort[:CEN_idx], Ysort[CEN_idx:] * UMFsort[CEN_idx:]))
            DENO = np.sum(np.append(LMFsort[:CEN_idx], UMFsort[CEN_idx:]))

        return Ysort[CEN_idx], CEN_idx

    else:
        while FULC/DENO < Ysort[CEN_idx]:
            CEN_idx = CEN_idx - 1
            
            FULC = np.sum(np.append(Ysort[:CEN_idx] * LMFsort[:CEN_idx], Ysort[CEN_idx:] * UMFsort[CEN_idx:]))
            DENO = np.sum(np.append(LMFsort[:CEN_idx], UMFsort[CEN_idx:]))

        return Ysort[CEN_idx + 1], CEN_idx + 1

# UMFgrid = gaussian(UMFfactor)
# LMFgrid = gaussian(LMFfactor)

UMFgrid = volcano(UMFfactor) * gaussian(UMFfactor)
LMFgrid = volcano(LMFfactor) * gaussian(LMFfactor)


plot_boundary(Xgrid, Ygrid, UMFgrid, LMFgrid)
