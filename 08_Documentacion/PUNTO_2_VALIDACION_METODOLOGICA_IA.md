# Punto 2 del docente — partición y evaluación de los modelos de inteligencia artificial

**Estado:** evaluación cuantitativa actualizada de Random Forest disponible y favorable frente a referencia; MobileNetV2 evaluado exploratoriamente sobre un conjunto nuevo de 100 fotografías, **pero independencia y diagnóstico nutricional no acreditados**. No afirmar que las dos IAs quedaron validadas independientemente.

Este informe se refiere exclusivamente al **proyecto de simulación** (Python, CODESYS, Modbus TCP y Factory I/O), sin componente de prototipo físico.

## Requisito que estamos atendiendo

Distinguir datos de entrenamiento y prueba, utilizar métricas apropiadas, conservar las matrices/resultados, identificar los modelos realmente evaluados y declarar límites de independencia, sesgos o cambios de versión. Un archivo del modelo `.pkl` o `.keras` publicado no sustituye esas verificaciones.

## A. Random Forest — humedad a +10 minutos simulados

**Artefacto vigente:** [`rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2). El cuaderno [`RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) forma muestras `X(t)` y `y(t+10)` sin cruzar sesiones/escenarios y utiliza 12 variables: temperatura, precipitación, humedad y riego activo actuales, y dos rezagos de cada variable.

| Medida | Random Forest v2 | Referencia de persistencia |
|---|---:|---:|
| Entrenamiento | **4.552** registros | — |
| Prueba reservada | **922** registros | 922 |
| MAE (p.p.) | **0,059976** | **0,144368** |
| RMSE (p.p.) | **0,114327** | **0,172037** |
| R² (reportado) | **0,999942** | No registrado |
| Reducción relativa del RMSE | **33,55 %** | — |

**Partición:** por grupos completos `(Sesion, Escenario)`, no por registros aleatorios de una misma trayectoria. Sin embargo, los cuatro grupos reservados para prueba son **escenarios 3, 4, 5 y 6 de la misma sesión `20261111_083605`**; esto respalda separación por escenario, **no una validación completamente independiente entre sesiones**. Los cuatro escenarios presentaron menor RMSE que persistencia.

**Prueba complementaria en la interfaz:** 21 pares registrados con separación de **10 minutos simulados entre pronóstico y observación**. A dos decimales: MAE **0,00429 p.p.**, RMSE **0,00655 p.p.**, 12 coincidencias exactas, nueve diferencias de 0,01 p.p.; las humedades observadas se concentraron entre **75,52 % y 76,61 %**. Esta muestra operativa no reemplaza la evaluación de 922 casos ni representa por sí sola diversidad de escenarios.

**Pronóstico del próximo riego:** la captura [E21](../07_Resultados/evidencias_integracion_guanabana/21_rf_v2_pronostico_proximo_riego.png) muestra un cálculo de **Día 3 a las 23:30** con humedad actual 69,61 %, estimación a +10 min de 69,60 % y riego inactivo. Es **evidencia funcional de la salida** y no de la exactitud del instante de activación; **el error temporal todavía no se midió**.

**Para validar con mayor independencia (recomendado):** obtener una **nueva sesión completa no utilizada** para entrenar, con escenarios de lluvia, secado y riego, conservando horas simuladas y estados de actuadores; aplicar `rf-v2` **sin reentrenarlo** y reportar MAE/RMSE y persistencia por escenario. Para el momento del próximo riego, registrar pronóstico emitido y activación real del PLC, calcular diferencia en minutos simulados. No inventar tales observaciones ni adjudicarle las métricas del +10 min a la hora del próximo riego.

**Fuentes de esta auditoría:** [JSON de métricas](../04_Random_Forest/metricas_random_forest.json), [CSV con 922 predicciones](../04_Random_Forest/resultados_prueba_random_forest.csv), [informe estadístico v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md), [21 predicciones observadas](../07_Resultados/RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md).

## B. MobileNetV2 — clasificación foliar y decisión conservadora de fertirriego

**Artefacto:** [`mejor_modelo_hojas_finetuning.keras`](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras). Entradas RGB de 224×224. Clases **Sana** y **Deficiencia**. Umbral operativo para autorizar fertirriego: **probabilidad de Deficiencia ≥0,90**.

La evaluación de un checkpoint de MobileNet sobre **100 capturas** seleccionadas como hojas de guanábana (50 sanas, 50 etiquetadas como deficiencia) produjo:

| Métrica | Umbral 0,50 | Umbral 0,90 (operativo) |
|---|---:|---:|
| Exactitud (accuracy) | **67 %** | **63 %** |
| Sanas correctamente identificadas | **50/50** | **50/50** |
| Deficiencias etiquetadas detectadas | **17/50** | **13/50** |
| Recall de Deficiencia | **34 %** | **26 %** |
| Precisión de Deficiencia en esta muestra | **100 %** | **100 %** |
| Falsos positivos de Deficiencia | **0** | **0** |
| Falsos negativos de Deficiencia | **33** | **37** |

**Matriz de confusión al 0,90** (filas: etiqueta Sana/Deficiencia; columnas: predicción Sana/Deficiencia):

```text
[[50,  0],
 [37, 13]]
```

**Limitación del conjunto:** las 50 fotos etiquetadas como deficiencia se localizaron mediante **Google Imágenes**; no hay comprobación individual de página primaria, licencia, independencia por fotografía original ni diagnóstico nutricional de la hoja. Las 50 fotos sanas se seleccionaron como guanábana, pero tampoco cuentan con toda la trazabilidad original. No se encontraron duplicados de bytes entre prueba e inventario de entrenamiento, pero las capturas de pantalla y recortes podrían ocultar originales repetidos. Por ello se trata de una **prueba exploratoria, no de una validación independiente acreditada**.

