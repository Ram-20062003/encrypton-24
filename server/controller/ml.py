from re import T
import pandas as pd
import numpy as np
import pickle as pkl
import tensorflow as tf 
import keras
import os
import shap
import matplotlib.pyplot as plt

current_directory = os.getcwd()

forest = pkl.load(open(f"{current_directory}/server/controller/ml/if.pkl", 'rb'))
ae = keras.models.load_model(f"{current_directory}/server/controller/ml/ae.keras")
explainer = shap.TreeExplainer(forest)

# inp = namedtuple('inp', ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'changebalanceOrig', 'changebalanceDest', 'hour', 'CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])
# test_1 = inp(181,181,0,21182,0,-181,-21182,4,0,1,0,0,0)


# 1 means fraudlent, 0 means not fraudlent
def predict_isolation(data,id:int=0):
    prediction = forest.predict([data])
    shap_values = explainer.shap_values(np.asarray(data))
    # feature_names=['amount', 'oldbalOrg', 'newbalOrg', 'oldbalDest', 'newbalDest', 'chbalOrg', 'chbalDest', 'hour', 'CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']
    shap.force_plot(explainer.expected_value, shap_values,np.asarray(data),feature_names=['1', '2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'] ,matplotlib=True,show=False)
    plt.savefig(f"{current_directory}/server/controller/ml/images/gg-{id}.png",transparent=True)
    return prediction[0]

def predict_autoencoder(data) -> list[float] :
    if not ae:
        return []
    prediction = ae.predict([data])
    mse = np.mean(np.power(data - prediction, 2), axis=1)
    threshold = 3
    result = 0
    confidence = 0
    if mse > threshold:
        result = 1
        confidence = (mse - threshold)/mse
    else:
        confidence = (threshold - mse)/threshold
        result = 0
    return [result,confidence]