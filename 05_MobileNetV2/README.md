# MobileNetV2: clasificación foliar para seleccionar el tipo de riego

Modelo de visión artificial integrado en Python para clasificar imágenes en categorías operativas «sana» y «deficiencia» y apoyar la selección entre riego normal y fertirriego.

## Inferencia en la aplicación

- Se recibe una imagen, se convierte a RGB y se redimensiona a **224 × 224 píxeles**.
- El archivo esperado por Python es `mejor_modelo_hojas_finetuning.keras`.
- La salida escalar del modelo se interpreta como probabilidad de «deficiencia».
- Solo se recomienda fertirriego con **probabilidad de deficiencia ≥ 90 %**. En caso contrario, el programa recomienda riego normal.

El preprocesamiento y el orden de clases utilizados durante la evaluación deben coincidir exactamente con los del modelo integrado.

## Datos y etiquetado

Se utilizaron como fuentes de referencia:
- [CoLeaf](https://doi.org/10.17632/brfgw46wzb.1): imágenes de hojas de café con etiquetas de deficiencia nutricional.
- [SoursopBD](https://doi.org/10.17632/hjrhrt5hs8.2): imágenes de hojas de guanábana que incluyen enfermedades, plagas y otros estados foliares.

**Importante:** una etiqueta de plaga o enfermedad en guanábana no equivale por sí sola a deficiencia nutricional. Del mismo modo, las deficiencias de café no verifican diagnóstico nutricional en guanábana. Los resultados se interpretan como clasificación visual sobre las categorías construidas y como apoyo a la decisión simulada.

## Evaluación reproducible

Registrar fuente, especie, etiqueta original, etiqueta final, criterio de agrupación, cantidad de imágenes originales y partición. Dividir por imagen original (o planta, cuando exista ese identificador) **antes del aumento de datos**, sin distribuir derivados entre entrenamiento y prueba.

Reportar matriz de confusión, accuracy, precisión, recall y F1-score sobre un conjunto independiente. Incluir una matriz calculada específicamente con el **umbral operativo de 0,90** y analizar falsos positivos y falsos negativos por clase y fuente.

Los detalles de entrenamiento y validación deben conservarse junto con los scripts, el modelo y las tablas de resultados que sustentan la evaluación.
