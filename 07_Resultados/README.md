# Resultados y evidencias

Esta carpeta reúne la evidencia cuantitativa y de funcionamiento de los componentes de simulación, control, monitoreo e inteligencia artificial.

Antes de incorporar capturas o resultados, preparar una copia de la [plantilla de evidencias funcionales](PLANTILLA_EVIDENCIAS_FUNCIONALES.md). No marcar pruebas como aprobadas ni atribuir métricas a un modelo sin registrar la versión, los datos y la ejecución real.

## Integración: evidencia real de ejecución

Se revisaron cinco capturas proporcionadas por el autor. El [reporte de ejecución integrada](EVIDENCIA_EJECUCION_INTEGRADA.md) registra **Factory I/O mostrando conexión OPC DA con 14 símbolos**, **Python indicando comunicación Modbus OK** y **CODESYS conectado con la aplicación en ejecución y SCADA visible**. El informe describe las limitaciones de esta evidencia: las capturas originales aún no se han publicado en el repositorio y faltan pruebas detalladas de señales, compilación y modelos. «Modelo cargado» **no significa** «modelo validado».

## Random Forest

Los reportes deben incluir las cantidades de muestras y trayectorias por conjunto, los parámetros del modelo, el RMSE (en puntos porcentuales de humedad disponible) y una comparación con la persistencia. Se recomienda medir también el error de predicción del instante del siguiente riego (minutos simulados).

La salida guardada en [`RF_Guanaba (1).ipynb`](../04_Random_Forest/RF_Guanaba%20(1).ipynb) utiliza el [Excel publicado](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx): **813 muestras**, 647 de entrenamiento y 163 de prueba cronológica, provenientes de **un solo escenario**. Reporta RMSE RF **0,6144** y RMSE de persistencia **0,1386**. El cuaderno identifica esta evaluación como **NO VALIDADA**. Se guardó un [resumen de los valores visibles](RF_metricas_preliminares_notebook.json), que **no sustituye** el CSV de predicciones ni el JSON exportado por Colab. Falta cotejar la procedencia del `.pkl` publicado y evaluar en escenarios independientes.

## MobileNetV2

Presentar matriz de confusión, exactitud, precisión, recall y F1-score por clase. El resultado de la decisión operacional de fertirriego debe calcularse con el umbral **0,90**. Analizar los falsos positivos y negativos e indicar la procedencia de las imágenes evaluadas.

## Evidencias de integración

Relacionar capturas y registros con el escenario de simulación, la versión de los programas y el momento simulado de ejecución. Distinguir los resultados de simulación de cualquier validación física o agronómica de campo.

## Convenciones de publicación

Cada tabla y gráfica debe vincularse con sus insumos y scripts de generación. No reutilizar una cifra de evaluaciones anteriores sin indicar la versión de datos, partición y configuración con la que se produjo.
