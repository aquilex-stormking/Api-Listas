
from fastapi import FastAPI
from utils import cargarlistas,leerlistas

app = FastAPI()
cargar = cargarlistas.cargardatos()

@app.get("/ListaOfac")
async def root():
    datos=leerlistas.leer_ofac()
    return datos

@app.get("/ListaOnu")
async def root():
    datos=leerlistas.leer_onu()
    return datos

@app.get("/ListaFbi")
async def root():
    datos=leerlistas.leer_fbi()
    return datos

@app.get("/ActualizaListas")
async def root():
    cargarlistas.cargardatos()
    

