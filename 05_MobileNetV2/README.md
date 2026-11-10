# MobileNetV2 — clasificación foliar para apoyar el tipo de riego

## Archivos del proyecto

- [`ia_imagen.py`](ia_imagen.py): código del entrenamiento, la primera evaluación y una prueba individual de clasificación. Es un script exportado desde Google Colab.
- [`mejor_modelo_hojas_finetuning.keras`](mejor_modelo_hojas_finetuning.keras): artefacto de modelo final aportado al repositorio (23.704.098 bytes).

El código original y el modelo se conservan sin alteraciones. El nombre del archivo coincide con el checkpoint de fine-tuning configurado en el script. **La presencia del artefacto no constituye, por sí sola, una validación de sus métricas o de su contenido interno.**

## Base de datos de gran tamaño

No es necesario alojar todas las fotografías en GitHub. Se puede mantener el conjunto original en Google Drive o descargarlo desde sus fuentes oficiales, siempre que el acceso y los derechos de uso permitan revisar los datos.

Para generar evidencia verificable sin copiar ni publicar imágenes se incorporó [`generar_inventario_imagenes.py`](generar_inventario_imagenes.py) y la [guía paso a paso para ejecutarlo en Google Colab](COMO_GENERAR_INVENTARIO.md).

El inventario resultante incluye rutas relativas, conteos, tamaños, huellas SHA-256 y campos para fuente, especie, etiqueta original/final y partición. Los campos no verificables permanecen vacíos hasta completarlos con información del conjunto real. El inventario **no** equivale a la evaluación de la IA ni reconstruye automáticamente la partición histórica.

## Entorno y datos de entrada

El script utiliza TensorFlow/Keras, NumPy, Matplotlib, scikit-learn, Pillow y Google Colab. Su ruta de datos está fijada en `/content/drive/MyDrive/IA`; copia el contenido a `/content/IA` y agrupa las imágenes por carpetas:

| Ruta relativa | Etiqueta en el script | Valor |
|---|---|---|
| `IA/Sanas/` y sus subcarpetas | Sana | 0 |
| `IA/Nutrientes/` y sus subcarpetas | Deficiencia | 1 |

El script recorre subcarpetas recursivamente. **No registra la procedencia individual, la especie, la clase original ni las reglas de reclasificación de cada imagen.** Por tanto, esos datos deberán identificarse con un manifiesto verificable del conjunto de imágenes realmente utilizado.

Las fuentes documentadas en el trabajo son [CoLeaf](https://doi.org/10.17632/brfgw46wzb.1) (café) y [SoursopBD](https://doi.org/10.17632/hjrhrt5hs8.2) (guanábana). La clasificación binaria construida a partir de ambas fuentes no demuestra automáticamente un diagnóstico nutricional fiable de guanábana en campo.

## Configuración del entrenamiento, según el script

| Elemento | Valor en `ia_imagen.py` |
|---|---|
| Red base | MobileNetV2, pesos ImageNet, `include_top=False` |
| Entrada | RGB, 224 × 224 × 3 |
| Etiquetado | 0 = Sana, 1 = Deficiencia |
| Partición | 70 % entrenamiento / 15 % validación / 15 % prueba |
| Método de partición | Dos llamadas a `train_test_split`, `stratify` y `random_state=42` |
| Aumento de datos | Giro, reflejo horizontal, zoom y contraste dentro del modelo |
| Salida | Una neurona sigmoide |
| Pérdida | Binary crossentropy |
| Primera fase | Hasta 30 épocas, base congelada, Adam `learning_rate=0.001` |
| Fine-tuning | Hasta 15 épocas, últimas 30 capas de la base habilitadas excepto BatchNormalization, Adam `learning_rate=1e-5` |
| Selección de checkpoint | Mejor `val_loss` |

El preprocesamiento `mobilenet_v2.preprocess_input` está dentro de la red construida. Por ello la aplicación [`Sensores.py`](../01_Python/Sensores.py) envía RGB con valores 0–255, sin aplicar una segunda normalización.

## Lectura académica de los resultados

El código realiza la partición de rutas **antes** del aumento aleatorio de datos; esto reduce el riesgo de filtrar transformaciones generadas en línea a la prueba. No obstante, no se agrupan imágenes por identificador de original, planta o fuente: no es posible descartar copias, variaciones o imágenes correlacionadas en particiones diferentes sin revisar las imágenes y sus metadatos.

El script calcula métricas y matriz de confusión con **umbral de 0,50** sobre el modelo **antes del fine-tuning**. Posteriormente efectúa el fine-tuning y guarda el mejor checkpoint, pero **no se observa una segunda evaluación completa de ese checkpoint sobre el conjunto independiente de prueba**.

El bloque final realiza una prueba de una sola imagen con `UMBRAL = 0.50`. En cambio, [`Sensores.py`](../01_Python/Sensores.py) autoriza fertirriego únicamente si `probabilidad_deficiencia >= 0.90`. Es necesario presentar al docente una matriz de confusión y métricas del checkpoint final **con el umbral operativo de 0,90**, y opcionalmente el umbral estándar de 0,50 a modo de comparación.

Por claridad, no se atribuyen al modelo final métricas que el código calcula antes de la segunda etapa.

## Cómo completar la evaluación sin reentrenar

1. Conservar el modelo original `.keras` y el código de entrenamiento sin modificaciones.
2. Recuperar la organización de imágenes utilizada y elaborar un **manifiesto** con ruta, fuente, especie, etiqueta original/final, grupo de imagen original o planta, partición y criterio de reclasificación.
3. Comprobar que los conjuntos de prueba no compartan originales o variantes con los datos de ajuste; si se detectan filtraciones, generar un conjunto verdaderamente independiente y documentarlo.
4. Cargar `mejor_modelo_hojas_finetuning.keras` con `compile=False`, confirmar su preprocesamiento y obtener probabilidades sobre imágenes de prueba independientes.
5. Reportar matrices de confusión con umbrales **0,50** y **0,90**, junto con accuracy, precision, recall, F1-score y falsos positivos/falsos negativos desglosados por clase y fuente.
6. Guardar scripts, manifiesto, versiones de dependencias y resultados en el repositorio.

Consultar [guía específica para la evaluación final](GUIA_EVALUACION_FINAL.md) y la [plantilla del manifiesto](../06_Datos/plantilla_manifest_imagenes.csv).

## Integración con la simulación

La aplicación espera encontrar el modelo en `01_Python/mejor_modelo_hojas_finetuning.keras`, junto a `Sensores.py`. El archivo en `05_MobileNetV2` es el artefacto documentado de entrenamiento; para ejecutar Python sin modificarlo se debe colocar allí **una copia** del modelo validado.

El umbral 0,90 controla la **decisión de fertirriego** y no debe interpretarse como garantía de fiabilidad diagnóstica.
