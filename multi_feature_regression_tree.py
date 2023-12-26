from collections import deque
import json

class Node:
    def __init__(self, value, column = None, isEnd = False):
        self.value = value
        self.isEnd = isEnd
        self.column = column
        self.left = None
        self.right = None
    
    def __repr__(self):
        if self.isEnd:
            return f"leaf {self.value}"
        return f"{self.column}: {self.value}"

class RegressionTree:
    def __init__(self, data, columns, columnToPredict):
        self.columns = columns
        self.columnToPredict = columnToPredict
        self.root = self.buildTree(data)

    def buildTree(self, data):       
        if len(data) <= 8:
            predictionSum = 0
            for dataPoint in data:
                predictionSum += dataPoint[self.columnToPredict]
            
            return Node(predictionSum / len(data), isEnd=True)
        
        bestLeftSideData = []
        bestRightSideData = []
        lowestResidual = float('inf')
        bestSplittingColumnName = None
        bestSplittingValue = 0

        for column in self.getColumns():
            
            data.sort(key=lambda x: x[column])

            for i in range(1, len(data)):
                avgSplitPoint = (data[i][column] + data[i-1][column]) / 2

                leftSideData, rightSideData, residual = self.getResidual(
                    data, 
                    (i + i - 1) / 2
                )

                if residual < lowestResidual:
                    lowestResidual = residual
                    bestLeftSideData = leftSideData
                    bestRightSideData = rightSideData
                    bestSplittingValue = avgSplitPoint
                    bestSplittingColumnName = column

        node = Node(bestSplittingValue, bestSplittingColumnName)

        node.left = self.buildTree(bestLeftSideData)
        node.right = self.buildTree(bestRightSideData)

        return node

    def getResidual(self, data, splitPointIdx):
        leftSideData = []
        rightSideData = []

        leftSideSum = 0
        rightSideSum = 0

        for idx, dataPoint in enumerate(data):
            if idx < splitPointIdx:
                leftSideData.append(dataPoint)
                leftSideSum += dataPoint[self.columnToPredict]
            else:
                rightSideData.append(dataPoint)
                rightSideSum += dataPoint[self.columnToPredict]

        leftSideAvg = leftSideSum / len(leftSideData)
        rightSideAvg = rightSideSum / len(rightSideData)


        leftResidualSum = 0
        rightResidualSum = 0

        for dataPoint in leftSideData:
            leftResidualSum += (leftSideAvg - dataPoint[self.columnToPredict]) ** 2 

        for dataPoint in rightSideData:
            rightResidualSum += (rightSideAvg - dataPoint[self.columnToPredict]) ** 2

        return [leftSideData, rightSideData, leftResidualSum + rightResidualSum]

    def getColumns(self):
        return self.columns

    def predict(self, features, node=None):
        if not node: node = self.root

        if node.isEnd:
            return node.value
        
        if features[node.column] < node.value:
            return self.predict(features, node.left)
        
        return self.predict(features, node.right)
        
    def logTree(self, node):
        if not node:
            return
        
        queue = deque([node])

        while queue:
            if queue[0].left: queue.append(queue[0].left)
            if queue[0].right: queue.append(queue[0].right)
            
            print(queue.popleft())


if __name__ == "__main__":
    # file = open('medicine-data.json')
    # data = json.load(file)

    # RTree = RegressionTree(data, ['dosage', 'weight'], 'effectiveness')
    # print(RTree.predict({'dosage': 29, 'weight': 50}))


    file = open('./houses-data-training.json')
    data = json.load(file)
    file.close()

    RTree = RegressionTree(data, ['rooms', 'space', 'floor', 'total_floors'], 'price')


    # accuracy on testing data with MAPE

    file = open('./houses-data-training.json')
    testingData = json.load(file)
    file.close()

    errorPercentageSum = 0

    for dataPoint in testingData:
        prediction = RTree.predict(
            {
                'rooms': dataPoint['rooms'], 
                'space': dataPoint['space'], 
                'floor': dataPoint['floor'], 
                'total_floors': dataPoint['total_floors']
            }
        )

        actual = dataPoint['price']
        diff = abs(actual - prediction)

        errorPercentageSum += (diff / actual) * 100

    print(f"mean absolute percentage error: {errorPercentageSum / len(testingData)}")


