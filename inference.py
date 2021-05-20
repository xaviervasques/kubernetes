#!/usr/bin/python3
# inference.py
# Xavier Vasques 13/04/2021


import platform; print(platform.platform())
import sys; print("Python", sys.version)
import numpy; print("NumPy", numpy.__version__)
import scipy; print("SciPy", scipy.__version__)

import os
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
import pandas as pd
from joblib import load
from sklearn import preprocessing
import paramiko


def inference():

    MODEL_DIR = os.environ["MODEL_DIR"]
    MODEL_FILE_LDA = os.environ["MODEL_FILE_LDA"]
    MODEL_FILE_NN = os.environ["MODEL_FILE_NN"]
    MODEL_PATH_LDA = os.path.join(MODEL_DIR, MODEL_FILE_LDA)
    MODEL_PATH_NN = os.path.join(MODEL_DIR, MODEL_FILE_NN)

    # Load, read and normalize testing data
    testing = "https://raw.githubusercontent.com/xaviervasques/kubernetes/main/test.csv"
    data_test = pd.read_csv(testing)

    y_test = data_test['# Letter'].values
    X_test = data_test.drop(data_test.loc[:, 'Line':'# Letter'].columns, axis = 1)

    print("Shape of the test data")
    print(X_test.shape)
    print(y_test.shape)

    # Data normalization (0,1)
    X_test = preprocessing.normalize(X_test, norm='l2')

    # Go to remote server, load trained models, output scores and predictions
    print("Moving to 192.168.1.11, load LDA and NN models and provide accuracy scores and predictions")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file('id_rsa')
    ssh_client.connect("192.168.1.11", username="LRENC",pkey=k)

    print(MODEL_PATH_LDA)
    sftp_client = ssh_client.open_sftp()
    remote_file = sftp_client.open("/Users/LRENC/Desktop/Kubernetes/Jenkins/"+MODEL_FILE_LDA)

    #clf_lda = load(MODEL_PATH_LDA)
    clf_lda = load(remote_file)
    print("LDA score and classification:")
    print(clf_lda.score(X_test, y_test))
    print(clf_lda.predict(X_test))

    remote_file.close()

    print(MODEL_PATH_NN)
    sftp_client = ssh_client.open_sftp()
    remote_file = sftp_client.open("/Users/LRENC/Desktop/Kubernetes/Jenkins/"+MODEL_FILE_NN)

    # Run model
    #clf_nn = load(MODEL_PATH_NN)
    clf_nn = load(remote_file)
    print("NN score and classification:")
    print(clf_nn.score(X_test, y_test))
    print(clf_nn.predict(X_test))

    remote_file.close()

if __name__ == '__main__':
    inference()
