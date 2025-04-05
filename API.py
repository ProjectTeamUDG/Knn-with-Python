from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import inspect

class Model:

    def __init__(self, model_name, data_name):
        self.model = None
        self.data = None
        #self.scaler = None
        self.load_data(model_name, data_name)

    def load_data(self, model_name, data_name):
        # Cargar modelo y datos del entrenamiento
        self.model = joblib.load(model_name + ".pkl")
        self.data = joblib.load(data_name + ".pkl")

        # Scaler comentado, pues ya esta escalada la informacion
        # scalerName = "Scaler"
        # self.scaler = joblib.load(scalerName+".pkl")

    # noinspection PyBroadException
    def get_recommendation(self, article_id):
        try:
            #------------------------------------------------------------------------------------
            if not isinstance(self.data, pd.DataFrame) or self.data.empty:
                return 500, "Datos no cargados o vacíos"

            if not hasattr(self.model, "kneighbors"):
                return 500, "Modelo no cargado correctamente"

            if article_id not in self.data["CLAVE_ARTICULO"].values:
                return 404, f"Artículo {article_id} no encontrado en los datos."

            #------------------------------------------------------------------------------------

            # Obtener características del artículo de referencia
            feature_cols = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]

            article_row = self.data[self.data["CLAVE_ARTICULO"] == article_id]
            article_features = article_row[feature_cols].values

            # Buscar los artículos más cercanos
            distances, indices = self.model.kneighbors(article_features)

            # Lista de articulos a recomendar
            recommendations = []
            for i, index in enumerate(indices[0]):
                similar_article = self.data.iloc[index]["CLAVE_ARTICULO"]
                if i > 0:  # Excluyendo el mismo articulo
                    recommendations.append(similar_article)

            return 200, {
                "recomendaciones": recommendations,
                "distancias": distances[0].tolist()
            }
        except Exception as e:
            return 500, "Error en "+ inspect.currentframe().f_code.co_name

class ModeloKNN(BaseModel):
    clave_articulo: int

model = Model("Modelo_KNN5", "Data")
app = FastAPI()

@app.post("/recomendar")
def recommend(container: ModeloKNN):
    error_code, answer = model.get_recommendation(container.clave_articulo)
    if error_code != 200:
        raise HTTPException(
            status_code=error_code,
            detail=answer
        )
    return answer
