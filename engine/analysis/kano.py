import pandas as pd
import numpy as np
import math
from adjustText import adjust_text
import matplotlib.pyplot as plt
from tqdm import tqdm, trange
'''
input field : group, label, nPos, nNeg
'''

def visualize_df_kano_dual(df_kano1, df_kano2, savepath) :
    pass

def visualize_df_kano(df_kano, savepath, x_colname='x', y_colname='y', label_colname='label') :
    visualize_kano(df_kano[x_colname],df_kano[y_colname],df_kano[label_colname],savepath)

def get_df_kanobow(df_textSent, df_labelKwd,
                   textColname = 'text', sentimentColname = 'sentiment', labelColname = 'label',keywordColname='keyword') :
    labels = set(df_labelKwd[labelColname])
    nPos = []
    nNeg = []
    for label in labels :
        keywords = df_labelKwd[keywordColname][df_labelKwd[labelColname]==label]
        sentiments = df_textSent[sentimentColname][map(_keywords_in_str_, df_textSent[textColname], keywords)]
        nPos.append(sum([s >= 0.5 for s in sentiments]))
        nNeg.append(sum([s < 0.5 for s in sentiments]))
    df_kanobow = pd.DataFrame(label = labels, nPos = nPos, nNeg=nNeg)
    return df_kanobow

def _keywords_in_str_(string, kwd_list) :
    for kwd in kwd_list :
        if kwd in string :
            return True
    return False

def get_df_kano(df_kanobow, nPosColumnName ='nPos', nNegColumnName ='nNeg') :
    df = df_kanobow.copy()
    df['log_nPos']=np.log(df[nPosColumnName])
    df['log_nNeg']=np.log(df[nNegColumnName])

    df['rPos'] = df[nPosColumnName]/sum(df[nPosColumnName])
    df['rNeg'] = df[nNegColumnName]/sum(df[nNegColumnName])
    #df['rTot'] = (df.rPos+df.rNeg)/sum((df.rPos+df.rNeg))
    df['rTot'] = (df[nPosColumnName]+df[nNegColumnName])/sum((df[nPosColumnName]+df[nNegColumnName]))
    df['rCount'] = (df.rTot-min(df.rTot))/(max(df.rTot)-min(df.rTot))
    df['adj_rCount'] = get_position(df.rCount)
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

def get_position(X,medmin=25,med=50,medmax=75) :
    '''
    get relative position
    :param X:
    :param lower:
    :param medmin:
    :param med:
    :param medmax:
    :param upper:
    :return:
    '''
    GRID_BASE = np.array([0, 0.05, 0.25, 0.5, 0.75, 0.95])
    GRID_GAP = np.append(GRID_BASE[1:], 1) - GRID_BASE
    nGRID = 6

    X25 = np.percentile(X, 25)
    X75 = np.percentile(X, 75)
    Xmin = min(np.percentile(X, 0), X25 - 1.5 * (X75 - X25))
    Xmax = max(np.percentile(X, 100), X75 + 1.5 * (X75 - X25))


    Xmedmin = np.percentile(X, medmin)
    Xmed = np.percentile(X, med)
    Xmedmax = np.percentile(X, medmax)

    Xlower = max(np.percentile(X, 0), X25 - 1.5 * (X75 - X25))
    Xupper = min(np.percentile(X, 100), X75 + 1.5 * (X75 - X25))


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
    '''
    round shape to square shape
    :param arr_radious: r
    :param arr_theta: t
    :return: X,Y position
    '''
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

def visualize_kano(X,Y,label,savepath) :
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

    texts = [plt.text(x, y, s) for x,y,s in zip(X,Y,label)]
    adjust_text(texts)
    plt.savefig(savepath)