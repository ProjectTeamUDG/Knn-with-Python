import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

def load_data(path):
    return pd.read_csv(path)

def normalize(data):
    sub_set = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID"]
    sub_set = MinMaxScaler().fit_transform(data[sub_set])
    return data

def train_knn(data):
    features = ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID"]
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn.fit(data[features])
    return knn


def recommend(knn, data, article_id):
    if article_id not in data["CLAVE_ARTICULO"].values:
        print(f"Artículo {article_id} no encontrado en los datos.")
        return

    # Obtener características del artículo de referencia
    article_features = data[data["CLAVE_ARTICULO"] == article_id][
        ["TOTAL_ARTICULOS", "TOTAL_CLIENTES", "LINEA_ARTICULO_ID"]].values

    # Buscar los artículos más cercanos
    distances, indices = knn.kneighbors(article_features)

    print(f"Artículos similares a {article_id}:")
    for i, index in enumerate(indices[0]):
        similar_article = data.iloc[index]["CLAVE_ARTICULO"]
        if similar_article != article_id:
            print(f"{i + 1}. Artículo {similar_article} (Distancia: {distances[0][i]:.4f})")


def main():
    data = load_data("Data.csv")
    data = normalize(data)

    knn = train_knn(data)

    for i in range(10):
        CLAVE_ARICULO = int(input("Ingrese CLAVE_ARICULO:"))
        # Prueba recomendando artículos similares a uno dado (por ejemplo, el artículo con ID 12345)
        recommend(knn, data, CLAVE_ARICULO)

main()
