# Texto propuesto para actualizar el capítulo 3.4 (punto 2 del docente)

> **Material de trabajo para trasladar a `Trabajo de grado V9(3).docx`.** No insertar íntegramente como anexo: adaptar los apartados existentes 3.4.1 y 3.4.2, actualizar las ecuaciones/tablas/figuras y conservar citas bibliográficas originales pertinentes. Los resultados anteriores no deben identificarse como el rendimiento actual del checkpoint final si no se acredita esa equivalencia.

## 3.4.1. Integración y evaluación del modelo predictivo Random Forest

Para apoyar la anticipación de cambios en la humedad del suelo se implementó un modelo de regresión Random Forest, entrenado a partir de registros generados por el simulador ambiental del cultivo de guanábana. La versión actualizada del entrenamiento incorporó escenarios registrados en distintas sesiones, organizados para conservar la continuidad temporal de las mediciones. Se emplearon como variables de entrada la temperatura, la precipitación, la humedad de agua disponible en el suelo y el estado del riego, junto con sus valores correspondientes a uno y dos intervalos anteriores. De este modo, cada predicción se realizó sobre un horizonte de diez minutos simulados.

El modelo se configuró con el algoritmo `RandomForestRegressor` y 300 árboles de decisión, profundidad máxima de 15, tamaño mínimo de división de cuatro muestras y mínimo de dos muestras por hoja. Los datos aptos se separaron por grupos de sesión y escenario, evitando mezclar registros del mismo escenario entre entrenamiento y prueba. La evaluación comprendió **4.552 registros para entrenamiento y 922 para prueba**, procedentes de un total de 13 grupos de sesión/escenario. Los cuatro escenarios reservados para prueba pertenecen a una misma sesión, por lo que se obtuvo separación entre escenarios, pero no una validación completamente independiente entre sesiones.

El desempeño se cuantificó mediante el error absoluto medio (MAE) y la raíz del error cuadrático medio (RMSE), comparando las predicciones del modelo con la humedad simulada diez minutos después y con una referencia de persistencia, que considera que la humedad futura será igual a la actual. Random Forest obtuvo un **MAE de 0,0600 puntos porcentuales y un RMSE de 0,1143 puntos porcentuales**, mientras que la persistencia presentó un **MAE de 0,1444 y un RMSE de 0,1720**. La reducción relativa del RMSE respecto a la referencia fue de **33,55 %**, lo que evidencia una mejora para los escenarios simulados reservados para prueba.

Adicionalmente, durante la operación de la aplicación se realizaron **21 comparaciones** entre las predicciones y las lecturas observadas diez minutos simulados después. Con los datos registrados a dos decimales se obtuvo un MAE de **0,00429** y un RMSE de **0,00655 puntos porcentuales**. Esta comprobación permitió contrastar la salida del modelo con la evolución del simulador, aunque sus observaciones se concentraron en un rango estrecho de humedad, entre 75,52 % y 76,61 %.

La interfaz también utiliza las predicciones para estimar el posible momento del próximo riego, manteniendo en CODESYS la decisión efectiva de activación basada en los umbrales del control. Una captura de funcionamiento mostró un próximo riego estimado para el día 3 a las 23:30, con humedad actual de 69,61 %, predicción a diez minutos de 69,60 % y riego inactivo. Sin embargo, **no se midió todavía el error temporal de esa estimación** frente al momento en que el controlador activaría el riego. En consecuencia, los errores MAE y RMSE reportados corresponden exclusivamente al pronóstico de humedad a diez minutos, no a la precisión de la fecha del próximo riego.

Los resultados validan el uso del modelo dentro de los escenarios de simulación evaluados, sin constituir una verificación directa de condiciones agrícolas reales. La robustez frente a sesiones completamente nuevas deberá verificarse mediante datos adicionales no utilizados para el entrenamiento.

**Tabla sugerida para integrar al apartado (renumerar según el documento):**

