🧠 Recomendador KNN para Artículos
Este proyecto implementa un sistema de recomendación de artículos basado en el algoritmo KNN (K-Nearest Neighbors), y expone una API REST con FastAPI para consumir las recomendaciones.

🔧 Estructura del Proyecto
Gen_ModelKNN.py: Script que entrena el modelo KNN con un conjunto de datos y lo guarda en disco.

API.py: Script que levanta una API con FastAPI y expone un endpoint para recibir una clave de artículo y devolver recomendaciones.

modelo_knn.pkl: Archivo generado tras entrenar el modelo, usado por la API.
Data.pkl: guardar el DataFrame original es clave para poder interpretar la salida del modelo;El modelo guarda solo los vectores numéricos.
datos.csv: Dataset base para el entrenamiento.

🚀 1. Entrenamiento del Modelo
El modelo se entrena usando scikit-learn con un dataset de artículos. Se utiliza el algoritmo NearestNeighbors para encontrar los artículos más cercanos en función de sus características (por ejemplo, ID, categorías, o embeddings).

Resultado: Se guarda el modelo entrenado en un archivo .pkl que luego es cargado por la API.

🌐 2. API REST con FastAPI
La API expone un endpoint /recomendar que recibe un artículo (por su CLAVE_ARTICULO) y devuelve una lista de artículos similares recomendados por el modelo entrenado.

Método: POST
Ruta: /recomendar
-------------------------------------------
json
{
  "CLAVE_ARTICULO": 123
}
-------------------------------------------
json
{
  "recomendaciones": [456, 789, 321]
}
