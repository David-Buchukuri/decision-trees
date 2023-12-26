from math import ceil
from multi_feature_regression_tree import RegressionTree
from random import randint

class RandomRegressionTree(RegressionTree):
    def __init__(self, data, columns, columnToPredict):
        super().__init__(data, columns, columnToPredict)

    def getColumns(self):
        allColumns = self.columns
        numOfColsToTake = ceil(len(allColumns) / 2) 
        randomColumns = set([])

        while len(randomColumns) < numOfColsToTake:
            randIdx = randint(0, len(allColumns) - 1)
            randomColumns.add(
                allColumns[randIdx]
            )
        
        return list(randomColumns)