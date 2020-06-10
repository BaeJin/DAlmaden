import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
'''
input field : group, label, nPos, nNeg
'''

def merge_df_kano(df_kano1, df_kano2) :
    pass

def visualize_df_kano(df_kano, x_colname='x', y_colname='y', label_colname='label') :
    visualize_kano(df_kano[x_colname],df_kano[y_colname],df_kano[label_colname])

def get_kanoXY(df_bowpn, nPosColumnName = 'nPos', nNegColumnName = 'nNeg') :
    df = df_bowpn.copy()
    df['log_nPos']=np.log(df[nPosColumnName])
    df['log_nNeg']=np.log(df[nNegColumnName])

    df['rPos'] = df[nPosColumnName]/sum(df[nPosColumnName])
    df['rNeg'] = df[nNegColumnName]/sum(df[nNegColumnName])
    #df['rTot'] = (df.rPos+df.rNeg)/sum((df.rPos+df.rNeg))
    df['rTot'] = (df[nPosColumnName]+df[nNegColumnName])/sum((df[nPosColumnName]+df[nNegColumnName]))
    df['rCount'] = (df.rTot-min(df.rTot))/(max(df.rTot)-min(df.rTot))
    df['adj_rCount'] = get_position(df.rCount, lower=2)
    df['radious'] = df.adj_rCount


    df['PosNeg'] = df.rPos / (df.rNeg + df.rPos)
    df['rPositiveness'] = (df.PosNeg - min(df.PosNeg)) / (max(df['PosNeg']) - min(df['PosNeg']))
    df['adj_rPositiveness'] = get_position(df.rPositiveness)

    df['theta'] = math.pi/2 * df.adj_rPositiveness

    df['xp'], df['yp'] = get_XY_POLAR(df.radious, df.theta)
    df['x'], df['y'] = trans_kano(df.radious, df.theta)
    return df

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


def get_text_positions(text, x_data, y_data, txt_width, txt_height):
    a = zip(y_data, x_data)
    text_positions = list(y_data)
    for index, (y, x) in enumerate(a):
        local_text_positions = [i for i in a if i[0] > (y - txt_height)
                            and (abs(i[1] - x) < txt_width * 2) and i != (y,x)]
        if local_text_positions:
            sorted_ltp = sorted(local_text_positions)
            if abs(sorted_ltp[0][0] - y) < txt_height: #True == collision
                differ = np.diff(sorted_ltp, axis=0)
                a[index] = (sorted_ltp[-1][0] + txt_height, a[index][1])
                text_positions[index] = sorted_ltp[-1][0] + txt_height*1.01
                for k, (j, m) in enumerate(differ):
                    #j is the vertical distance between words
                    if j > txt_height * 2: #if True then room to fit a word in
                        a[index] = (sorted_ltp[k][0] + txt_height, a[index][1])
                        text_positions[index] = sorted_ltp[k][0] + txt_height
                        break
    return text_positions

def text_plotter(text, x_data, y_data, text_positions, txt_width,txt_height):
    for z,x,y,t in zip(text, x_data, y_data, text_positions):
        plt.annotate(str(z), xy=(x-txt_width/2, t), size=12)
        if y != t:
            plt.arrow(x, t,0,y-t, color='red',alpha=0.3, width=txt_width*0.1,
                head_width=txt_width, head_length=txt_height*0.5,
                zorder=0,length_includes_head=True)
