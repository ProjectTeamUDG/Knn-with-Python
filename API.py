from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

def load_data(path, extension):
    if extension == ".csv":
        return pd.read_csv(path+extension)
    elif extension == ".xlsx":
        return pd.read_excel(path+extension)
    return "Extension no valida"

# Cargar modelo y columnas
model = joblib.load("Modelo_KNN5.pkl")

app = FastAPI()

class Modelo_KNN(BaseModel):
    CLAVE_ARTICULO: int
    cantidad: int
    linea_articulo: int
    precio: float

@app.post("/recomendar")
def recomendar(data: Modelo_KNN):
    dictionary = load_data("Temporal", ".xlsx")
    # Obtener características del artículo de referencia
    article_features = pd.DataFrame({
    "TOTAL_ARTICULOS": [data.cantidad],
    "TOTAL_CLIENTES": [1],
    "LINEA_ARTICULO_ID": [data.linea_articulo],
    "PRECIO": [data.precio]
    })

    # Buscar los artículos más cercanos
    distances, indices = model.kneighbors(article_features)

    results = []
    for index in enumerate(indices):
        similar_article = dictionary.iloc[index]["CLAVE_ARTICULO"]
        results.append(similar_article)
    temporal = pd.DataFrame({"CLAVE_ARTICULO": [results]})
    return {
        "recomendaciones":temporal,
        "distancias": distances[0].tolist()
    }