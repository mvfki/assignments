# -*- coding: utf-8 -*-
"""
@author: Yichen Wang
@date: 06/30/2020
"""
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np

def generateCmap(breakPointColors, breakPoints=None, sensitivity=256, 
               name="userCmap"):
    '''
    Aimed at generate user customized ListedColormap instance, to be used when 
    plotting with matplotlib.
    Arguments:
    ----------
    breakPointColors: 
        An array of color difinitions. Can be "rgba" vector or a string (like 
        "red") that `matplotlib.colors.to_rgba()` accepts.
    breakPoints: 
        Optional. An array of numbers that defines the border of color 
        gradients. The values does not necessarily match the border of the 
        data to plot, but will be reflected as ratio on the plot. Must be of 
        the same length as `breakPointColors`.
    sensitivity: 
        An integer for how many intrinsic intervals in the colormap. Default 
        `256`. Should use larger value if there are breakpoints close to each 
        other.
    Return:
    ----------
        a matplotlib.colors.ListedColormap object, that can be used for "cmap"
    argument in matplotlib plotting function.
    Example:
    ----------
    >>> import matplotlib.pyplot as plt
    >>> cmap = generateCmap(['blue', 'white', 'red'])
    >>> plt.scatter(range(100), range(100), c=range(100), cmap=cmap)
    '''
    # Input Check
    assert len(breakPointColors) >= 2
    if breakPoints != None:
        assert len(breakPoints) == len(breakPointColors)
        assert len(set(breakPoints)) == len(breakPoints), \
               "Should not give duplicated value in 'breakPoints'"
    else:
        breakPoints = list(range(len(breakPointColors)))
    
    breakPointColors = np.array(breakPointColors)
    assert len(breakPointColors.shape) == 1 or \
           len(breakPointColors.shape) == 2
    if len(breakPointColors.shape) == 1:
        assert str(breakPointColors.dtype).startswith('<U'), \
               "Color specification dtype not understandable"
    elif len(breakPointColors.shape) == 2:
        assert breakPointColors.shape[1] in [3, 4] and \
               breakPointColors.dtype in ['int32', 'float64'], \
               "'rgb(a)' color specification not understandable."

    ## Randomly fetch an ListedColormap object, and modify the colors inside
    cmap = cm.get_cmap("viridis", sensitivity)
    cmap.name = name
    
    # Format the input
    minBP, maxBP = min(breakPoints), max(breakPoints)
    scaledBP = [round((i-minBP)/(maxBP-minBP)*(sensitivity-1)) \
                for i in breakPoints]
    assert len(set(scaledBP)) == len(breakPoints), \
           "Sensitivity too low"
    sortedBP = sorted(scaledBP)
    sortedBPC = []
    for i in sortedBP:
        idx = scaledBP.index(i)
        sortedBPC.append(breakPointColors[idx])
    BPC_rgba = np.array([colors.to_rgba(i) for i in sortedBPC])
    # Now replace colors in the Colormap object
    for i in range(1, len(sortedBP)):
        ## Indices when slicing colormap.colors
        start = sortedBP[i-1]
        end = sortedBP[i] + 1
        n = end - start
        ## Color range
        startC = BPC_rgba[i-1]
        endC = BPC_rgba[i]
        for i in range(3):
            cmap.colors[start:end, i] = np.linspace(startC[i], endC[i], n)
        
    return cmap

if __name__ == '__main__':
    x = list(range(100))
    y = list(range(100))
    c = list(range(100))
    # Example usage
    ## Define two types of cmap
    cmap1 = generateCmap(['blue', 'white', 'red'])
    cmap2 = generateCmap(['blue', 'red', 'yellow', 'green'], [0, 1, 2, 6])
    ## Plot
    cms = [cmap1, cmap2]
    fig, axs = plt.subplots(1, 2, figsize=(6, 3), constrained_layout=True)
    for [ax, cmap] in zip(axs, cms):
        ax.scatter(x, y, c=x, cmap=cmap)
    plt.show()
