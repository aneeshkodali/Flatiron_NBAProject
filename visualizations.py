import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def visualizeTTest(hA, n, alpha=0.05):
    '''
    Args:
        - hA = alternative hypothesis: '>', '<', '<>'
        - n = degrees of freedom
    Returns plot
    '''

    dof = n-1
    # generate points on the x axis:
    bound = 4
    xs = np.linspace(-bound, bound, dof)

    # use stats.t.pdf to get values on the probability density function for the t-distribution
    # the second argument is the degrees of freedom
    ys = stats.t.pdf(xs, dof, 0, 1)

    # initialize a matplotlib "figure"
    fig = plt.figure(figsize=(8,5))

    # get the current "axis" out of the figure
    ax = fig.gca()

    # Designate colors
    colorCurve='blue'
    colorRejectionRegion='red'
    colorVLine='black'

    # Designate line width
    lineWidth=3

    # plot the lines using matplotlib's plot function:
    ax.plot(xs, ys, linewidth=lineWidth, color=colorCurve)

    if hA=='>':
        area = 1 - alpha
        # Calculate t-statistic
        tCrit = stats.t.ppf(area, dof)
        # Create vertical line for t-statistic
        ax.axvline(tCrit, color=colorVLine, linestyle='--', lw=lineWidth, label=f"T-Crit: {round(tCrit, 2)}")
        # Fill area between t-statistic and curve
        plt.fill_between(xs, ys, where=xs>tCrit, color=colorRejectionRegion)

    elif hA=='<':
        area = 1 - alpha
        # Calculate t-statistic
        tCrit = stats.t.ppf(area, dof)*-1
        # Create vertical line between t-statistic and curve
        ax.axvline(tCrit, color=colorVLine, linestyle='--', lw=lineWidth, label=f"T-Crit: {round(tCrit, 2)}")
        # Fill area between t-statistic and curve
        plt.fill_between(xs, ys, where=xs<tCrit, color=colorRejectionRegion)
    
    else:
        area = 1 - alpha/2
        # Calculate t-statistic
        tCrit = stats.t.ppf(area, dof)
        # Create vertical lines between t-statistic and curve
        ax.axvline(tCrit, color=colorVLine, linestyle='--', lw=lineWidth,label=f"T-Crit: {round(tCrit, 2)}")
        ax.axvline(-tCrit, color=colorVLine, linestyle='--', lw=lineWidth)
        # Fill area between t-statistic and curve
        plt.fill_between(xs, ys, where=xs>tCrit, color=colorRejectionRegion)
        plt.fill_between(xs, ys, where=xs<-tCrit, color=colorRejectionRegion)
    
    ax.legend()

    tailedString = "One-Tailed" if hA in ["<",">"] else "Two-Tailed"
    titleString = f"{tailedString} Critical Region for Significance Level of {alpha} and Degrees of Freedom of {dof}"
    plt.title(titleString)
    plt.show()


def visualizeFTest(numGroups, numObs, alpha=0.05):
    ''' Given number of groups and number of observations,
    Returns plot
    '''

    # Generate curve
    fVar = stats.f(dfn=numGroups-1, dfd=numObs-numGroups, loc=0, scale=1)
    x = np.linspace(fVar.ppf(0.0001), fVar.ppf(0.9999), 100)
    y = fVar.pdf(x) 

    # Find critical value
    fCrit = stats.f.ppf(q=1-alpha, dfn=numGroups-1, dfd=numObs-numGroups)

    # initialize a matplotlib "figure"
    fig = plt.figure(figsize=(8,5))

    # get the current "axis" out of the figure
    ax = fig.gca()

    # Designate colors
    colorCurve='blue'
    colorRejectionRegion='red'
    colorVLine='black'

    # Designate line width
    lineWidth=3

    # plot the lines using matplotlib's plot function
    ax.plot(x, y, linewidth=lineWidth, color=colorCurve)

    # Create vertical lines between t-statistic and curve
    ax.axvline(fCrit, color=colorVLine, linestyle='--', lw=lineWidth,label=f"F-Crit: {round(fCrit, 2)}")
    # Fill area between t-statistic and curve
    plt.fill_between(x, y, where=x>fCrit, color=colorRejectionRegion)
    plt.legend()
    plt.show()

    # plt.xlim(0,5)
    # plt.plot(x,y, 'b')
    # plt.show()