import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt, matplotlib

mu, sigma = 0.0, 1.0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Network:
    def __init__(self, n_epoch=500, learning_rate=0.15, dataset_address=None):
        self.n_epoch = n_epoch
        self.learning_rate = learning_rate
        df = pd.read_csv(dataset_address)
        self.dataX = np.asarray(pd.concat([df['X1'], df['X2']], axis=1, keys=['X1', 'X2']))
        self.percX = pd.DataFrame()
        self.y = pd.concat([df['Label']], axis=1, keys=['Label']).values.flatten()
        self.rows = self.dataX.shape[0]
        self.columns = self.dataX.shape[1]
        self.ones = np.ones_like(self.y)
        self.A = Perceptron(self.dataX, self.rows, self.columns)
        self.B = Perceptron(self.dataX, self.rows, self.columns)
        self.C = Perceptron(None, self.rows, self.columns)

    def weird_calc(self, first, calc):
        a_minus = np.matmul(calc, np.subtract(self.ones, calc).T)
        return first * a_minus

    def rate_generator(self, gradient):
        return self.learning_rate * gradient / self.rows

    def train_network(self):
        for _ in range(self.n_epoch):
            y_hat = self.calc_y_hat()
            coeff = 2 * np.subtract(y_hat, self.y) * y_hat * (1 - y_hat)

            base_a = coeff * self.weird_calc(self.C.W[0], self.percX['X1'])
            ab_gradient = base_a.sum()
            aw_gradient = np.matmul(self.dataX.T, base_a)
            
            base_b = coeff * self.weird_calc(self.C.W[1], self.percX['X2'])
            bb_gradient = (base_b).sum()
            bw_gradient = np.matmul(self.dataX.T, base_b)

            base_c = coeff
            cb_gradient = base_c.sum()
            cw_gradient = np.matmul(self.dataX.T, base_c)

            self.C.W -= self.rate_generator(cw_gradient)
            self.B.W -= self.rate_generator(bw_gradient)
            self.A.W -= self.rate_generator(aw_gradient)
            self.C.b -= self.rate_generator(cb_gradient)
            self.B.b -= self.rate_generator(bb_gradient)
            self.A.b -= self.rate_generator(ab_gradient)

    def calc_y_hat(self, X=None):
        self.percX['X1'] = self.A.calc_y_hat(X=X)
        self.percX['X2'] = self.B.calc_y_hat(X=X)
        return self.C.calc_y_hat(self.percX)


    def test_network(self, testset_address):
        testDf = pd.read_csv(testset_address)
        testX = np.asarray(pd.concat([testDf['X1'], testDf['X2']], axis=1, keys=['X1', 'X2']))
        testN = testX.shape[0]
        self.percX = pd.DataFrame()
        testDf['Estimate'] = self.calc_y_hat(testX)

        testDf['Check'] = 0
        for i in range(testN):
            testDf['Check'][i] = 1 if np.abs(testDf['Label'][i] - testDf['Estimate'][i]) < 0.5 else 0
        print(testDf)
        self.accuracy = testDf['Check'].sum() / testN
        colors = ['red','black']
        testDf.plot(kind='scatter',x='X1',y='X2', c=testDf['Check'], cmap=matplotlib.colors.ListedColormap(colors))
        plt.savefig("test3-node-scatter.png")


class Perceptron:
    def __init__(self, X, rows, columns):
        self.X = X
        self.rows = rows
        self.columns = columns
        self.W = np.random.normal(mu, sigma, size=columns)
        self.b = np.random.normal(mu, sigma, size=1)

    def calc_y_hat(self, X=None):
        if X is None:
            X = self.X
        y_hat = np.dot(self.W, X.T) + self.b
        return sigmoid(y_hat)





p = Network(dataset_address="train.csv")
p.train_network()
p.test_network("test.csv")
print(str(p.accuracy*100) + "%")
