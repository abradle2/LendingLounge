import matplotlib.pyplot as plt
import numpy as np
from numpy import random

##Put the series you want to plot in the double array data. Put the series labels in the labels array
##Right now, all y_data series must use the same x_series


x_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 500]
y_data = [[0.86, 0.89, 0.89, 0.91, 0.91, 0.90, 0.92, 0.92, 0.93, 0.92, 0.93, 0.93], 
		  [0.12, 0.13, 0.14, 0.14, 0.13, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.15], 
		  [0.14, 0.11, 0.11, 0.09, 0.09, 0.10, 0.08, 0.08, 0.07, 0.08, 0.07, 0.07], 
		  [0.88, 0.87, 0.86, 0.86, 0.87, 0.86, 0.86, 0.86, 0.86, 0.86, 0.86, 0.85]]
labels = ['Pred paid actually paid', 'Pred paid actually default', 'Pred default actually paid', 'Pred default actually default']
color = ['#0015ff', '#353c85', '#33FF00', '#439130', '#FF0000', '#9C2F2F', '#EA00FF', '#85348C']
for i in np.arange(0,len(y_data)):
	plt.semilogx(x_data, y_data[i], color[i], label=labels[i], linewidth=3)

plt.title('Random Forest Classifier Validation')
plt.xlabel('Number of Trees')
plt.ylabel('Rate')
plt.ylim([0, 1.1])
plt.legend(loc='best')
plt.show()