| Métrica | Random Forest `rf-v2` | Persistencia |
|---|---:|---:|
| Muestras de prueba | 922 | 922 |
| MAE (p.p.) | 0,05998 | 0,14437 |
| RMSE (p.p.) | 0,11433 | 0,17204 |
| Reducción relativa de RMSE | 33,55 % | — |

**Nota de tabla:** elaboración propia a partir de los 922 registros reservados para prueba del modelo Random Forest `rf-v2`. No representa mediciones en campo.

## 3.4.2. Evaluación del modelo MobileNetV2 para apoyar el tipo de riego

Para apoyar la selección entre riego normal y fertirriego se implementó un clasificador binario basado en MobileNetV2, cuyas salidas corresponden a las categorías **Sana** y **Deficiencia**. Las imágenes se procesan a una resolución de 224 × 224 píxeles. La salida del modelo se utiliza como criterio de apoyo: únicamente cuando la probabilidad asignada a la clase Deficiencia alcanza o supera **el 90 %** se autoriza la selección de fertirriego; en caso contrario se mantiene el riego normal o la decisión definida por las condiciones del controlador. Este umbral es una **regla conservadora de decisión**, no una estimación cuantificada del error ni un diagnóstico definitivo de nutrición vegetal.

El modelo se entrenó utilizando imágenes de los conjuntos CoLeaf y SoursopBD, agrupadas en las dos clases definidas para el proyecto. Como comprobación exploratoria del checkpoint final `mejor_modelo_hojas_finetuning.keras`, se evaluaron **100 imágenes seleccionadas como hojas de guanábana**, distribuidas en 50 imágenes etiquetadas como sanas y 50 como hojas con posibles deficiencias. Las imágenes de la segunda categoría fueron recopiladas mediante Google Imágenes, sin corroboración individual de sus fuentes primarias ni de un diagnóstico nutricional.

Con el umbral de clasificación de **0,50**, el modelo obtuvo una exactitud global de **67 %**. Con el umbral operativo de **0,90**, la exactitud fue de **63 %**. En esta última condición clasificó correctamente **las 50 imágenes etiquetadas como sanas** y **13 de las 50 etiquetadas con deficiencia**. No se observaron falsos positivos de deficiencia en esta muestra, pero **37 imágenes de la clase Deficiencia fueron clasificadas como sanas**, equivalentes a una sensibilidad (*recall*) de **26 %** para esa clase.

La ausencia de falsos positivos en el grupo de hojas sanas representa un resultado favorable bajo las condiciones particulares del ensayo, pero la baja sensibilidad hacia la categoría de deficiencia muestra que el modelo todavía no ofrece una clasificación robusta para alteraciones nutricionales. Además, síntomas como manchas, amarillamiento o necrosis foliar pueden deberse a enfermedades, plagas o estrés ambiental, y no necesariamente a deficiencias de nutrientes.

Por esta razón, la evaluación de 100 imágenes se considera **preliminar**, dado que la independencia respecto de imágenes originales del entrenamiento, las etiquetas nutricionales y las fuentes de las fotografías no se encuentran acreditadas. Como mejora futura se recomienda construir una base específica de hojas de guanábana con fotografías originales, buena calidad visual y diagnósticos nutricionales verificados, con el fin de mejorar el desempeño de clasificación y reducir la incertidumbre de las decisiones de fertirriego.

**Matriz de confusión propuesta para el ensayo del checkpoint final al 90 %:**

| Clase real / predicción | Sana | Deficiencia |
|---|---:|---:|
| Sana | 50 | 0 |
| Deficiencia | 37 | 13 |

**Nota:** elaboración propia con 100 imágenes de una evaluación exploratoria del checkpoint final MobileNetV2; las etiquetas y la independencia de las fotografías no fueron confirmadas externamente. Esta matriz **no equivale** a la matriz histórica de 338 casos y **no debe reemplazarla sin ajustar título, figura y texto**.

## Revisión de los resultados históricos y de las fórmulas

