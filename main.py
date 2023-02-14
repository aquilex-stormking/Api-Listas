
from fastapi import FastAPI
from utils import cargarlistas,leerlistas

app = FastAPI()
cargar = cargarlistas.cargardatos()

@app.get("/ListaOfac")
async def root():
    datos=leerlistas.leerOfac()
    return datos

@app.get("/ListaOnu")
async def root():
    datos=leerlistas.leerOnu()
    return datos

@app.get("/ListaFbi")
async def root():
    datos=leerlistas.leerFbi()
    return datos

@app.get("/ActualizaListas")
async def root():
    cargarlistas.cargardatos()
    return 

