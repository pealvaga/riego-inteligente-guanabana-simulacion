# Random Forest: predicción de humedad y próximo riego

Este componente del proyecto utiliza un regresor Random Forest para predecir la humedad disponible del suelo y apoyar la estimación del próximo riego dentro del entorno simulado.

## Corrección: usar los registros de las tres sesiones

**Para volver a entrenar con el Excel publicado utiliza el [cuaderno corregido `RF_Guanaba_todas_sesiones.ipynb`](RF_Guanaba_todas_sesiones.ipynb) y las [instrucciones paso a paso](COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md).** El cuaderno anterior `RF_Guanaba (1).ipynb` se conserva como registro del entrenamiento exploratorio de 813 muestras.

La versión corregida lee la hoja **`Registro_10min`** con 2.878 registros en lugar de leer `Entrenamiento_RF` con 813. Construye una base consolidada a partir de todas las sesiones/escenarios, aplicando filtros de continuidad temporal y estado Modbus. La cantidad final de muestras válidas y las métricas **aún no se han calculado con el nuevo cuaderno**. No reemplaza automáticamente el `.pkl` en `01_Python`.

## Archivos incorporados

- [`simulador_guanabana_grado_registro_RF.py`](simulador_guanabana_grado_registro_RF.py): copia de la aplicación preparada para registrar y exportar datos en Excel sin modificar `01_Python/Sensores.py`.
- [`RF_Guanaba (1).ipynb`](RF_Guanaba%20(1).ipynb): notebook de entrenamiento con separación de escenarios y comparación con persistencia.
- [`modelo_prediccion_humedad.pkl`](modelo_prediccion_humedad.pkl): modelo publicado; la procedencia y las métricas específicas de este artefacto deben verificarse antes de desplegarlo.
- [Revisión del entrenamiento vigente](REVISION_ENTRENAMIENTO_ACTUAL.md): confirma el Excel empleado, las métricas y el estado preliminar. La [revisión anterior](REVISION_ARCHIVOS_Y_RESULTADOS.md) se conserva como antecedente histórico.

**Estado actual de evaluación:** el cuaderno `RF_Guanaba (1).ipynb` registra **813 muestras del Excel publicado**, con 647 para entrenamiento y 163 para prueba cronológica. Reporta **RMSE RF 0,6144 y RMSE de persistencia 0,1386**: resultado **NO VALIDADO**. Debido a que la hoja `Entrenamiento_RF` contiene un único escenario, la prueba es exploratoria. **No se ha verificado que el `.pkl` de nombre estándar sea el producto de esa ejecución.** No copiarlo a la aplicación hasta validarlo.

## Separación del entrenamiento y la aplicación

La versión de simulación instalada en `01_Python/Sensores.py` se conserva **sin modificaciones**. En esta carpeta se desarrollan de forma independiente los procesos de preparación de datos, entrenamiento, validación y evaluación del modelo.

**Flujo de trabajo usado por los nuevos archivos:** simulador alternativo → Excel por sesión/escenario (hojas `Registro_10min`, `Entrenamiento_RF`, `Parametros`, etc.) → consolidación trazable de escenarios → entrenamiento y prueba por escenarios completos en Colab → evaluación frente a persistencia → exportación de modelo y métricas. La validación y el uso final requieren un resultado satisfactorio y una prueba independiente.

La copia a `01_Python` debe realizarse únicamente después de comprobar la compatibilidad del paquete y las métricas. No es necesario modificar la interfaz Python, la lógica de CODESYS ni la escena Factory I/O para cambiar el modelo serializado si conserva su interfaz esperada.

El historial de CODESYS se describe como `HistorialCultivo.csv` y contiene columnas `Dia`, `Hora`, `Minuto`, `Temperatura`, `Precipitacion`, `HumedadSuelo`, `NivelAgua`, `NivelNutrientes`, `RiegoActivo` y `TipoRiego`. Como no incorpora un identificador de sesión, los archivos de distintas ejecuciones se deben etiquetar **antes** de construir rezagos, de modo que no se combinen trayectorias discontinuas.

## Archivo de entrada del cuaderno vigente

La salida guardada en `RF_Guanaba (1).ipynb` confirma la lectura de [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx), ya disponible en `06_Datos`. Su hoja `Registro_10min` tiene **2.878 registros de tres sesiones**, pero la hoja `Entrenamiento_RF` usada por el notebook incluye **813 muestras de una sola sesión**. La [revisión del Excel](../06_Datos/REVISION_EXCEL_RANDOM_FOREST.md) explica esta diferencia.

La evaluación anterior con otro Excel consolidado de 2.502 muestras se conserva como antecedente histórico en [REVISION_ARCHIVOS_Y_RESULTADOS.md](REVISION_ARCHIVOS_Y_RESULTADOS.md), pero **no debe presentarse como resultado de la ejecución vigente**.

## Datos y variables

Las entradas emplean cuatro señales: temperatura, precipitación, humedad del suelo y riego activo, más dos rezagos temporales para cada señal. El paso de predicción es de **10 minutos simulados**.

El conjunto de entrenamiento debe generarse con la misma dinámica hídrica implementada en el simulador de referencia. En la aplicación Python, la versión correspondiente se identifica como `balance_hidrico_temperatura_v2`.

## Partición y metodología de evaluación

1. Identificar cada trayectoria o sesión de simulación y mantener sus muestras agrupadas.
2. Respetar el orden cronológico y separar entrenamiento, validación y prueba, sin usar registros futuros en el entrenamiento.
3. Ajustar hiperparámetros y seleccionar el estimador utilizando únicamente los conjuntos permitidos para desarrollo.
4. Evaluar una sola vez el modelo definitivo sobre datos independientes.
5. Comparar el pronóstico a 10 minutos con una **línea base de persistencia**.
6. Evaluar el error de estimación del siguiente momento de riego, en minutos simulados.

Las métricas se deben presentar junto con cantidades de registros, sesiones, fechas o intervalos simulados, versión del generador, hiperparámetros y semilla aleatoria.

## Integración con Python

El archivo `modelo_prediccion_humedad.pkl` utilizado por [Sensores.py](../01_Python/Sensores.py) debe contener al menos:
- `modelo`: regresor entrenado compatible con `predict`.
- `variables`: nombres y orden de las 12 variables.
- `simulador_modelo_version`: `balance_hidrico_temperatura_v2`.
- `paso_minutos`: `10`.

La inferencia permite anticipar el siguiente riego, pero **no reemplaza la activación basada en la humedad y el control por histéresis implementado en CODESYS**.

## Reproducción de resultados

Para sustentar las métricas académicas, el conjunto de datos, los scripts de preparación, entrenamiento y evaluación y el modelo final deben asociarse mediante identificadores de versión y configuración. Consultar [guía de verificación](../08_Documentacion/ESTADO_REPRODUCIBILIDAD.md).
