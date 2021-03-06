#!/usr/bin/python

# HTTP client
import httplib
import json
import os

# Model training
from mnist import MNIST
import numpy as np
from sklearn import neural_network as nn

# Model serialization
from sklearn2pmml import sklearn2pmml
from sklearn.externals import joblib


def query_digit(digit, host=None, port=None):
    """
    Issues HTTP POST to host, port with digit array
    Expects a digit in the response
    """
    if not host or not port:
        host, port = "localhost", 4567
    con = httplib.HTTPConnection(host, port)
    params = json.dumps({"data": digit})
    con.request("POST", "/digit", params)
    response = con.getresponse()
    print "For digit:%s\nReceived prediction response [%s]\n" % (MNIST.display(digit), response.read())


def draw_random_misclassification(truth_array, prediction, test_label, test_data):
    """
    Prints the prediction, label and digit for a random misclassified sample
    """
    incorrect_idx = [idx for idx, is_true in enumerate(truth_array) if not is_true]
    n = incorrect_idx[np.random.randint(0, len(incorrect_idx))]
    print "predicted [%s]\nlabeled [%s]\nraw data:\n%s" % (prediction[n].argmax(), test_label[n], MNIST.display(test_data[n]))


def main():
    data = MNIST('./data')

    def transform(x):
        return x / 255.

    # 60,000 train samples of 28x28 grid, domain 0-255
    mnist_train_data, mnist_train_label = data.load_training()
    mnist_train_data_norm = np.array([transform(np.array(x)) for x in mnist_train_data])

    mlp_config = {'hidden_layer_sizes': (1000,),
                  'activation': 'relu',
                  'algorithm': 'adam',
                  'max_iter': 20,
                  'early_stopping': True,
                  'validation_fraction': 0.1,
                  'verbose': True
                  }
    mnist_classifier = nn.MLPClassifier(**mlp_config)
    mnist_classifier.fit(X=mnist_train_data_norm, y=mnist_train_label)

    # 10,000 test samples
    mnist_test_data, mnist_test_label = data.load_testing()
    mnist_test_data_norm = np.array([transform(np.array(x)) for x in mnist_test_data])

    prediction = mnist_classifier.predict_proba(mnist_test_data_norm)
    truth_array = [prediction[idx].argmax() == mnist_test_label[idx] for idx in range(len(prediction))]
    accuracy = float(sum(truth_array)) / float(len(truth_array))
    print "out of sample model accuracy [%s]" % accuracy

    print "serializing to pmml without transform (User defined transform not yet supported"
    pmml_path = "./model_pmml"
    if not os.path.exists(pmml_path):
        os.mkdir(pmml_path)
    sklearn2pmml(mnist_classifier, None, pmml_path + "/MLP_MNIST.pmml", with_repr=True)

    print "serializing with joblib for import in python"
    # KJS TODO: Serialize transform with the model
    pickle_path = "./model_pickle"
    if not os.path.exists(pickle_path):
        os.mkdir(pickle_path)
    joblib.dump(mnist_classifier, pickle_path + "/MLP_MNIST.pkl")


if __name__ == '__main__':
    main()
