import matplotlib.pyplot as plt
import numpy as np
from numpy import random

##Put the series you want to plot in the double array data. Put the series labels in the labels array
##Right now, all y_data series must use the same x_series


x_data = [1E-2, 1E-1, 1, 1E1, 1E2, 1E3, 1E4]
y_data = [[-0.42, -0.41, -0.42, -0.42, -0.42, -0.42, -0.42], [-0.44, -0.43, -0.44, -0.44, -0.44, -0.44, -0.44],
		  [-0.41, -0.37, -0.41, -0.42, -0.42, -0.42, -0.42], [-0.43, -0.39, -0.43, -0.44, -0.44, -0.44, -0.44],
		  [-0.27, -0.20, -0.40, -0.41, -0.41, -0.41, -0.41], [-0.29, -0.19, -0.42, -0.44, -0.44, -0.44, -0.44],
		  [0.34, 0.52, -0.02, -0.39, -0.39, -0.39, -0.39], [0.33, 0.51, -0.10, -0.45, -0.46, -0.46, -0.46],
		  [0.53, 0.56, 0.58, 0.03, -0.02, -0.02, -0.00], [0.52, 0.53, 0.34, -0.38, -0.41, -0.41, -0.41]]
labels = ['C=0.01 Train', 'C=0.01 Test', 'C=0.1 Train', 'C=0.1 Test', 'C=1 Test', 'C=1 Test', 'C=10 Train', 'C=10 Test', 'C=100 Train', 'C=100 Test']
color = ['#0015ff', '#353c85', '#33FF00', '#439130', '#FF0000', '#9C2F2F', '#EA00FF', '#85348C', '#DB6D1F', '#70482C']

for i in np.arange(0,len(y_data)):
	plt.semilogx(x_data, y_data[i], color[i], label=labels[i], linewidth=3)

plt.title('SVR')
plt.xlabel('gamma')
plt.ylabel('R2 Score')
plt.ylim([-0.5, 1])
plt.legend(loc='best')
plt.show()