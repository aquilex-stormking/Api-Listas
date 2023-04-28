import pandas as pd
import warnings
import numpy as np

warnings.filterwarnings("ignore")


def leer_ofac():

    datos_ofac = pd.read_pickle("dummy.pkl") 

    lista=[]
    lista = datos_ofac.to_numpy().tolist()

    

    return lista

def leer_onu():

    datos_onu = pd.read_pickle("dummy2.pkl")

    lista=[]
    lista = datos_onu.to_numpy().tolist()

    return lista

def leer_fbi():

    datos_fbi = pd.read_pickle("dummy3.pkl")

    lista=[]
    lista = datos_fbi.to_numpy().tolist()

    return lista


