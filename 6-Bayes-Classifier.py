from __future__ import print_function, division
from builtins import range, input
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn

from tensorflow.examples.tutorials.mnist import input_data

class BayesClassifier:
  def fit(self, X, Y):
    # assume classes are numbered 0...K-1
    self.K = len(set(Y))

    self.gaussians = []
    self.p_y = np.zeros(self.K)
    for k in range(self.K):
      Xk = X[Y == k]

      self.p_y[k] = len(Xk)
      mean = Xk.mean(axis=0)
      cov = np.cov(Xk.T)

      g = {'m': mean, 'c': cov}
      self.gaussians.append(g)
    # normalize p(y)
    self.p_y /= self.p_y.sum()

  def sample_given_y(self, y):
    g = self.gaussians[y]
    return mvn.rvs(mean=g['m'], cov=g['c'])

  def sample(self):
    y = np.random.choice(self.K, p=self.p_y)
    return self.sample_given_y(y)


if __name__ == '__main__':
  # X, Y = util.get_mnist()
  mnist = input_data.read_data_sets(train_dir="../03-Convolutional-Neural-Networks/MNIST_data/", one_hot=False)

  X = mnist.train.images
  Y = mnist.train.labels


  clf = BayesClassifier()
  clf.fit(X, Y)

  for k in range(clf.K):
    # show one sample for each class
    # also show the mean image learned

    sample = clf.sample_given_y(k).reshape(28, 28)
    mean = clf.gaussians[k]['m'].reshape(28, 28)

    plt.subplot(1,2,1)
    plt.imshow(sample, cmap='gray')
    plt.title("Sample")
    plt.subplot(1,2,2)
    plt.imshow(mean, cmap='gray')
    plt.title("Mean")
    plt.show()

  # generate a random sample
  sample = clf.sample().reshape(28, 28)
  plt.imshow(sample, cmap='gray')
  plt.title("Random Sample from Random Class")
  plt.show()
