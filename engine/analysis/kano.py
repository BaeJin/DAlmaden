import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
'''
input field : group, label, nPos, nNeg
'''
df = pd.read_csv("test_kano.csv", encoding='cp949')
df = df[df.group==2015]


def get_kanoXY(df) :
    df['log_nPos']=np.log(df.nPos)
    df['log_nNeg']=np.log(df.nNeg)

    df['rPos'] = df.nPos/sum(df.nPos)
    df['rNeg'] = df.nNeg/sum(df.nNeg)
    #df['rTot'] = (df.rPos+df.rNeg)/sum((df.rPos+df.rNeg))
    df['rTot'] = (df.nPos+df.nNeg)/sum((df.nPos+df.nNeg))
    df['rCount'] = (df.rTot-min(df.rTot))/(max(df.rTot)-min(df.rTot))
    df['adj_rCount'] = get_position(df.rCount, lower=2)
    df['radious'] = df.adj_rCount


    df['PosNeg'] = df.rPos / (df.rNeg + df.rPos)
    df['rPositiveness'] = (df.PosNeg - min(df.PosNeg)) / (max(df['PosNeg']) - min(df['PosNeg']))
    df['adj_rPositiveness'] = get_position(df.rPositiveness)

    df['theta'] = math.pi/2 * df.adj_rPositiveness

    df['xp'], df['yp'] = get_XY_POLAR(df.radious, df.theta)
    df['x'], df['y'] = trans_kano(df.radious, df.theta)
    visualize_kano(df.x,df.y,df.label)

def get_XY_POLAR(Radious, Theta) :
    return np.cos(Theta)*Radious, np.sin(Theta)*Radious

def get_position(X,lower=1.5,medmin=25,med=50,medmax=75,upper=1.5) :
    GRID_BASE = np.array([0, 0.05, 0.25, 0.5, 0.75, 0.95])
    GRID_GAP = np.append(GRID_BASE[1:], 1) - GRID_BASE
    nGRID = 6

    Xmin = np.percentile(X,0)
    X25 = np.percentile(X, 25)
    X75 = np.percentile(X, 75)
    Xmax = np.percentile(X, 100)


    Xmedmin = np.percentile(X, medmin)
    Xmed = np.percentile(X, med)
    Xmedmax = np.percentile(X, medmax)

    Xlower = np.percentile(X, lower) if lower >= 2 else X25 - lower * (X75 - X25)
    Xupper = np.percentile(X, upper) if upper >= 2 else X75 + upper * (X75 - X25)


    BASE = np.array([Xmin, Xlower, Xmedmin, Xmed, Xmedmax, Xupper])
    GAP = np.append(BASE[1:], Xmax) - BASE

    B = np.transpose(np.array([
        X<Xlower,
        np.logical_and(Xlower<=X, X<Xmedmin),
        np.logical_and(Xmedmin<=X, X<Xmed),
        np.logical_and(Xmed<=X, X<Xmedmax),
        np.logical_and(Xmedmax<=X, X<Xupper),
        Xupper<=X
    ]))

    GRID_BASEx = np.dot(np.array([GRID_BASE] * len(X)) * B, np.array([1] * nGRID))
    GRID_GAPx = np.dot(np.array([GRID_GAP] * len(X)) * B, np.array([1] * nGRID))
    BASEx = np.dot(np.array([BASE] * len(X)) * B, np.array([1] * nGRID))
    GAPx = np.dot(np.array([GAP] * len(X)) * B, np.array([1] * nGRID))
    Xx = np.dot(np.array(np.transpose(np.array([X] * nGRID))) * B, np.array([1] * nGRID))
    POSITIONx = GRID_BASEx + GRID_GAPx*(Xx - BASEx)/GAPx

    return POSITIONx


def trans_kano(arr_radious, arr_theta) :
    INNER_R = 0.25

    X = []
    Y = []
    for theta, radious in zip(arr_theta, arr_radious) :
        if radious < INNER_R:
            if theta < math.pi/4 :
                x = 0.5 * radious/INNER_R
                y = x*math.tan(theta)
            else :
                y = 0.5 * radious/INNER_R
                x = y/math.tan(theta)
        else :
            if theta < math.pi/4 :
                x = (radious-INNER_R)/(1-INNER_R)*0.5+0.5
                y = x * math.tan(theta)
            else:
                y = (radious-INNER_R)/(1-INNER_R)*0.5+0.5
                x = y / math.tan(theta)
        X.append(x)
        Y.append(y)
    return X, Y



def visualize_kano(X,Y,label,min_distX=0.05,min_distY=0.05) :
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set(xlim=(-0.1,1.1), ylim=(-0.1,1.1))
    ax.scatter(X, Y)
    ax.axhline(0.5,color='black',linewidth=.5)
    ax.axvline(0.5,color='black',linewidth=.5)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.rc('font', size=20,family='NanumGothic')  # For Windows
    ax.text(0.17,0.2, 'Indifferent', color='grey')
    ax.text(0.17,0.75, 'Attractive', color='grey')
    ax.text(0.7, 0.2, 'Must-be', color='grey')
    ax.text(0.65, 0.75, 'One-Dimensional', color='grey')


    plt.rc('font', size=15 , family='NanumGothic')  # For Windows
    X = list(X)
    Y = list(Y)

    label_position_y = []
    for x,y in zip(X,Y) :
        for x0,y0 in zip(X,Y) :
            gapx, gapy = abs(x-x0), abs(y-y0)
            if gapx < min_distX and gapy < min_distY :
                if y<y0 :
                    label_position_y.append(y-gapy)
                else :
                    label_position_y.append(y+gapy)
                break

    for lx, ly, label in zip(X, label_position_y, label):
        ax.annotate(label, (lx, ly))


