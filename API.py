from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Cargar modelo y columnas
model = joblib.load("Modelo_KNN5.pkl")
modelData = joblib.load("Data.pkl")

app = FastAPI()

class ModeloKNN(BaseModel):
    CLAVE_ARTICULO: int

@app.post("/recomendar")
def recomendar(data: ModeloKNN):
    article_id = data.CLAVE_ARTICULO
    if article_id not in modelData["CLAVE_ARTICULO"].values:
        print(f"Artículo {article_id} no encontrado en los datos.")
        return

        # Obtener características del artículo de referencia
    article_features = modelData[modelData["CLAVE_ARTICULO"] == article_id][
        ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]]

    # Buscar los artículos más cercanos
    distances, indices = model.kneighbors(article_features)

    print(f"Artículos similares a {article_id}:")

    recommendations = []
    for i, index in enumerate(indices[0]):
        similar_article = modelData.iloc[index]["CLAVE_ARTICULO"]
        if i > 0:
            recommendations.append(similar_article)
            print(f"{i}. Artículo {similar_article} (Distancia: {distances[0][i]:.4f})")

    return {
        "recomendaciones":recommendations,
        "distancias": distances[0].tolist()
    }

