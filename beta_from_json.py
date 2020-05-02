import sys 
import getopt

import json
import time

from matplotlib import pyplot
from numpy import cov
from scipy.stats import pearsonr
import numpy as np

def main():
    symbol = 'IBM'
    index = 'SPY'
    data_as_json_string = ''
    with open("{0:}_{1:}.json".format(symbol, index),"r") as jsonfile:
        data_as_json_string = jsonfile.read()
    cleaned_data = json.loads(data_as_json_string)
    num_datapoints=len(cleaned_data)
    data1 = np.zeros(num_datapoints)
    data2 = np.zeros(num_datapoints)
    j = 0
    for i in cleaned_data:
        x = cleaned_data[i][index]
        y = cleaned_data[i][symbol]
    #    print(x,y)
        data1[j]=x
        data2[j]=y
        j += 1
        
    # print(data1, data2)
    pyplot.scatter(data1, data2)
    pyplot.show()
    
    covariance = cov(data1, data2)
    print("covariance is {0:}".format(covariance))
    rvalues = pearsonr(data1, data2)
    print("beta estimate is {0:}".format(rvalues[0]))
        
main()
