
# Sistema de Recomendación con KNN (k-Nearest Neighbors)

Este proyecto implementa un sistema de recomendación basado en el algoritmo **KNN**, construido con Python y expuesto a través de una **API con FastAPI**. Se diseñó para recomendar artículos similares en función de características como cantidad, precio, línea y comportamiento histórico.

---

## 🧠 Lógica General

- Se cargan datos tabulados de artículos.
- Se normalizan las características relevantes usando `MinMaxScaler`.
- Se entrena un modelo `NearestNeighbors` con los datos normalizados.
- Se expone un endpoint `/recomendar` que devuelve artículos similares a uno dado.
- La respuesta incluye los IDs recomendados y sus distancias.

---

## 🛠️ Estructura de Archivos

### `Gen_ModelKNN.py`

- Contiene la clase `RecommendKnn`.
- Funcionalidades:
  - `load_data(...)`: Carga archivos CSV o Excel.
  - `normalize_data(...)`: Escala características numéricas.
  - `index_data(...)`: Ajusta el modelo KNN.
  - `recommend(...)`: Imprime por consola artículos similares.
  - `export_model(...)`: Guarda modelo, datos y scaler (`*.pkl`).

- Datos utilizados:
  - `"CLAVE_ARTICULO"` (no se normaliza)
  - `"TOTAL_ARTICULOS"`, `"TOTAL_CLIENTES"`, `"LINEA_ARTICULO_ID"`, `"PRECIO"`

- Modelos serializados:
  - `Modelo_KNN5.pkl`
  - `Data.pkl` (ya normalizado)
  - `Scaler.pkl` (solo necesario si se usan nuevos artículos)

---

### `API.py`

- Exposición vía FastAPI
- Endpoint: `POST /recomendar`
- Entrada esperada (JSON):
```json
{
  "clave_articulo": 123456
}
```

- Funcionamiento:
  - Verifica si el artículo existe en los datos.
  - Extrae sus características ya normalizadas.
  - Calcula vecinos más cercanos.
  - Retorna artículos similares distintos al solicitado.

- Respuesta:
```json
{
  "recomendaciones": [100001, 100045, 100078],
  "distancias": [0.12, 0.23, 0.29]
}
```

---

## ⚠️ Consideraciones

- **El modelo requiere que los datos estén normalizados**, por eso en la API no se vuelve a aplicar el `scaler`.
- **Los resultados serán incorrectos si escalás dos veces** los datos o si usás características fuera del rango original.
- Para artículos **nuevos no presentes en el dataset**, se debe:
  - Guardar el `scaler.pkl` al entrenar.
  - En la API: recibir las características y escalar con ese mismo `scaler`.

---

## ✅ Recomendaciones

- Validar entrada en la API con `HTTPException`.
- Usar `.values` en lugar de `.transform()` cuando los datos ya están normalizados.
- Hacer logging o impresión de artículos, distancias y entradas para debugging.

---

## 📦 Requisitos

- Python 3.8+
- pandas
- scikit-learn
- fastapi
- uvicorn

---

## 🚀 Ejecución

### 1. Entrenamiento del modelo

```bash
python Gen_ModelKNN.py
```

### 2. Levantar la API

```bash
uvicorn API:app --reload
```

---

Desarrollado con fines de exploración y aprendizaje. ¡Que tus recomendaciones siempre sean relevantes!
