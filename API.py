from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

# Cargar modelo y columnas
model = joblib.load("Modelo_KNN5.pkl")
columns = joblib.load("Columnas.pkl")

app = FastAPI()

class Modelo_KNN(BaseModel):
    CLAVE_ARTICULO: int
    cantidad: int
    precio: float

@app.post("/recomendar")
def recomendar(data: Modelo_KNN):
    article_id = data.CLAVE_ARTICULO

    # Obtener características del artículo de referencia
    article_features = pd.DataFrame({
    "TOTAL_ARTICULOS": [data.cantidad],
    "TOTAL_CLIENTES": [1],
    "LINEA_ARTICULO_ID": [1],
    "PRECIO": [data.precio]
    })

    # Buscar los artículos más cercanos
    distances, indices = model.kneighbors(article_features)

    return {
        "recomendaciones": indices[0].tolist(),
        "distancias": distances[0].tolist()
    }