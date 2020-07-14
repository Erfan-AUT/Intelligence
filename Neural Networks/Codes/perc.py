import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt, matplotlib

mu, sigma = 0.0, 1.0

def preparation():
    from sklearn.model_selection import train_test_split
    df = pd.read_csv("data.csv")
    colors = ['red','green']
    df.plot(kind='scatter',x='X1',y='X2', c=df['Label'], cmap=matplotlib.colors.ListedColormap(colors))
    plt.savefig("scatter.png")
    train, test = train_test_split(df, test_size=0.2)
    train.to_csv("train.csv")
    test.to_csv("test.csv")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Perceptron:
    def __init__(self, n_epoch=6000, learning_rate=0.15, dataset_address=None):
        self.n_epoch = n_epoch
        self.learning_rate = learning_rate
        df = pd.read_csv(dataset_address)
        self.X = np.asarray(pd.concat([df['X1'], df['X2']], axis=1, keys=['X1', 'X2']))
        self.y = pd.concat([df['Label']], axis=1, keys=['Label']).values.flatten()
        self.rows = self.X.shape[0]
        self.columns = self.X.shape[1]
        self.W = np.random.normal(mu, sigma, size=self.columns)
        self.b = np.random.normal(mu, sigma, size=1)


    def calc_y_hat(self, X):
        y_hat = np.dot(self.W, X.T) + self.b
        return sigmoid(y_hat)

    def train_network(self):
        for _ in range(self.n_epoch):
            calc_matrix = self.calc_y_hat(self.X)
            diff = np.subtract(calc_matrix, self.y)
            w_gradient = np.matmul(self.X.T, diff)
            b_gradient = diff.sum()
            self.W -= self.learning_rate * w_gradient / self.rows
            self.b -= self.learning_rate * b_gradient / self.rows


    def test_network(self, testset_address):
        testDf = pd.read_csv(testset_address)
        testX = pd.concat([testDf['X1'], testDf['X2']], axis=1, keys=['X1', 'X2'])
        testN = len(testX.index)
        testDf['Estimate'] = self.calc_y_hat(testX)

        testDf['Check'] = 0
        for i in range(testN):
            testDf['Check'][i] = 1 if np.abs(testDf['Label'][i] - testDf['Estimate'][i]) < 0.5 else 0
        print(testDf)
        self.accuracy = testDf['Check'].sum() / testN
        colors = ['red','black']
        testDf.plot(kind='scatter',x='X1',y='X2', c=testDf['Check'], cmap=matplotlib.colors.ListedColormap(colors))
        plt.savefig("test-scatter.png")


p = Perceptron(dataset_address="train.csv")
p.train_network()
p.test_network("test.csv")
print(p.W)
print(p.b)
print(str(p.accuracy*100) + "%")
