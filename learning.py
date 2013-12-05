import sys
import numpy as np
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.externals import joblib


class Observation(object):
    def __init__(self, data, classification):
        self.data = data
        self.classification = classification

    def as_vector(self):
        '''Child classes may override'''
        return self.data


class Dataset(list):
    '''A list of observations'''
    def X(self):
        flat = np.concatenate([o.as_vector() for o in self])
        return flat.reshape((len(self), -1))

    def y(self):
        return np.array([o.classification for o in self])

    def getXy(self):
        return self.X(), self.y()


class SVMClassifier(object):
    def __init__(self, dataset=None):
        self.dataset = dataset
        self.clf = None

    def train(self):
        self._assert_dataset_present()
        X, y = self.dataset.getXy()
        self.clf = svm.SVC()
        self.clf.fit(X, y)

    def validate(self, n_folds=10, verbose=False):
        '''Performs Stratified K-fold validation and returns the average precision (across folds)'''
        self._assert_dataset_present()
        labels = self.dataset.y()
        kf = StratifiedKFold(labels, n_folds=n_folds)
        precisions = []

        X, y = self.dataset.getXy()
        avg = None
        for k, (train_index, test_index) in enumerate(kf):
            X_train, y_train = X[train_index], y[train_index]
            X_test, y_test = X[test_index], y[test_index]

            clf = svm.SVC()
            clf.fit(X_train, y_train)

            predicted = clf.predict(X_test)
            success = [i == j for i, j in zip(predicted, y_test)]
            precisions += [float(sum(success)) / len(y_test)]
            avg = sum(precisions) / len(precisions)
            if verbose:
                print "K-fold %i/%i complete - average precision so far: %.2f" % (k + 1, n_folds, avg)
        return avg

    def predict(self, observation):
        self._assert_trained()
        return self.clf.predict(observation)

    def dump(self, path):
        '''Dump classifier to a file'''
        self._assert_trained()
        joblib.dump(self.clf, path, compress=9)
        print "Wrote:", path

    def load(self, path):
        '''Load a previously saved model'''
        self.clf = joblib.load(path)

    def _assert_trained(self):
        if self.clf is None:
            raise RuntimeError("Model must first be trained")

    def _assert_dataset_present(self):
        if self.dataset is None:
            raise ValueError("Classifier is not bound to a dataset")
