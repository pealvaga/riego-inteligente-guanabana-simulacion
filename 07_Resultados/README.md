# Resultados y evidencias

Esta carpeta reúne la evidencia cuantitativa y de funcionamiento de los componentes de simulación, control, monitoreo e inteligencia artificial.

Antes de incorporar capturas o resultados, preparar una copia de la [plantilla de evidencias funcionales](PLANTILLA_EVIDENCIAS_FUNCIONALES.md). No marcar pruebas como aprobadas ni atribuir métricas a un modelo sin registrar la versión, los datos y la ejecución real.

## Integración: evidencia real de ejecución

Se revisaron **veinte capturas** de la simulación, incluidas tres posteriores con compilación CODESYS (**0 errores, 0 advertencias**), escena virtual y monitorización de GVL. El [reporte de ejecución integrada](EVIDENCIA_EJECUCION_INTEGRADA.md) registra **Factory I/O mostrando conexión OPC DA con 14 símbolos**, **Python indicando comunicación Modbus OK** y **CODESYS conectado con la aplicación en ejecución y SCADA visible**. El informe describe las limitaciones de esta evidencia: las capturas originales **E1–E5 ya están publicadas** en [evidencias_integracion_guanabana/](evidencias_integracion_guanabana/), pero **faltan E6–E20** y faltan pruebas dinámicas de señales y evaluaciones independientes de modelos. Las capturas E9/E10 muestran una transición de **`FO_EMERGENCIA` de FALSE a TRUE**. Las nuevas E11/E12 muestran **salidas de riego en FALSE e indicador rojo en TRUE** durante la emergencia. Las E13–E16 documentan `FO_EMERGENCIA` TRUE→FALSE, salida de riego `FO_Riego2` FALSE→TRUE e indicador verde activo. El chorro de llenado ya no se observa, pero todavía falta verificar la polaridad de `FO_STOP`, las condiciones de rearme y el comportamiento sincronizado de las válvulas. Las E17–E20 muestran ambas salidas de riego desactivadas e indicador amarillo encendido sin emergencia activa. `FO_STOP` aparece TRUE también en la captura anterior, por lo que aún debe verificarse el evento específico de pulsación STOP. «Modelo cargado» **no significa** «modelo validado».

## Random Forest

Los reportes deben incluir las cantidades de muestras y trayectorias por conjunto, los parámetros del modelo, el RMSE (en puntos porcentuales de humedad disponible) y una comparación con la persistencia. Se recomienda medir también el error de predicción del instante del siguiente riego (minutos simulados).

La salida guardada en [`RF_Guanaba (1).ipynb`](../04_Random_Forest/RF_Guanaba%20(1).ipynb) utiliza el [Excel publicado](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx): **813 muestras**, 647 de entrenamiento y 163 de prueba cronológica, provenientes de **un solo escenario**. Reporta RMSE RF **0,6144** y RMSE de persistencia **0,1386**. El cuaderno identifica esta evaluación como **NO VALIDADA**. Se guardó un [resumen de los valores visibles](RF_metricas_preliminares_notebook.json), que **no sustituye** el CSV de predicciones ni el JSON exportado por Colab. Falta cotejar la procedencia del `.pkl` publicado y evaluar en escenarios independientes.

## Resultado preliminar de MobileNetV2

Se revisó una prueba de **100 imágenes** del checkpoint final (50 Sanas, 50 Deficiencia): **accuracy 0,67** a umbral 0,50 y **0,63** a umbral 0,90. En el umbral de fertirriego, la IA detectó **13 de 50 imágenes etiquetadas con deficiencia**. Consultar el [informe preliminar y sus límites de independencia](MobileNetV2/INFORME_PRELIMINAR_20261111.md) y [CSV de métricas agregadas](MobileNetV2/metricas_preliminares_resumen.csv). No se publicaron imágenes individuales. La evaluación definitiva sigue pendiente de corroborar procedencia, etiquetas e independencia del conjunto de prueba.

## Evaluación MobileNetV2: herramientas disponibles

Se publicó un [cuaderno de Colab](../05_MobileNetV2/EVALUAR_MOBILENETV2.ipynb) y [script de evaluación](../05_MobileNetV2/evaluar_checkpoint_final.py) que generan matrices a umbrales 0,50 y 0,90, métricas por clase, probabilidades por fotografía y comprobaciones de duplicados exactos. **Los resultados aún no se han ejecutado ni publicado**. Cuando se disponga de fotografías de prueba con independencia verificable, guardar los archivos generados en `07_Resultados/MobileNetV2/`, siguiendo las [instrucciones](../05_MobileNetV2/COMO_EVALUAR_CHECKPOINT_FINAL.md).

## MobileNetV2

Presentar matriz de confusión, exactitud, precisión, recall y F1-score por clase. El resultado de la decisión operacional de fertirriego debe calcularse con el umbral **0,90**. Analizar los falsos positivos y negativos e indicar la procedencia de las imágenes evaluadas.

## Evidencias de integración

Relacionar capturas y registros con el escenario de simulación, la versión de los programas y el momento simulado de ejecución. Distinguir los resultados de simulación de cualquier validación física o agronómica de campo.

## Convenciones de publicación

Cada tabla y gráfica debe vincularse con sus insumos y scripts de generación. No reutilizar una cifra de evaluaciones anteriores sin indicar la versión de datos, partición y configuración con la que se produjo.
