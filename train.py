#!/usr/bin/python3
# train.py
# Xavier Vasques 16/05/2021

import os
import json
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd
from joblib import dump, load
from sklearn import preprocessing
import paramiko


def train():

    # Load directory paths for persisting model

    MODEL_DIR = os.environ["MODEL_DIR"]
    MODEL_FILE_LDA = os.environ["MODEL_FILE_LDA"]
    MODEL_FILE_NN = os.environ["MODEL_FILE_NN"]
    METADATA_FILE = os.environ["METADATA_FILE"]
    MODEL_PATH_LDA = os.path.join(MODEL_DIR, MODEL_FILE_LDA)
    MODEL_PATH_NN = os.path.join(MODEL_DIR, MODEL_FILE_NN)
    METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILE)

    # Load training data
    url="https://raw.githubusercontent.com/xaviervasques/Jenkins/main/train.csv"
    data_train = pd.read_csv(url)

    y_train = data_train['# Letter'].values
    X_train = data_train.drop(data_train.loc[:, 'Line':'# Letter'].columns, axis = 1)

    # Print the shape of the training data
    print("Shape of the training data")
    print(X_train.shape)
    print(y_train.shape)

    # Data normalization (0,1)
    X_train = preprocessing.normalize(X_train, norm='l2')

    # Models training

    # Linear Discrimant Analysis (Default parameters)
    clf_lda = LinearDiscriminantAnalysis()
    clf_lda.fit(X_train, y_train)

    # Serialize model
    from joblib import dump
    dump(clf_lda, MODEL_PATH_LDA)

    # Neural Network: multi-layer perceptron (MLP)
    clf_NN = MLPClassifier(solver='adam', activation='relu', alpha=0.0001, hidden_layer_sizes=(500,), random_state=0, max_iter=1000)
    clf_NN.fit(X_train, y_train)

    # Serialize model
    from joblib import dump, load
    dump(clf_NN, MODEL_PATH_NN)

    # Perform cross validation and store it in a json file
    accuracy_lda = cross_val_score(clf_lda, X_train, y_train, cv=5)
    accuracy_nn = cross_val_score(clf_NN, X_train, y_train, cv=5)

    print(accuracy_lda)

    metadata = {
        "train_accuracy_lda": accuracy_lda.mean(),
        "train_accuracy_nn": accuracy_nn.mean()
    }

    print("Serializing metadata to: {}".format(METADATA_PATH))
    with open(METADATA_PATH, 'w') as outfile:
        json.dump(metadata, outfile)

    print("Moving to 192.168.1.11")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file('id_rsa')
    client.connect("192.168.1.11", username="LRENC",pkey=k)

    # upload the file using SFTP
    sftp = client.open_sftp()

    sftp.put(MODEL_PATH_LDA,"/Users/LRENC/Desktop/Kubernetes/Jenkins/"+MODEL_FILE_LDA)
    sftp.put(MODEL_PATH_NN,"/Users/LRENC/Desktop/Kubernetes/Jenkins/"+MODEL_FILE_NN)
    sftp.put(METADATA_PATH,"/Users/LRENC/Desktop/Kubernetes/Jenkins/"+METADATA_FILE)

    sftp.close()
    client.close()

if __name__ == '__main__':
    train()
