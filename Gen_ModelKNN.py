import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from pathlib import Path
import joblib

class RecommendKnn:
    def __init__(self, raw_data, neighbors):
        if raw_data is None:
            print("Datos no encontrados")
            return
        self.data : pd.DataFrame = pd.DataFrame()
        self.model = NearestNeighbors(n_neighbors=neighbors, metric='euclidean', algorithm='auto')
        self.features = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]

        #stuff for normalize
        self.scaler = MinMaxScaler()
        print("Setting Knn Nearest Neighbors with:"
              "\n Modelo: ", self.model.get_params(),
              "\n Caracteristicas: ", self.features,
              "\n Scaler: ", self.scaler.get_params())

    def normalize_data(self, raw_data):
        self.data = self.scaler.fit_transform(self.data[self.features])
        print("Datos normalizados")

    def index_data(self):
        self.model.fit(self.data[self.features])
        print("Datos indexados")

    def recommend(self, article_id):

        if article_id not in self.data["CLAVE_ARTICULO"].values:
            print(f"Artículo {article_id} no encontrado en los datos.")
            return

        # Obtener características del artículo de referencia
        article_features = self.data[self.data["CLAVE_ARTICULO"] == article_id][
            ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]]

        print(article_features)

        # Buscar los artículos más cercanos
        distances, indices = self.model.kneighbors(article_features)

        print(f"Artículos similares a {article_id}:")
        for i, index in enumerate(indices[0]):
            similar_article = self.data.iloc[index]["CLAVE_ARTICULO"]
            if similar_article != article_id:
                print(f"{i}. Artículo {similar_article} (Distancia: {distances[0][i]:.4f})")

    def export_model(self):
        joblib.dump( self.model, "Modelo_KNN5.pkl")
        joblib.dump( self.data, "Data.pkl")
        joblib.dump( self.scaler, "Scaler.pkl")
        print("Modelo exportado")

def load_data(path, extension):
    if not Path(path + extension).exists():
        print("Archivo no encontrado")
    elif extension == ".csv":
        return pd.read_csv(path+extension)
    elif extension == ".xlsx":
        return pd.read_excel(path+extension)
    else:
        print("Extension no valida")
    return

def main():
    model = RecommendKnn(load_data("Data", ".xlsx"), 3)

main()
