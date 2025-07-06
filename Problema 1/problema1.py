import pandas as pd
from scipy.stats import chi2

datos = pd.read_csv("muestra_ech.csv") 

datos["ingreso_per_capita"] = datos["ingreso"] / datos["personas_hogar"]

datos["quintil"] = pd.qcut(datos["ingreso_per_capita"], q=5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])

quintil_superior = datos[datos["quintil"] == "Q5"]

observadas = quintil_superior["departamento"].value_counts().sort_index()

cantidad_departamentos = datos["departamento"].nunique()
cantidad_ricos = len(quintil_superior)
esperada = cantidad_ricos / cantidad_departamentos
esperadas = pd.Series([esperada] * cantidad_departamentos, index=observadas.index)

estadistico_chi2 = ((observadas - esperadas) ** 2 / esperadas).sum()

valor_critico = chi2.ppf(0.95, df=cantidad_departamentos - 1)

print("Estadístico chi-cuadrado:", estadistico_chi2)
print("Valor crítico (α = 0.05):", valor_critico)

if estadistico_chi2 > valor_critico:
    print("Se rechaza la hipótesis nula: la distribución NO es uniforme.")
else:
    print("No se rechaza la hipótesis nula: la distribución podría ser uniforme.")
