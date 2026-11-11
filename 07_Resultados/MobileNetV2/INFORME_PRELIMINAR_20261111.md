# Evaluación preliminar del checkpoint final MobileNetV2 — 11 de noviembre de 2026

## Identificación y alcance

Se ejecutó el script [`evaluar_checkpoint_final.py`](../../05_MobileNetV2/evaluar_checkpoint_final.py) sobre el modelo `mejor_modelo_hojas_finetuning.keras`, **sin reentrenarlo ni modificarlo**. El análisis corresponde a un ZIP de resultados de Google Colab y a un conjunto de **100 imágenes etiquetadas**: 50 `Sanas` y 50 `Nutrientes` (clase `Deficiencia`).

- **Estado de esta prueba:** `EVALUACION_PRELIMINAR_INDEPENDENCIA_NO_ACREDITADA`.
- **Checkpoint SHA-256 reportado:** `587883879fc5545dcb8cb4191fedfe042cf9cd13b1d56c91fd58175a38248d59`.
- **Fecha de ejecución UTC indicada por el JSON:** 2026-11-11T05:46:32.474292+00:00.
- **Entorno reportado por Colab:** Python 3.13.18, TensorFlow 2.21.0, scikit-learn 1.6.1, NumPy 2.4.6 y pandas 2.2.3.
- **Entradas:** imágenes RGB 224 × 224, `float32` 0–255, con preprocesamiento interno del modelo.
- **Convención:** etiqueta 0 = Sana; 1 = Deficiencia.

## Métricas observadas

| Métrica | Umbral 0,50 | Umbral 0,90 |
|---|---:|---:|
| Imágenes evaluadas | 100 | 100 |
| Accuracy | **0,67** | **0,63** |
| Precisión clase Deficiencia | 1,00 | 1,00 |
| Recall clase Deficiencia | **0,34** | **0,26** |
| F1 clase Deficiencia | 0,5075 | 0,4127 |
| Verdaderos negativos (Sana→Sana) | 50 | 50 |
| Falsos positivos (Sana→Deficiencia) | 0 | 0 |
| Falsos negativos (Deficiencia→Sana) | **33** | **37** |
| Verdaderos positivos (Deficiencia→Deficiencia) | 17 | 13 |

Matriz de confusión para **umbral 0,50** (filas = clase real Sana, Deficiencia; columnas = predicción Sana, Deficiencia):

```text
[[50,  0],
 [33, 17]]
```

Matriz de confusión para **umbral 0,90** (umbral operativo de fertirriego):

```text
[[50,  0],
 [37, 13]]
```

**Interpretación:** ninguna hoja etiquetada como sana recibió predicción positiva en esta muestra; sin embargo, al umbral operativo 0,90 **37 de 50 hojas etiquetadas con deficiencia se clasificaron como sanas**. Por eso, la precisión positiva 100 % **no implica** detección suficientemente sensible o generalización a campo. El resultado no constituye una validación satisfactoria para diagnóstico nutricional.

## Control de calidad e independencia

El JSON de la ejecución informa:

| Control | Resultado |
|---|---|
| Imágenes Sanas | 50 |
| Imágenes Deficiencia | 50 |
| Duplicados exactos en prueba | **0** |
| Coincidencias de SHA-256 con inventario de entrenamiento | **0** |
| Inventario de entrenamiento disponible | **Sí** |
| Declaración de no participación en entrenamiento/validación | **No** |
| Imágenes con fuente documentada | **0/100** |
| Imágenes con especie documentada | **0/100** |
| Imágenes con clase original documentada | **0/100** |
| Imágenes con identificador de hoja/planta/grupo original | **0/100** |

Los **100 nombres de archivo** del CSV de predicciones comienzan con «Captura de pantalla» y usan `.png`. Por esta razón, la ausencia de coincidencias SHA-256 **no prueba independencia** frente a capturas, recortes o capturas de las mismas imágenes originales. Deben verificarse fuentes, licencias, etiquetas, posibles imágenes correlacionadas y diferencias de composición visual de las capturas.

El conjunto de entrenamiento original usó material de **CoLeaf y SoursopBD** con etiquetas heterogéneas. La clase binaria «Deficiencia» no acredita por sí sola carencias nutricionales concretas de guanábana.

## Procedencia declarada de las imágenes con deficiencia

Las **50 imágenes etiquetadas como `Deficiencia`** para esta prueba se localizaron mediante **Google Imágenes**, según la información de recopilación proporcionada durante la revisión. Google Imágenes es un **buscador**, no necesariamente el creador, propietario ni fuente primaria de las fotografías.

Por ello, **la búsqueda mediante Google Imágenes no acredita las etiquetas de deficiencia nutricional** ni permite identificar automáticamente especie, hoja/planta de origen, sitio de publicación o licencia. Las capturas de pantalla pueden además contener recortes de imágenes usadas previamente en otro conjunto, que no se detectarían mediante coincidencias exactas SHA-256.

Esta información completa el **método de localización** de las 50 imágenes de deficiencia, **pero no llena todavía los campos de fuente original ni valida las etiquetas**. La procedencia de las 50 imágenes sanas permanece sin precisar. Se mantiene el estado **`EVALUACION_PRELIMINAR_INDEPENDENCIA_NO_ACREDITADA`** y las métricas no cambian.

Para fortalecer la evaluación sin recopilar inmediatamente otras 100 fotografías, se recomienda localizar la **página original** de cada captura prioritaria, registrar URL, especie, diagnóstico original y condiciones de uso, y revisar en primer lugar las **37 imágenes con deficiencia clasificadas como sanas** al umbral operativo 0,90. Si un diagnóstico no puede verificarse, registrarlo como **etiqueta no acreditada**; no cambiarlo basándose solamente en la predicción del modelo.

