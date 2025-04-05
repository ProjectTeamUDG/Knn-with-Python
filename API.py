from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import joblib

# Cargar modelo y columnas
modelName = "Modelo_KNN5"
dataName = "Data"
#Scaler comentado, pues ya esta escalada la informacion
#scalerName = "Scaler"
model = joblib.load(modelName+".pkl")
data = joblib.load(dataName+".pkl")
#scaler = joblib.load(scalerName+".pkl")

app = FastAPI()

class ModeloKNN(BaseModel):
    clave_articulo: int

@app.post("/recomendar")
def recomendar(container: ModeloKNN):
    if container.clave_articulo not in data["CLAVE_ARTICULO"].values:
        raise HTTPException(
            status_code=404,
            detail=f"Artículo {container.clave_articulo} no encontrado en los datos."
        )

    # Obtener características del artículo de referencia
    feature_cols = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]

    article_row = data[data["CLAVE_ARTICULO"] == container.clave_articulo]
    article_features = article_row[feature_cols].values

    # Buscar los artículos más cercanos
    distances, indices = model.kneighbors(article_features)

    #Lista de articulos a recomendar
    recommendations = []
    for i, index in enumerate(indices[0]):
        similar_article = data.iloc[index]["CLAVE_ARTICULO"]
        if i > 0:#Excluyendo el mismo articulo
            recommendations.append(similar_article)

    return {
        "recomendaciones":recommendations,
        "distancias": distances[0].tolist()
    }

