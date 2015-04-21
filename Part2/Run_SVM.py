from numpy import *
from PyML.classifiers import knn
from PyML import *


data= SparseDataSet('values.csv')
s= SVM()
r=s.cv(data, numFolds=5)
print r
r.plotROC()
