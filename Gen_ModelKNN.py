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
        #----------------------Strings para los serializados-------------------------
        self.modelName = "Modelo_KNN5"
        self.dataName = "Data"
        self.scalerName = "Scaler"
        #----------------------Strings para los serializados-------------------------

        self.data : pd.DataFrame = pd.DataFrame()
        self.model = NearestNeighbors(n_neighbors=neighbors, metric='euclidean', algorithm='auto')
        self.features = ["CLAVE_ARTICULO","TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]

        #---------------------stuff for normalize------------------------------------
        self.scaler = MinMaxScaler()
        print("\nSetting Knn Nearest Neighbors with:"
              "\n Modelo: ", self.model.get_params(),
              "\n Caracteristicas: ", self.features,
              "\n Scaler: ", self.scaler.get_params())

        self.normalize_data(raw_data)
        self.index_data()
        self.export_model()

    def normalize_data(self, raw_data):
        self.data = raw_data.copy()
        self.data[self.features[1:]] = self.scaler.fit_transform(self.data[self.features[1:]])
        print("\nDatos normalizados")

    def index_data(self):
        self.model.fit(self.data[self.features[1:]])
        print("\nDatos indexados")

    def recommend(self, article_id):

        if article_id not in self.data["CLAVE_ARTICULO"].values:
            print(f"\nArtículo {article_id} no encontrado en los datos.")
            return

        # Obtener características del artículo de referencia
        article_features = self.data[self.data["CLAVE_ARTICULO"] == article_id][
            ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]]

        print("\nSelected article: ")
        print(article_features)

        # Buscar los artículos más cercanos
        distances, indices = self.model.kneighbors(article_features)

        print(f"\nArtículos similares a {article_id}:")
        for i, index in enumerate(indices[0]):
            similar_article = self.data.iloc[index]["CLAVE_ARTICULO"]
            if similar_article != article_id:
                print(f"{i}. Artículo {similar_article} (Distancia: {distances[0][i]:.4f})")

    def export_model(self):
        extension = ".pkl"
        joblib.dump( self.model, self.modelName+extension)
        joblib.dump( self.data, self.dataName+extension)
        #Scaler comentado, pues ya esta escalada la informacion
        #joblib.dump( self.scaler, self.scalerName+extension)
        print("\nModelo exportado a:",
              "\n\t"+self.modelName+extension,
              "\n\t"+self.dataName+extension,
        #     "\n\t"+self.scalerName+extension,
              "\nEsta informacion es necesaria para la API...")

def load_data(path, extension):
    if not Path(path + extension).exists():
        print("\nArchivo no encontrado")
    elif extension == ".csv":
        return pd.read_csv(path+extension)
    elif extension == ".xlsx":
        return pd.read_excel(path+extension)
    else:
        print("\nExtension no valida")
    return

def main():
    model = RecommendKnn(load_data("Data", ".xlsx"), 3)
    model.recommend(100002)

main()