**Interpretación defendible:** el clasificador funcionó favorablemente con las **50 hojas etiquetadas como sanas** de la prueba; para hojas etiquetadas como deficientes mostró **sensibilidad baja** y no debe afirmarse que diagnostica deficiencias nutricionales de modo confiable. El umbral **0,90** expresa una **regla conservadora de autorización de fertirriego**, no un «margen de error» ni una validación agrícola. Se recomienda, como mejora futura, una base de fotografías originales de hojas de guanábana con **deficiencias nutricionales confirmadas y fuentes/licencias documentadas**.

**Fuentes:** [informe preliminar del checkpoint](../07_Resultados/MobileNetV2/INFORME_PRELIMINAR_20261111.md), [guía de evaluación](../05_MobileNetV2/COMO_EVALUAR_CHECKPOINT_FINAL.md) e [inventario de imágenes](../06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md).

## C. Cambios imprescindibles en el documento de grado — versión V9(3)

El archivo **`Trabajo de grado V9(3).docx`** conserva resultados antiguos no equivalentes a la nueva evaluación. Los siguientes elementos requieren reconciliación metodológica antes de entregar la versión definitiva:

| Ubicación del documento | Desactualización detectada | Acción propuesta |
|---|---|---|
| **Resumen y Abstract** | RF reportado como RMSE **1,64 y 0,5965**; MobileNet como accuracy **99,70 %** sin delimitar evaluación | Actualizar el **RF vigente** a RMSE **0,1143 vs 0,1720 persistencia**. En MobileNet, separar el **resultado histórico** del ensayo exploratorio del checkpoint: **63 % al 0,90**, dejando claro que independencia y etiquetas no están acreditadas. |
| **3.4.1 Predicción de riego** | RMSE **0,5965**, **199 muestras** y ecuación (25) se presentan como «última prueba» | Conservar esa medición si se necesita como **antecedente**, pero reemplazar «última» por la evaluación **rf-v2 de 922 registros**, con RMSE/MAE y método de partición por escenario. |
| **3.4.1 Proyección de próximo riego** | Presenta cálculo recursivo sin evaluación independiente de error de fecha | Señalar que se mostró una fecha calculada en la interfaz E21, pero **no se midió su error respecto al momento real de activación**. |
| **3.4.2 Modelo de visión artificial** | Matriz con **338 fotos** y cifras **TP=154,TN=183,FP=0,FN=1**, exactitud **99,70 %**, tratadas como desempeño general | Explicar que corresponden a una evaluación **anterior** cuya atribución al checkpoint final e independencia requieren revisión. Presentar aparte la **prueba del checkpoint de 100 capturas** y su matriz 0,90 `[[50,0],[37,13]]`, sin equivalerlas. |
| **Figura 5 y ecuaciones (26)–(29)** | Representan matriz y métricas anteriores; pueden inducir a creer que son el resultado actual al umbral 0,90 | Mantenerlas solo si se titulan claramente como **evaluación histórica**; para el checkpoint actual incluir matriz 100 imágenes y métricas 63 %, 100 % precisión de la clase positiva observada, 26 % recall y F1 ≈ 41,27 %. Revisar numeración y referencias cruzadas. |
| **Conclusiones 5.1** | Afirma los resultados 0,5965 y 99,70 % como desempeño final | Sustituir por cifras actuales con limitaciones de simulación, independencia de datos y sensibilidad foliar. |
| **Anexo C** | No figura en el índice de anexos de la V9(3) | Insertar el [texto final propuesto](TEXTO_PROPUESTO_ANEXO_C.md) después del Anexo B y regenerar tabla de contenido. |

**Precisión:** un **99,70 %** obtenido sobre **338 casos** no puede transferirse automáticamente a otro checkpoint, a otra distribución de imágenes ni al umbral 0,90. Tampoco es correcto sustituirlo silenciosamente sin identificar a qué experimento perteneció. Una redacción defendible presenta **ambos experimentos con su procedencia y alcance** o excluye el histórico de las conclusiones si su trazabilidad es insuficiente.

## D. Estado respecto a las tres observaciones principales

1. **Punto 1 — GitHub y reproducibilidad:** componentes, modelos, bases, 21 capturas, versiones Python y Anexo C listos; el equipo **confirmó la apertura del ZIP CODESYS final**. Faltan solamente la incorporación del Anexo C al Word y, como mejora opcional, una prueba íntegra de instalación desde cero/etiqueta de entrega.
2. **Punto 2 — partición y evaluación de IA:** **avance parcial sustancial**. RF v2 supera persistencia con escenarios separados; MobileNet cuenta con métricas de checkpoint y matriz pero **no independencia acreditada**. Además el trabajo de grado no está actualizado aún.
3. **Punto 3 — etiquetado, procedencia y alcance de las clases:** se documentó Google Imágenes y la necesidad de fotos de deficiencia nutricional verificadas; persisten diagnósticos originales y fuentes individuales sin acreditar. Puede presentarse honestamente como limitación y mejora futura; no declarar confirmación clínica/agronómica.

**Siguiente paso práctico del punto 2:** corregir los apartados **3.4.1, 3.4.2, Resumen/Abstract y 5.1** para que reporten exactamente los ensayos descritos y, si el docente exige validación independiente estricta, elaborar una **prueba con datos nuevos por sesión** y un conjunto foliar con fuente/etiqueta confiable. Mantener las fuentes y cifras históricas como antecedentes, nunca como validación del nuevo checkpoint sin demostración.

Ningún archivo de código/modelo se modificó para producir este informe.
