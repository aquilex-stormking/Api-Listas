from fastapi import FastAPI
from utils import cargarlistas,leerlistas

app = FastAPI()
cargar = cargarlistas.cargardatos()

@app.get("/ListaOfac", tags=["Listas"])
async def root():
    datos=leerlistas.leer_ofac()
    return datos

@app.get("/ListaOnu", tags=["Listas"])
async def root():
    datos=leerlistas.leer_onu()
    return datos

@app.get("/ListaFbi", tags=["Listas"])
async def root():
    datos=leerlistas.leer_fbi()
    return datos

@app.get("/ListaTerro", tags=["Listas"])
async def root():
    datos=leerlistas.leer_terro()
    return datos

@app.get("/ListaTerro2", tags=["Listas"])
async def root():
    datos=cargarlistas.terroristas()
    return datos

@app.get("/ActualizaListas")
async def root():
    lista = cargarlistas.cargardatos()
    return lista
    

