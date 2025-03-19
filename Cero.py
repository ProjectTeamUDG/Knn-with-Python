import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.preprocessing import StandardScaler
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import classification_report, confusion_matrix
# from imblearn.over_sampling import SMOTE
# from collections import Counter

def leerdatos():
    datos = pd.read_csv('Data.csv')

    muypopular = datos[(datos["TOTAL_ARTICULOS"] >= 20) | (datos["TOTAL_CLIENTES"] >= 10)]
    # popular = datos[(datos["TOTAL_ARTICULOS"] < 20 ) & (datos["TOTAL_ARTICULOS"] >= 10) | (datos["TOTAL_CLIENTES"] < 10) & (datos["TOTAL_CLIENTES"] >= 5) ]
    pocopopular = datos[(datos["TOTAL_ARTICULOS"] < 10) & (datos["TOTAL_CLIENTES"] < 5)]
    # Datos que no estan en muyPopular ni en pocoPopular
    popular = datos[~datos.index.isin(muypopular.index) & ~datos.index.isin(pocopopular.index)]

    total = len(muypopular) + len(popular) + len(pocopopular)
    if total > len(datos):
        print("Error 3 categories are greater than total dataset")
        print(total)
        print(len(datos))
        return -1
    else:
        print(muypopular)
        print(popular)
        print(pocopopular)
    return muypopular, popular, pocopopular

def dibujargrafica(muypopular, popular, pocopopular):
    plt.scatter(muypopular["TOTAL_ARTICULOS"], muypopular["TOTAL_CLIENTES"], marker="^", s=150, color="blue", label="Muy Popular")
    plt.scatter(popular["TOTAL_ARTICULOS"], popular["TOTAL_CLIENTES"], marker="s", s=150, color="green", label="Popular")
    plt.scatter(pocopopular["TOTAL_ARTICULOS"], pocopopular["TOTAL_CLIENTES"], marker="v", s=150, color="red", label="Poco Popular")
    plt.xlabel("TOTAL_ARTICULOS")
    plt.ylabel("TOTAL_CLIENTES")
    plt.show()

def main():
    muypopular, popular, pocopopular = leerdatos()
    dibujargrafica(muypopular, popular, pocopopular)

main()

