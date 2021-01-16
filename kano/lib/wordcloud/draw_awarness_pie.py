import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def draw_awarness_pie(ratio, start_angle, color, index):

    dir = str(Path.cwd().parents[0])
    # data
    explode = [0.05, 0]
    ratio = [ratio]
    # append data and assign color
    ratio.append(1 - ratio[0])  # 50% blank
    colors = [color, 'k']

    # plot
    fig, ax = plt.subplots(figsize=(12, 12))
    wedges, texts = ax.pie(ratio, explode=explode, colors=colors, startangle=start_angle)
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    ax.axis('equal')
    ax.margins(0, 0)

    wedges[-1].set_visible(False)

    # autotexts[-1].set_visible(False)
    plt.tight_layout()
    plt.axis('off')

    plt.savefig("{}/{}/{}/{}/mask_test_{}.png".format(dir,'kano','source', 'img', index),
                pad_inches=0,
                bbox_inches='tight',
                facecolor='white',
                dpi=100, transparent=True)
    plt.close()
