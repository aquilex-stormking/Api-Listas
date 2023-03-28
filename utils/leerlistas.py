import pandas as pd
import warnings
import numpy as np

warnings.filterwarnings("ignore")


def leerOfac():

    datosOfac = pd.read_pickle("dummy.pkl") 

    lista=[]
    lista = datosOfac.to_numpy().tolist()

    

    return lista

def leerOnu():

    datosOnu = pd.read_pickle("dummy2.pkl")

    lista=[]
    lista = datosOnu.to_numpy().tolist()

    return lista

# def leerFbi():

#     datosFbi = pd.read_pickle("dummy3.pkl")

#     lista=[]
#     lista = datosFbi.to_numpy().tolist()

#     return lista


