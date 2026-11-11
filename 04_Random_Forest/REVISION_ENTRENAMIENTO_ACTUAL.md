# Revisión de Random Forest — entrenamiento vigente

## Archivos
- Excel [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx).
- Cuaderno [`RF_Guanaba (1).ipynb`](RF_Guanaba%20(1).ipynb).
- Modelo publicado [`modelo_prediccion_humedad.pkl`](modelo_prediccion_humedad.pkl) de **7.610.502 bytes**; falta comprobar que corresponde a esta misma ejecución.

El cuaderno vigente registra que cargó exactamente `Datos_entrenamiento_guanabana_20261110_103013.xlsx`. El libro contiene 2.878 filas en `Registro_10min` procedentes de tres sesiones, pero **813 muestras de una sola sesión y un solo escenario en `Entrenamiento_RF`**, la hoja que consume el cuaderno. Los datos de las otras sesiones no se incluyeron en esta ejecución de entrenamiento.

## Resultados conservados en las salidas del cuaderno

| Indicador | Valor |
|---|---:|
| Muestras válidas | 813 |
| Entrenamiento | 647 |
| Prueba temporal | 163 |
| Escenarios de entrenamiento/validación disponibles | 1 |
| Árboles del bosque | 300 |
| MAE Random Forest | 0,5033 |
| RMSE Random Forest | 0,6144 |
| R² Random Forest | 0,9715 |
| MAE persistencia | 0,1054 |
| RMSE persistencia | 0,1386 |
| Evaluación de la salida | **NO VALIDADO** |

El cuaderno utilizó una partición cronológica con tres filas de separación porque solo encontró un escenario, por lo que la propia ejecución declara que la prueba es **preliminar**. El modelo no supera la predicción por persistencia, aunque el R² sea elevado.

**Advertencia sobre la integración:** el código del notebook exporta `modelo_prediccion_humedad_NO_VALIDADO.pkl` cuando el resultado es preliminar o inferior a persistencia. El fichero de GitHub, sin embargo, tiene el nombre `modelo_prediccion_humedad.pkl`. No debe suponerse que ambos archivos corresponden a la misma ejecución, ni cargar el `.pkl` en `01_Python` antes de comprobar su procedencia, su formato y el desempeño del modelo.

## Pendiente para reproducibilidad y evaluación definitiva

1. Publicar en `07_Resultados` el `resultados_prueba_random_forest.csv` y `metricas_random_forest.json` generados **por la ejecución vigente**, vinculados al modelo y a esta base.
2. Validar la procedencia del `.pkl` publicado, su estructura `modelo`, `variables`, `paso_minutos`, `simulador_modelo_version` y sus métricas, sin ejecutar archivos `.pkl` de origen desconocido.
3. Reconstruir en un módulo **independiente** la tabla de entrenamiento para las otras sesiones a partir de `Registro_10min`; preservar sesiones, continuidad de 10 minutos y validez del registro Modbus.
4. Separar escenarios completos para entrenamiento, validación y prueba, sin mezclar trayectorias; comparar nuevamente con persistencia.
5. Si se presenta pronóstico del próximo riego, evaluar también el error del instante de riego en minutos simulados.

Esta revisión interpreta los archivos y salidas existentes, sin ejecutar nuevo entrenamiento ni modificar la aplicación principal, el PLC o Factory I/O.
