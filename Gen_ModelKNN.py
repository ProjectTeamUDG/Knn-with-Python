import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import joblib


def load_data(path, extension):
    if extension == ".csv":
        return pd.read_csv(path+extension)
    elif extension == ".xlsx":
        return pd.read_excel(path+extension)
    return "Extension no valida"

def normalize(data):
    sub_set = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]
    sub_set = MinMaxScaler().fit_transform(data[sub_set])
    return data

def train_knn(data):
    features = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]
    knn = NearestNeighbors(n_neighbors=6, metric='euclidean')
    knn.fit(data[features])
    return knn


def recommend(knn, data, article_id):
    if article_id not in data["CLAVE_ARTICULO"].values:
        print(f"Artículo {article_id} no encontrado en los datos.")
        return

    # Obtener características del artículo de referencia
    article_features = data[data["CLAVE_ARTICULO"] == article_id][
        ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID", "PRECIO"]]

    print(article_features)

    # Buscar los artículos más cercanos
    distances, indices = knn.kneighbors(article_features)

    print(f"Artículos similares a {article_id}:")
    for i, index in enumerate(indices[0]):
        similar_article = data.iloc[index]["CLAVE_ARTICULO"]
        if similar_article != article_id:
            print(f"{i}. Artículo {similar_article} (Distancia: {distances[0][i]:.4f})")

def export_model(model_knn):
    joblib.dump(model_knn, "Modelo_KNN5.pkl")
    print("Modelo exportado")

def main():
    data = load_data("Data", ".xlsx")
    data = normalize(data)

    knn = train_knn(data)
    export_model(knn)

    # for i in range(10):
    #     CLAVE_ARICULO = int(input("Ingrese CLAVE_ARICULO:"))
    #     # Prueba recomendando artículos similares a uno dado (por ejemplo, el artículo con ID 12345)
    #     recommend(knn, data, 100002)
main()
