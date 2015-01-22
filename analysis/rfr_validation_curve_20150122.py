import matplotlib.pyplot as plt
import numpy as np
from numpy import random

##Put the series you want to plot in the double array data. Put the series labels in the labels array
##Right now, all y_data series must use the same x_series


x_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 300, 500, 1000]
y_data = [[0.93, 0.94, 0.94, 0.94, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95], 
		  [0.53, 0.56, 0.59, 0.58, 0.58, 0.59, 0.58, 0.58, 0.59, 0.59, 0.59, 0.59, 0.59]]
labels = ['Training', 'Testing']
color = ['#0015ff', '#353c85', '#33FF00', '#439130', '#FF0000', '#9C2F2F', '#EA00FF', '#85348C']
for i in np.arange(0,len(y_data)):
	plt.plot(x_data, y_data[i], color[i], label=labels[i], linewidth=3)

plt.title('Random Forest Classifier Validation Curve')
plt.xlabel('Number of Trees')
plt.ylabel('R2 Score')
plt.ylim([0.4, 1.1])
plt.legend(loc='best')
plt.show()