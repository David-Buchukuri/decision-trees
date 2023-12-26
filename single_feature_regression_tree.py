import json
from collections import deque

class Node:
    def __init__(self, value, isEnd = False):
        self.value = value
        self.isEnd = isEnd
        self.left = None
        self.right = None
    
    def __repr__(self):
        if self.isEnd:
            return f"end value {self.value}"
        return f"comparison value {self.value}"

class RegressionTree:
    def __init__(self, data):
        self.root = self.buildTree(data)

    def buildTree(self, data):
        if len(data) <= 8:
            effectivenessSum = 0
            for dataPoint in data:
                effectivenessSum += dataPoint['effectiveness']
            
            return Node(effectivenessSum / len(data), True)
        
        bestLeftSideData = []
        bestRightSideData = []
        lowestResidual = float('inf')
        bestDosage = 0

        for i in range(1, len(data)):
            avgDosage = (data[i]['dosage'] + data[i-1]['dosage']) / 2
            leftSideData, rightSideData, residual = self.getResidual(avgDosage, data)

            if residual < lowestResidual:
                lowestResidual = residual
                bestLeftSideData = leftSideData
                bestRightSideData = rightSideData
                bestDosage = avgDosage

        node = Node(bestDosage)

        node.left = self.buildTree(bestLeftSideData)
        node.right =  self.buildTree(bestRightSideData)

        return node

    def getResidual(self, avgDosage, data):
        leftSideData = []
        rightSideData = []

        leftSideSum = 0
        rightSideSum = 0

        for dataPoint in data:
            if dataPoint['dosage'] < avgDosage:
                leftSideData.append(dataPoint)
                leftSideSum += dataPoint['effectiveness']
            else:
                rightSideData.append(dataPoint)
                rightSideSum += dataPoint['effectiveness']

        
        leftSideAvg = leftSideSum / len(leftSideData)
        rightSideAvg = rightSideSum / len(rightSideData)


        leftResidualSum = 0
        rightResidualSum = 0

        for dataPoint in leftSideData:
            leftResidualSum += (leftSideAvg - dataPoint['effectiveness']) ** 2 

        for dataPoint in rightSideData:
            rightResidualSum += (rightSideAvg - dataPoint['effectiveness']) ** 2

        return [leftSideData, rightSideData, leftResidualSum + rightResidualSum]

    


    def predict(self, dosage, node):
        if node.isEnd:
            return node.value

        print(dosage, node.value)
        
        if dosage < node.value:
            return self.predict(dosage, node.left)
        
        return self.predict(dosage, node.right)


        
    def logTree(self, node):
        if not node:
            return
        
        queue = deque([node])

        while queue:
            if queue[0].left: queue.append(queue[0].left)
            if queue[0].right: queue.append(queue[0].right)
            
            print(
                queue.popleft()
            )



file = open('medicine-data.json')
data =  json.load(file)


RTree = RegressionTree(data)
RTree.logTree(RTree.root)

print(RTree.predict(25, RTree.root))

