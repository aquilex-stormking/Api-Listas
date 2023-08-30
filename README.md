# Fast-Api-Listas
#Descargar Python: Ve a la página oficial de descargas de Python y descarga la versión que necesites.

#Instalar Python: Ejecuta el archivo descargado y sigue las instrucciones. Asegúrate de marcar la casilla "Add Python to PATH" durante la instalación.

#Verificar la Instalación: Abre una nueva ventana de terminal (CMD) y ejecuta:

python --version

# Instalar FastAPI y Hypercorn: Instala FastAPI y Hypercorn usando pip:

pip install fastapi hypercorn

#Correr FastAPI con Hypercorn: Navega a la carpeta de tu proyecto y ejecuta el siguiente comando (reemplaza main:app con la ubicación de tu aplicación FastAPI):

hypercorn main:app --bind 0.0.0.0:8080

