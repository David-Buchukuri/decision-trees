import json
from random import randint
from random_regression_tree import RandomRegressionTree


class RandomForest:
    def __init__(self, data, columns, columnToPredict, numOfTrees = 10):
        self.forest = []
        self.data = data
        self.columns = columns
        self.columnToPredict = columnToPredict
        self.numOfTrees = numOfTrees
        self.buildForest()
    
    def buildForest(self):
        for _ in range(self.numOfTrees):
            data = self.generateBootstrappedData(self.data)
            RRTree = RandomRegressionTree(data, self.columns, self.columnToPredict)
            self.forest.append(RRTree)
    
    def predict(self, features):
        sum = 0
        
        for tree in self.forest:
            sum += tree.predict(features)
        
        return round(sum / len(self.forest), 2)

    def generateBootstrappedData(self, data):
        bootstrappedData = []

        for _ in range(len(data)):
            randIdx = randint(0, len(data) - 1)
            bootstrappedData.append(
                data[randIdx]
            )
        
        return bootstrappedData


file = open('./houses-data-training.json')
data = json.load(file)
file.close()

forest = RandomForest(data, ['rooms', 'space', 'floor', 'total_floors'], 'price', 25)
result = forest.predict({'rooms': 3, 'space': 90, 'floor': 4, 'total_floors': 10})
print(result)



# accuracy on testing data with MAPE

file = open('./houses-data-testing.json')
testingData = json.load(file)
file.close()

errorPercentageSum = 0

for dataPoint in testingData:
    prediction = forest.predict(
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






