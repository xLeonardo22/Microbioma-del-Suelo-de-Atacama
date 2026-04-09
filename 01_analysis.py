## 1. Importación de librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## 2. Carga y exploración del dataset
metadata = pd.read_csv(".../atacama-soil-microbiome/data/raw/sample_metadata.tsv", sep="\t", index_col=0, skiprows=[1])
print(metadata.shape)
print(metadata.head())

## 3. Limpieza de datos
metadata['elevation'] = pd.to_numeric(metadata['elevation'], errors='coerce')
metadata['humidity'] = pd.to_numeric(metadata['average-soil-relative-humidity'], errors='coerce')
metadata = metadata.dropna(subset=['elevation', 'humidity'])
print(f"campioni dopo pulizia: {len(metadata)}")
print(f"Elevazione — min: {metadata['elevation'].min()}m, max: {metadata['elevation'].max()}m")
print(f"Umidità    — min: {metadata['humidity'].min():.2f}%, max: {metadata['humidity'].max():.2f}%")

## 4. Creamos grafica de distribución de muestras
import os
os.makedirs('.../atacama-soil-microbiome/results/figures', exist_ok= True)

fig,axes = plt.subplots(1, 2, figsize = (12,4))
axes[0].hist(metadata['elevation'], bins=15, color='steelblue', edgecolor='white')
axes[0].set_xlabel('Elevación (m)')
axes[0].set_ylabel('Numero muestras')
axes[0].set_title('Distribución muestras por elevación')

axes[1].hist(metadata['humidity'], bins=15, color='seagreen', edgecolor='white')
axes[1].set_xlabel('Humedad media suelo(%)')
axes[1].set_ylabel('Numero muestras')
axes[1].set_title('Distribución muestras por humedad')

plt.tight_layout()
plt.savefig('.../atacama-soil-microbiome/results/figures/sample_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

## 5. Creamos grafica de correlación elevación — humedad
from scipy.stats import spearmanr

r, p = spearmanr(metadata['elevation'], metadata['humidity'])
fig, ax = plt.subplots(figsize = (8, 6))
scatter = ax.scatter(metadata['elevation'], metadata['humidity'],
                     c=metadata['humidity'], cmap='YlOrRd',
                     s=80, edgecolors='k', linewidth=0.5, alpha=0.85)
plt.colorbar(scatter, ax = ax, label = "Humedad (%)")
ax.set_xlabel("Elevación (m)", fontsize = 12)
ax.set_ylabel("Humedad media suelo (%)", fontsize = 12)
ax.set_title(f"Elevación vs Humedad - Atacama Desert\nSpearman r = {r:.2f}, p= {p:.4f}", fontsize = 13)

plt.tight_layout()
plt.savefig('.../atacama-soil-microbiome/results/figures/Comparación.png', dpi = 150, bbox_inches = 'tight')
plt.show()

print(f"Correlazione di Spearman r = {r:.2f}, p = {p:.4f}")
