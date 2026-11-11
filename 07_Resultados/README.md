# Resultados y evidencias

Esta carpeta reúne la evidencia cuantitativa y de funcionamiento de los componentes de simulación, control, monitoreo e inteligencia artificial.

Antes de incorporar capturas o resultados, preparar una copia de la [plantilla de evidencias funcionales](PLANTILLA_EVIDENCIAS_FUNCIONALES.md). No marcar pruebas como aprobadas ni atribuir métricas a un modelo sin registrar la versión, los datos y la ejecución real.

**Cierre de pruebas y verificación de modelos:** se reporta ejecución funcional repetida del sistema sin fallas observadas. Los 20 PNG E1–E20 permanecen publicados y el detalle de sus límites se conserva en el informe de integración. Para la prueba específica de carga de Random Forest `rf-v2` en Python existe el [protocolo mínimo de comprobación](PROTOCOLO_VERIFICACION_RF_V2_EN_PYTHON.md): no repetir el entrenamiento, solo registrar carga, inferencia y, de ser posible, una comparación puntual con la humedad real simulada.

## Comparación complementaria de humedad predicha frente a humedad real

Se registraron **21 parejas reportadas de humedad predicha y real** en [el informe de comprobación operativa](RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md) y en su [CSV reproducible](RF_comparacion_operativa_21_pares_20261111.csv). Con valores redondeados a dos decimales: **12 coincidencias exactas**, **9 diferencias de 0,01 puntos porcentuales**, **MAE 0,00429** y **RMSE 0,00655**. Las observaciones están en un intervalo estrecho de humedad (75,52–76,61 %); **se confirmó el intervalo de +10 minutos simulados utilizado entre predicción y observación; no se conservaron marcas de tiempo por fila**. No sustituye el conjunto de **922 pruebas de Colab**.

## Integración: evidencia real de ejecución

Se revisaron **veinte capturas** de la simulación, incluidas tres posteriores con compilación CODESYS (**0 errores, 0 advertencias**), escena virtual y monitorización de GVL. El [reporte de ejecución integrada](EVIDENCIA_EJECUCION_INTEGRADA.md) registra **Factory I/O mostrando conexión OPC DA con 14 símbolos**, **Python indicando comunicación Modbus OK** y **CODESYS conectado con la aplicación en ejecución y SCADA visible**. El informe describe las limitaciones de esta evidencia: las **20 capturas E1–E20 están publicadas** en [evidencias_integracion_guanabana/](evidencias_integracion_guanabana/), pero siguen pendientes las pruebas dinámicas sincronizadas de señales y evaluaciones independientes adicionales de modelos. Las capturas E9/E10 muestran una transición de **`FO_EMERGENCIA` de FALSE a TRUE**. Las nuevas E11/E12 muestran **salidas de riego en FALSE e indicador rojo en TRUE** durante la emergencia. Las E13–E16 documentan `FO_EMERGENCIA` TRUE→FALSE, salida de riego `FO_Riego2` FALSE→TRUE e indicador verde activo. El chorro de llenado ya no se observa, pero todavía falta verificar la polaridad de `FO_STOP`, las condiciones de rearme y el comportamiento sincronizado de las válvulas. Las E17–E20 muestran ambas salidas de riego desactivadas e indicador amarillo encendido sin emergencia activa. `FO_STOP` aparece TRUE también en la captura anterior, por lo que aún debe verificarse el evento específico de pulsación STOP. «Modelo cargado» **no significa** «modelo validado».

## Actualización: Random Forest v2 validado frente a persistencia

El [**informe de la nueva evaluación**](RF_INFORME_EVALUACION_V2_20261111.md) confirma que se publicaron Excel consolidado, métricas originales, CSV de 922 predicciones y trazabilidad del origen en `04_Random_Forest/`, así como el modelo adjunto en [GitHub Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2). Se registraron **4.552 muestras de entrenamiento y 922 de prueba**, **RMSE RF 0,114327** y **RMSE persistencia 0,172037** (reducción del 33,55 %). Esta evaluación **sí supera persistencia** en cuatro escenarios de una misma sesión. La copia local del modelo y su adjunto en GitHub **ya coincidieron en SHA-256**; siguen pendientes la carga funcional en la aplicación y la evaluación del momento del próximo riego.

**Los apartados inferiores de Random Forest son antecedentes de entrenamientos previos no validados; no corresponden a `rf-v2`.**

## Random Forest: entrenamiento con la base ampliada (histórico, NO VALIDADO)

La [evaluación histórica anterior](RF_INFORME_EVALUACION_BASE_ACTUALIZADA_20261111.md) reportó **3.243 muestras aptas**, con 2.672 de entrenamiento y 571 de prueba, y **RMSE Random Forest 1,7698 vs. persistencia 0,6304**, por lo que quedó **NO VALIDADA**. No corresponde al modelo `rf-v2`. El CSV, Excel y `_NO_VALIDADO.pkl` de aquella ejecución histórica no están publicados aquí, pero el CSV/Excel/JSON **de la nueva ejecución rf-v2 sí están disponibles** en `04_Random_Forest/`.

Las cifras del notebook exploratorio de 813 muestras pertenecen a una **evaluación histórica** y no deben presentarse como si procedieran de la nueva base.

## Random Forest

Los reportes deben incluir las cantidades de muestras y trayectorias por conjunto, los parámetros del modelo, el RMSE (en puntos porcentuales de humedad disponible) y una comparación con la persistencia. Se recomienda medir también el error de predicción del instante del siguiente riego (minutos simulados).

El **cuaderno histórico retirado** `RF_Guanaba (1).ipynb` utilizó una versión anterior del Excel: **813 muestras**, 647 para entrenamiento y 163 de prueba cronológica, provenientes de un escenario. Reportó RMSE RF **0,6144** y RMSE persistencia **0,1386**, **NO VALIDADO**. Se conserva un [resumen histórico de sus resultados](RF_metricas_preliminares_notebook.json); el resultado **vigente** está documentado en el [informe rf-v2](RF_INFORME_EVALUACION_V2_20261111.md).

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
