import pandas as pd
from scipy.stats import chi2

datos = pd.read_csv("muestra_ech.csv")

datos["ingreso_per_capita"] = datos["ingreso"] / datos["personas_hogar"]

datos["quintil"] = pd.qcut(datos["ingreso_per_capita"], q=5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])

quintil_superior = datos[datos["quintil"] == "Q5"]
print("\nHogares en el quintil superior")
print(f"Cantidad de hogares ricos: {len(quintil_superior)}")

observadas = quintil_superior["departamento"].value_counts().sort_index()
print("\nFrecuencia observada por departamento")
for depto, cantidad in observadas.items():
    print(f"Departamento {depto}: {cantidad} hogares")

cantidad_departamentos = datos["departamento"].nunique()
cantidad_ricos = len(quintil_superior)
esperada = cantidad_ricos / cantidad_departamentos
esperadas = pd.Series([esperada] * cantidad_departamentos, index=observadas.index)
print("\nFrecuencia esperada por departamento (uniforme)")
for depto, valor in esperadas.items():
    print(f"Departamento {depto}: {valor:.2f} hogares esperados")

estadistico_chi2 = ((observadas - esperadas) ** 2 / esperadas).sum()
print("\nEstadístico chi-cuadrado calculado")
print(f"χ² = {estadistico_chi2:.2f}")

valor_critico = chi2.ppf(0.95, df=cantidad_departamentos - 1)
print("\nValor crítico con α = 0.05")
print(f"Grados de libertad: {cantidad_departamentos - 1}")
print(f"Valor crítico: {valor_critico:.2f}")

print("\nConclusión del test:")
if estadistico_chi2 > valor_critico:
    print("Se rechaza la hipótesis nula: la distribución NO es uniforme entre departamentos.")
else:
    print(" No se rechaza la hipótesis nula: la distribución podría ser uniforme.")
