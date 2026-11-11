# Resultados y evidencias

Esta carpeta reúne la evidencia cuantitativa y de funcionamiento de los componentes de simulación, control, monitoreo e inteligencia artificial.

## Random Forest

Los reportes deben incluir las cantidades de muestras y trayectorias por conjunto, los parámetros del modelo, el RMSE (en puntos porcentuales de humedad disponible) y una comparación con la persistencia. Se recomienda medir también el error de predicción del instante del siguiente riego (minutos simulados).

La salida guardada en [`RF_Guanaba.ipynb`](../04_Random_Forest/RF_Guanaba.ipynb) corresponde a una prueba de **485 filas** sobre un escenario independiente, con RMSE RF **23,3915** y RMSE de persistencia **0,6709**. El cuaderno la identifica como **NO VALIDADA**. Publicar aquí el CSV `resultados_prueba_random_forest.csv` y el JSON `metricas_random_forest.json` de una ejecución trazable, además de la base que la originó. El `.pkl` de nombre estándar requiere cotejo con esa misma ejecución.

## MobileNetV2

Presentar matriz de confusión, exactitud, precisión, recall y F1-score por clase. El resultado de la decisión operacional de fertirriego debe calcularse con el umbral **0,90**. Analizar los falsos positivos y negativos e indicar la procedencia de las imágenes evaluadas.

## Evidencias de integración

Relacionar capturas y registros con el escenario de simulación, la versión de los programas y el momento simulado de ejecución. Distinguir los resultados de simulación de cualquier validación física o agronómica de campo.

## Convenciones de publicación

Cada tabla y gráfica debe vincularse con sus insumos y scripts de generación. No reutilizar una cifra de evaluaciones anteriores sin indicar la versión de datos, partición y configuración con la que se produjo.
