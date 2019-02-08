import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import itertools

def facetErrorBars(x, y, sigma, cDict, color=None, label=None, **kwargs):
    # Add error bars to a FacetGrid / FactorPlot and match the bar color to the hue
    data = kwargs.pop("data")
    hue = kwargs.pop("hue")

    ebColors = []
    for eval in data[hue].unique():
        ebColor = cDict[eval]
        xVals = data[x].loc[data[hue] == eval].values
        yVals = data[y].loc[data[hue] == eval].values
        yErrs = data[sigma].loc[data[hue] == eval].values    
        plt.fill_between(xVals, yVals-yErrs, yVals+yErrs, interpolate=True,alpha=0.2,color=ebColor)

dfLAR = pd.read_csv('./LAR_cancer.csv')

dfLAR['Sigma'] = np.sqrt(np.power(dfLAR['Incidence'],2)*dfLAR['Var(log) Incidence'])

dfLAR_most = dfLAR[(dfLAR['Type'] != 'All cancers') \
				& (dfLAR['Type'] != 'All solid') \
				& (dfLAR['Type'] != 'Prostate') \
				& (dfLAR['Type'] != 'Uterus') \
				& (dfLAR['Type'] != 'Ovary') \
 ]
ax = sns.relplot(x="Age",y="Incidence", hue="Sex", col='Type',data=dfLAR_most,col_wrap=3)


# Superimpose error bars
palette = itertools.cycle(sns.color_palette())

ebDict = { }    
for gender in dfLAR['Sex'].unique():
    ebDict[gender] = next(palette)

ax.map_dataframe(facetErrorBars,"Age","Incidence","Sigma",ebDict,data=dfLAR_most, hue='Sex',
       markeredgecolor='k',ls='',elinewidth=1.5,capsize=6,zorder=0)
       
       
ax.set(xlabel="Age of exposure", ylabel="Lifetime risk (LAR) for 0.1 Gy exposure, per 100,000 exposed")


plt.tight_layout()
plt.savefig('Cancer_morbitity.pdf')


