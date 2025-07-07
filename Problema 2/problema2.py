import pandas as pd
import numpy as np
from scipy.stats import t

# 1. Cargar datos
datos = pd.read_csv("Problema 2/velocidad_internet_ucu.csv")

# 2. Filtrar solo Central y Semprún
datos_central = datos[datos['Edificio'] == 'Central']['Velocidad Mb/s']
datos_semprun = datos[datos['Edificio'] == 'Semprún']['Velocidad Mb/s']

# 3. Estadísticos descriptivos
media_central = datos_central.mean()
media_semprun = datos_semprun.mean()
std_central = datos_central.std(ddof=1)  # ddof=1 para varianza muestral
std_semprun = datos_semprun.std(ddof=1)
n_central = len(datos_central)
n_semprun = len(datos_semprun)

print(f"Central: n = {n_central}, Media = {media_central:.2f} Mbps, Desviación = {std_central:.2f}")
print(f"Semprún: n = {n_semprun}, Media = {media_semprun:.2f} Mbps, Desviación = {std_semprun:.2f}")

# 4. Prueba t (varianzas desiguales)
numerador = media_central - media_semprun
denominador = np.sqrt((std_central**2 / n_central) + (std_semprun**2 / n_semprun))
t_estadistico = numerador / denominador

# 5. Grados de libertad 
df_numerador = ((std_central**2 / n_central) + (std_semprun**2 / n_semprun))**2
df_denominador = ((std_central**2 / n_central)**2 / (n_central - 1)) + ((std_semprun**2 / n_semprun)**2 / (n_semprun - 1))
df = df_numerador / df_denominador

# 6. p-valor (prueba unilateral inferior: H1: Central < Semprún)
p_valor = t.cdf(t_estadistico, df=df)

# 7. Resultados
alpha = 0.05
print(f"\nEstadístico t = {t_estadistico:.4f}")
print(f"Grados de libertad (df) = {df:.2f}")
print(f"p-valor = {p_valor:.4f}")

if p_valor < alpha:
    print("\nRechazamos H₀: La velocidad en Central es significativamente menor que en Semprún (p < 0.05).")
else:
    print("\nNo rechazamos H₀: No hay evidencia suficiente para afirmar que Central sea más lento (p ≥ 0.05).")