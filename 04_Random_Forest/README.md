# Random Forest: predicción de humedad y próximo riego

Este componente del proyecto utiliza un regresor Random Forest para predecir la humedad disponible del suelo y apoyar la estimación del próximo riego dentro del entorno simulado.

## Entrenamiento nuevo v2 — publicado el 11/11/2026

La versión **[rf-v2](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2)** contiene el nuevo `modelo_prediccion_humedad.pkl` (**53.111.758 bytes**). El [informe verificado](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md) y los [resultados originales](metricas_random_forest.json) confirman el reentrenamiento con los archivos actuales de GitHub:

- **4.552 muestras de entrenamiento** y **922 de prueba** en **13 escenarios** reportados.
- **RMSE Random Forest 0,114327 vs. persistencia 0,172037**: mejora relativa del **33,55 %**.
- **MAE 0,059976 vs. persistencia 0,144368**; **R² 0,999942**.
- En los **cuatro escenarios de prueba** RF supera persistencia; los cuatro pertenecen a una misma sesión.
- El JSON registra `supera_referencia=true` y `apto_para_prueba_en_aplicacion=true`.

Archivos de esta ejecución: [Excel consolidado](Base_guanabana_consolidada_para_RF.xlsx), [CSV de predicciones](resultados_prueba_random_forest.csv), [JSON de métricas](metricas_random_forest.json) y [trazabilidad del Excel](origen_excel_RF.json), además del [cuaderno de Colab](RF_Guanaba_todas_sesiones.ipynb).

**Verificación pendiente:** contrastar el SHA-256 del modelo original producido en Colab con la huella del adjunto de Release `c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`; confirmar que la aplicación carga su contenido y realiza inferencias. Aunque el archivo supera persistencia en esta evaluación, su desempeño frente a una sesión completamente nueva y la exactitud del momento de próximo riego aún no se han acreditado.

## Evaluaciones históricas (no son el modelo rf-v2)

El entrenamiento anterior sobre la base de 3.819 registros obtuvo **RMSE Random Forest 1,7698 vs. 0,6304 de persistencia**, y quedó **NO VALIDADO**. La evaluación aún más antigua con 813 muestras también quedó no validada. Se conservan los [informes históricos](../07_Resultados/RF_INFORME_EVALUACION_BASE_ACTUALIZADA_20261111.md) para trazabilidad, pero **no describen el nuevo modelo publicado en Release**.

## Preparación desde todas las sesiones

**Para volver a entrenar con el Excel actual utiliza el [cuaderno corregido `RF_Guanaba_todas_sesiones.ipynb`](RF_Guanaba_todas_sesiones.ipynb) y las [instrucciones paso a paso](COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md).** La descarga ya no utiliza un commit antiguo ni conserva archivos de ejecuciones anteriores. El cuaderno histórico `RF_Guanaba (1).ipynb` fue retirado del árbol actual; sus resultados se documentan como antecedente histórico.

La versión corregida lee la hoja **`Registro_10min`** del **Excel actualmente publicado en GitHub**, en lugar de leer `Entrenamiento_RF`. El Excel original tenía 2.878 registros brutos y solo 813 muestras preparadas, pero **el archivo fue reemplazado por una versión con más datos**. El cuaderno descarga siempre el archivo de la rama `main` e imprime el nuevo conteo. Construye una base consolidada a partir de todas las sesiones/escenarios, aplicando filtros de continuidad temporal y estado Modbus. La ejecución actual generó **5.474 muestras en total** (4.552 para entrenamiento y 922 para prueba), verificadas en los archivos de métricas y predicciones. No reemplaza automáticamente el `.pkl` en `01_Python`.

## Archivos incorporados

- [`simulador_guanabana_grado_registro_RF.py`](simulador_guanabana_grado_registro_RF.py): copia de la aplicación preparada para registrar y exportar datos en Excel sin modificar `01_Python/Sensores.py`.
- [`RF_Guanaba_todas_sesiones.ipynb`](RF_Guanaba_todas_sesiones.ipynb): notebook actual de entrenamiento con separación por escenarios y comparación con persistencia.
- [Modelo `.pkl` de 53 MB publicado en **GitHub Release `rf-v2`**](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2): la versión actual no está almacenada directamente en la carpeta del repositorio.
- [Revisión de RF v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md): métricas y procedencia de la ejecución actual. [Revisión histórica](REVISION_ENTRENAMIENTO_ACTUAL.md) y [revisión aún anterior](REVISION_ARCHIVOS_Y_RESULTADOS.md) se conservan como antecedentes.

**Evaluación histórica anterior (NO corresponde a rf-v2):** el cuaderno antiguo `RF_Guanaba (1).ipynb` utilizó 813 muestras de una edición previa del Excel (647 para entrenamiento y 163 de prueba). Reportó **RMSE RF 0,6144** y **RMSE persistencia 0,1386**, sin validar. Ese cuaderno y el modelo antiguo se retiraron del árbol del repositorio; la evaluación nueva v2 es la indicada al comienzo del README.

## Separación del entrenamiento y la aplicación

La versión de simulación instalada en `01_Python/Sensores.py` se conserva **sin modificaciones**. En esta carpeta se desarrollan de forma independiente los procesos de preparación de datos, entrenamiento, validación y evaluación del modelo.

**Flujo de trabajo usado por los nuevos archivos:** simulador alternativo → Excel por sesión/escenario (hojas `Registro_10min`, `Entrenamiento_RF`, `Parametros`, etc.) → consolidación trazable de escenarios → entrenamiento y prueba por escenarios completos en Colab → evaluación frente a persistencia → exportación de modelo y métricas. La validación y el uso final requieren un resultado satisfactorio y una prueba independiente.

La copia a `01_Python` debe realizarse únicamente después de comprobar la compatibilidad del paquete y las métricas. No es necesario modificar la interfaz Python, la lógica de CODESYS ni la escena Factory I/O para cambiar el modelo serializado si conserva su interfaz esperada.

El historial de CODESYS se describe como `HistorialCultivo.csv` y contiene columnas `Dia`, `Hora`, `Minuto`, `Temperatura`, `Precipitacion`, `HumedadSuelo`, `NivelAgua`, `NivelNutrientes`, `RiegoActivo` y `TipoRiego`. Como no incorpora un identificador de sesión, los archivos de distintas ejecuciones se deben etiquetar **antes** de construir rezagos, de modo que no se combinen trayectorias discontinuas.

## Archivo de entrada del cuaderno vigente

La salida histórica del cuaderno retirado `RF_Guanaba (1).ipynb` leyó una versión **anterior** de [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx), reemplazada posteriormente. En la versión **histórica** de ese Excel, `Registro_10min` tenía **2.878 registros de tres sesiones**, mientras que el antiguo notebook utilizaba solo **813 muestras de una sesión**. Estas cifras **no deben atribuirse automáticamente al archivo reemplazado** en GitHub. La [revisión del Excel](../06_Datos/REVISION_EXCEL_RANDOM_FOREST.md) explica esta diferencia.

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