## Especie de las imágenes de prueba

Las **50 fotografías de la clase `Deficiencia` corresponden a hojas de guanábana (`Annona muricata`)**, según la identificación realizada durante la selección de la prueba. Estas imágenes se localizaron mediante Google Imágenes, como se indica en la sección de procedencia.

La identificación de la especie se considera **declarada para esta muestra**, pero todavía no se ha corroborado individualmente mediante las páginas de origen. Asimismo, que una hoja sea de guanábana no confirma que su alteración corresponda a **deficiencia nutricional**: pueden existir otros factores (enfermedades, plagas o estrés ambiental) y errores de etiquetado.

Los resultados cuantitativos **no cambian**: al umbral 0,90 se detectaron **13 de 50** hojas de guanábana etiquetadas con deficiencia y hubo **37 falsos negativos bajo las etiquetas actuales**. Las **50 imágenes sanas** también fueron seleccionadas como guanábana; **sus fuentes originales aún no están documentadas** y la identificación de especie no se ha corroborado fotografía por fotografía. Se mantiene el carácter preliminar de la evaluación.

## Identificación de las dos clases y revisión del ZIP de imágenes

Las **100 imágenes de la prueba (50 en `Sanas` y 50 en `Nutrientes`) fueron seleccionadas como fotografías de guanábana (`Annona muricata`)**. Esta identificación corresponde a la selección de la muestra; sigue pendiente comprobar individualmente la fuente y la etiqueta original de cada fotografía. **No se ha confirmado que todos los casos clasificados como «Deficiencia» correspondan a una carencia nutricional.**

Se examinó el ZIP `Nueva carpeta.zip` proporcionado como material complementario: incluye **50 archivos PNG** en una carpeta general, sin subdivisión de clases y **con 50 huellas SHA-256 distintas**. Las imágenes muestran síntomas visuales como amarillamiento, manchas, lesiones y tejido seco; **estos signos no bastan para distinguir entre deficiencia nutricional, enfermedad, plaga o estrés ambiental**. Se aprecian fotografías con encuadres o contenido muy similares, por lo que la ausencia de hashes idénticos **no acredita que todas correspondan a originales independientes**. El ZIP no se subió a GitHub: es necesario determinar la licencia y la fuente original de cada fotografía.

Estas observaciones no cambian las métricas del modelo ya registradas. El estado de la prueba sigue siendo **preliminar** y los resultados se deben interpretar conforme a las etiquetas utilizadas, no como diagnóstico nutricional certificado.

## Interpretación para la entrega académica

Las 100 imágenes del conjunto de prueba fueron seleccionadas como fotografías de hojas de guanábana. Las 50 clasificadas como deficientes se localizaron mediante Google Imágenes; la fuente y el diagnóstico nutricional original no se han corroborado individualmente.

**Resultado con hojas sanas:** las 50 imágenes etiquetadas como sanas fueron reconocidas como sanas en esta evaluación (**50/50**, sin falsos positivos de deficiencia). Es correcto describir un comportamiento favorable en esa muestra, pero no generalizar a todas las hojas o condiciones de campo.

**Limitación principal:** con el umbral operativo **0,90**, solo **13 de 50** imágenes etiquetadas como deficientes se clasificaron como deficiencia (**recall 26 %**) y **37** se clasificaron como sanas. Algunos síntomas visibles podrían corresponder a enfermedades, plagas u otras causas, no necesariamente a deficiencia nutricional; por ello las etiquetas requieren verificación.

**Criterio de fertirriego:** el programa utiliza un **umbral conservador de 90 %** para considerar suficiente la evidencia del modelo antes de autorizar fertirriego. En este conjunto no hubo falsas detecciones de deficiencia entre las 50 hojas sanas, pero el umbral también provocó una elevada cantidad de deficiencias etiquetadas no detectadas. Se trata de un criterio de decisión configurado, **no de un margen de error medido ni de garantía agronómica**.

**Recomendación:** utilizar en futuras evaluaciones una colección mejor documentada de fotografías de guanábana, con buena nitidez e iluminación, imágenes originales, fuentes y licencias conocidas y **deficiencias nutricionales diagnosticadas de manera confiable**. La evaluación presente se conserva como preliminar y sus cifras no se modifican.

## Acciones recomendadas

1. **Conservar los 100 ejemplos y esta medición** como prueba exploratoria; no modificar cifras ni presentar el 63 % como validación final.
2. Revisar visualmente los **37 falsos negativos** al umbral 0,90 y corregir **únicamente etiquetas demostrablemente erróneas**, dejando registro.
3. Completar el `manifest_prueba.csv` con `fuente`, `especie`, `clase_original`, `grupo_original`, criterio de reclasificación y referencia/licencia.
4. Evaluar similitudes visuales, originales compartidos, composición de capturas de pantalla y posibles solapes con imágenes de entrenamiento.
5. Si se consigue un conjunto **efectivamente independiente y correctamente etiquetado**, repetir el análisis sin adaptar el umbral a las imágenes de prueba. Si no, conservar esta evaluación explícitamente como preliminar y discutir sus limitaciones en el documento.
6. Archivar el ZIP/CSV/JSON completos solo después de verificar privacidad, permisos y trazabilidad de nombres/rutas de imágenes. Este informe publica métricas agregadas, no las fotografías originales.

**Importante:** la integración funcional de Python–CODESYS–Factory I/O se documenta por separado. Un desempeño limitado en detección no invalida la ejecución del sistema simulado, pero impide sostener una eficacia diagnóstica que no se ha observado.
