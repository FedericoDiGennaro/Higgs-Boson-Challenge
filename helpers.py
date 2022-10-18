# -*- coding: utf-8 -*-
"""some helper functions."""

import numpy as np
import csv

def build_poly(x, degree):
    """polynomial basis functions for input data x, for j=0 up to j=degree.
    
    Args:
        x: numpy array of shape (N,), N is the number of samples.
        degree: integer.
        
    Returns:
        poly: numpy array of shape (N,d+1)
        
    >>> build_poly(np.array([0.0, 1.5]), 2)
    array([[1.  , 0.  , 0.  ],
           [1.  , 1.5 , 2.25]])
    """    
    # ***************************************************
    
    phi=np.ones((len(x),1))
    for i in range(1,degree+1):
        phi=np.c_[phi,x**i]
        
    # ***************************************************
    return phi

def load_train_data(path,default_missing_value = -999):
    """Load data function. 
    Arguments:
    path : path to find the file

    Returns
    ids : numpy array containing ids of the observed data
    tx : feature matrix
    y : prediction converted according to the rule {'b': 1, 's': 0}
    """
    columns_labels = np.genfromtxt(path, delimiter = ',', max_rows = 1, dtype = str, usecols = list(range(2,32)))
    ids = np.genfromtxt(path, delimiter = ',',usecols = [0], dtype = int, skip_header = 1)
    tx = np.genfromtxt(path,skip_header = 1, delimiter = ',', usecols = list(range(2,32)))
    y = np.genfromtxt(path, skip_header = 1, delimiter = ',', usecols = 1, converters = {1: lambda x: 1 if x == b's' else 0}, dtype = int)
    tx[tx == default_missing_value] = np.nan
    return y,tx,ids,columns_labels

def load_test_data(path,missing_values = -999.0):
    """Load data function. 
    Arguments:
    path : path to find the file

    Returns
    ids : numpy array containing ids of the observed data
    tx : feature matrix
    y : prediction converted according to the rule {'b': 1, 's': 0}
    """
    ids = np.genfromtxt(path, delimiter = ',',usecols = [0], dtype = int, skip_header = 1)
    tx = np.genfromtxt(path,skip_header = 1, delimiter = ',', usecols = list(range(2,32)))
    tx[tx == missing_values]=np.nan
    return tx,ids


def batch_iter(y, tx, batch_size=1, num_batches=1, shuffle=True):
    """
    Generate a minibatch iterator for a dataset.
    Takes as input two iterables (here the output desired values 'y' and the input data 'tx')
    Outputs an iterator which gives mini-batches of `batch_size` matching elements from `y` and `tx`.
    Data can be randomly shuffled to avoid ordering in the original data messing with the randomness of the minibatches.
    Example of use :
    for minibatch_y, minibatch_tx in batch_iter(y, tx, 32):
        <DO-SOMETHING>
    """
    data_size = len(y)

    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_y = y[shuffle_indices]
        shuffled_tx = tx[shuffle_indices]
    else:
        shuffled_y = y
        shuffled_tx = tx
    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, data_size)
        if start_index != end_index:
            yield shuffled_y[start_index:end_index], shuffled_tx[start_index:end_index]

def build_model_data(y, X_without_offset):
    """Form (y,tX) to get regression data in matrix form."""
    num_samples = len(y)
    tx = np.c_[np.ones(num_samples), X_without_offset]
    return y, tx

def sigmoid(x):
    """
    Compute sigmoid function for logistic regression.
    """
    return 1/(1+np.exp(-x))

def predict(tx,w,threshold):
    """
    Prediction function for logistic regresson model.
    """
    prediction = sigmoid(tx.dot(w))
    prediction[prediction >= threshold] = 1
    prediction[prediction < threshold] = -1
    return prediction.astype(int)

def create_submission(ids,y_pred,name,file_name):
    """
    Create a csv file to submit the output to the challenge arena.
    """
    with open(file_name,'w',newline ='') as file:
        dw = csv.DictWriter(file,delimiter =',',fieldnames = name)
        dw.writeheader()
        for r1,r2 in zip(ids,y_pred):
            dw.writerow({'Id':r1,'Prediction':r2})
