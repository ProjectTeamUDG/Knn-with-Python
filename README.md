
# 🧠 Sistema de Recomendación con KNN (k-Nearest Neighbors)

Este proyecto implementa un sistema de recomendación basado en el algoritmo KNN, entrenado con datos normalizados y expuesto a través de una API con FastAPI. Está diseñado para recomendar artículos similares a uno dado, usando propiedades como cantidad de ventas, número de clientes, línea del artículo y precio.

---

## 📁 Estructura de Archivos

### `Gen_ModelKNN.py`

Contiene la clase `RecommendKnn`, encargada de:

- Cargar los datos desde Excel o CSV.
- Normalizar las columnas numéricas (`MinMaxScaler`).
- Entrenar el modelo `NearestNeighbors`.
- Exportar el modelo (`.pkl`) y los datos normalizados.

**Métodos principales:**

- `normalize_data(raw_data)`: Escala columnas seleccionadas (`features[1:]`).
- `index_data()`: Ajusta el modelo con los datos escalados.
- `recommend(article_id)`: Muestra artículos similares por consola.
- `export_model()`: Guarda modelo y datos escalados.
- `load_data(...)`: Función externa para cargar datos desde archivo.

---

### `API.py`

Contiene la clase `Model` y la API FastAPI con un solo endpoint:

**Clase `Model`:**
- Carga el modelo y los datos normalizados desde archivos `.pkl`.
- Método `get_recommendation(article_id)`:
  - Verifica existencia de datos y del modelo.
  - Obtiene las características del artículo buscado.
  - Calcula vecinos usando `.kneighbors()`.
  - Devuelve lista de artículos similares y sus distancias.

**Endpoint disponible:**
- `POST /recomendar`
```json
{
  "clave_articulo": 100002
}
```

**Respuesta esperada:**
```json
{
  "recomendaciones": [100001, 100045, 100078],
  "distancias": [0.12, 0.23, 0.29]
}
```

---

## ⚠️ Consideraciones

- Los datos exportados (`Data.pkl`) **ya están normalizados**, por lo tanto el `scaler` no se usa en la API.
- Si se desean recomendar artículos nuevos no presentes en el dataset original, sí se deberá exportar y aplicar el `Scaler`.
- La API maneja errores con códigos HTTP apropiados (`404`, `500`) usando `HTTPException`.

---

## 🧪 Flujo de Ejecución

### Entrenamiento

```bash
python Gen_ModelKNN.py
```

### Ejecución de la API

```bash
uvicorn API:app --reload
```

---

## ✅ Requisitos

- Python 3.8+
- pandas
- scikit-learn
- fastapi
- uvicorn
- joblib

---

## 🧠 Observaciones Finales

- La clase `RecommendKnn` encapsula correctamente todo el flujo: cargar → normalizar → entrenar → exportar.
- El modelo está siendo entrenado con datos consistentes, y el API devuelve recomendaciones reales ajustadas.
- Se ha eliminado el doble escalado, y ahora cada módulo cumple su rol sin ambigüedad.

Este README resume el flujo completo desde el entrenamiento del modelo hasta la exposición vía API. Perfecto para producción ligera o pruebas de concepto.



---

## 🚀 Instrucciones detalladas

### 1. Instalar dependencias

Desde la carpeta `KnnModel/SubSpace/`, ejecutar:

```bash
ScriptInstaller.bat
```

Esto creará un entorno virtual `venv/` e instalará automáticamente las dependencias desde `requirements.txt`.

---

### 2. Entrenar el modelo

Desde `KnnModel/`, ejecutar:

```bash
python Gen_ModelKNN.py
```

Esto:

- Carga los datos desde `Data.xlsx` o `Data.csv`.
- Normaliza las columnas seleccionadas con `MinMaxScaler`.
- Entrena el modelo KNN con `NearestNeighbors`.
- Exporta `Modelo_KNN5.pkl` y `Data.pkl` dentro de `SubSpace/`.

---

### 3. Levantar la API

Desde `KnnModel/SubSpace/`:

#### En CMD:
```cmd
venv\Scripts\activate
uvicorn API:app --reload
```

#### En PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
uvicorn API:app --reload
```

---

### 4. Probar el endpoint

#### URL:
```
http://127.0.0.1:8000/recomendar
```

#### JSON de prueba:
```json
{
  "clave_articulo": 100002
}
```

Incluye una colección de pruebas `BasicTest.json` para usar en Postman con varios casos:

- Artículo válido
- Artículo inexistente
- Parámetros inválidos

---

## 📁 Notas técnicas adicionales

- El modelo se entrena una sola vez y se exporta en `.pkl`.
- La API no necesita reentrenar ni reescalar, solo consumir los `.pkl`.
- El `Scaler` no se exporta porque los datos ya están normalizados.
- El estado `self.ready` en `RecommendKnn` evita errores si el objeto no está correctamente inicializado.