En la V9(3), el experimento histórico de 338 imágenes (TP=154, TN=183, FP=0, FN=1) y **99,70 %** de exactitud figura como resultado del modelo. La evidencia actual del checkpoint final sobre 100 capturas no avala generalizar aquella cifra a la versión actual, al umbral 0,90 ni a fotografías nuevas. Si el resultado histórico se mantiene, debe identificarse explícitamente como **prueba anterior con un conjunto distinto** y explicar su relación exacta con el modelo evaluado; de lo contrario, retirar esa afirmación de las conclusiones sobre la evaluación final.

Las **ecuaciones (22) y (23)** pueden seguir describiendo el promedio de árboles y la estimación del horizonte de riego, siempre que su redacción sea coherente con la implementación. Las **ecuaciones (24) y (25)** del RMSE calculado sobre 535 y 199 casos, respectivamente, corresponden a experimentos anteriores; no deben rotularse como cifras de `rf-v2`. Las **ecuaciones (26)–(29)** y **Figura 5** deben asociarse claramente al conjunto y checkpoint al que corresponden, o actualizarse junto con la matriz y los indicadores del ensayo de 100 imágenes. Regenerar numeración y referencias cruzadas si se insertan o retiran tablas/figuras.

## Sustituciones puntuales para Resumen / Abstract / Conclusiones

### Resumen (fragmento actualizado para reemplazar las cifras antiguas)

Para apoyar la anticipación del riego se entrenó un modelo Random Forest que predice la humedad del suelo a diez minutos simulados. Su evaluación sobre 922 registros de prueba obtuvo un RMSE de **0,1143 puntos porcentuales**, inferior al **0,1720** de una referencia de persistencia. Por otra parte, el modelo MobileNetV2, destinado a apoyar la selección entre riego normal y fertirriego, se evaluó preliminarmente sobre 100 fotografías de hojas seleccionadas como guanábana, con una exactitud global del **63 %** al umbral operativo del 90 %. El modelo clasificó correctamente las 50 hojas etiquetadas como sanas, pero reconoció 13 de las 50 etiquetadas con deficiencia. La evaluación foliar se considera preliminar debido a la falta de verificación independiente del diagnóstico nutricional y de la procedencia de las imágenes.

### Abstract (updated excerpt)

To support irrigation planning, a Random Forest model was trained to predict soil water availability ten simulated minutes ahead. Evaluation on 922 test records yielded an RMSE of **0.1143 percentage points**, outperforming a persistence baseline with an RMSE of **0.1720**. A MobileNetV2 classifier was also evaluated preliminarily using 100 images selected as soursop leaves. At the 90% operational threshold, its overall accuracy was **63%**: all 50 images labeled healthy were classified as healthy, whereas 13 out of 50 images labeled as potentially deficient were detected. These leaf-classification results remain preliminary because the original sources and nutritional diagnoses of the photographs have not been independently verified.

### Conclusiones 5.1 (fragmento actualizado)

La evaluación del modelo Random Forest mostró una mejora del **33,55 %** en el RMSE respecto a una referencia de persistencia para los escenarios reservados de simulación. Esta evidencia respalda su utilización para pronosticar la humedad a diez minutos simulados, aunque no demuestra todavía la precisión temporal del instante estimado del próximo riego ni su generalización a condiciones de campo. En cuanto a MobileNetV2, se observaron resultados favorables en las 50 imágenes etiquetadas como sanas, mientras que la detección de imágenes etiquetadas como deficientes fue limitada, con **26 % de sensibilidad** al umbral del 90 %. Este umbral conserva una función preventiva en la autorización del fertirriego, pero la evaluación requiere mejores datos de origen y diagnósticos nutricionales verificados antes de atribuir al sistema fiabilidad agronómica.

---

**Fuentes para verificar las cifras antes de pegar:** [RF v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md), [21 predicciones](../07_Resultados/RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md), [MobileNetV2 preliminar](../07_Resultados/MobileNetV2/INFORME_PRELIMINAR_20261111.md). No se cambió el código ni los modelos.
