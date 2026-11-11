# Guía para evaluar el checkpoint final de MobileNetV2

## Objetivo

Documentar de forma reproducible la evaluación del modelo `mejor_modelo_hojas_finetuning.keras` incluido en el proyecto, sin modificar el código de entrenamiento ni sus pesos.

## Insumos requeridos

- Modelo `.keras` de `05_MobileNetV2/`.
- Imágenes de prueba independientes de entrenamiento y validación (no solo una imagen de demostración).
- [Manifiesto de imágenes](../06_Datos/plantilla_manifest_imagenes.csv) con clase final, especie, fuente y grupo original.
- Entorno compatible con TensorFlow/Keras, Pillow, NumPy, pandas y scikit-learn, con versiones consignadas.

## Validación de independencia

Para cada imagen determinar su identificador de origen, planta o serie de captura. El mismo grupo nunca debe estar distribuido entre entrenamiento y prueba. Considerar imágenes aumentadas y duplicados exactos o visualmente similares. Mantener el conjunto de prueba fuera de cualquier decisión de optimización o selección.

Las etiquetas de CoLeaf (café) y SoursopBD (guanábana con alteraciones fitosanitarias) deben conservar una columna de clase original. Explicar por qué una categoría se asignó a `Sana` o `Deficiencia`, señalando cuándo el mapeo no permite inferir deficiencia nutricional de guanábana.

## Procedimiento analítico

1. Abrir el modelo sin reentrenarlo; usar inferencia sin aumento aleatorio.
2. Cargar todas las imágenes del conjunto de prueba, convertir a RGB y redimensionar a 224 × 224.
3. Entregar al modelo valores RGB de punto flotante en escala 0–255, dado que el script de entrenamiento incluye el preprocesamiento MobileNetV2 dentro de la red.
4. Extraer la salida sigmoide `p_deficiencia` de cada imagen.
5. Evaluar por separado los dos umbrales:
   - **Clasificación convencional 0,50:** clase 1 cuando `p_deficiencia >= 0.50`.
   - **Decisión de fertirriego 0,90:** clase/decisión positiva cuando `p_deficiencia >= 0.90`.
6. Guardar para ambos umbrales la matriz de confusión, accuracy, precision, recall y F1-score, preferiblemente por clase y global.
7. Registrar falsos positivos y falsos negativos con ruta, fuente y categoría original. Analizar su distribución en lugar de optimizar únicamente la exactitud.
8. Publicar script de evaluación, CSV de probabilidades, identificadores de imágenes, manifestación de particiones y versión de las dependencias.

**Convención de matriz:** etiqueta 0 = Sana; etiqueta 1 = Deficiencia. La decisión de fertirriego se considera positiva solamente al alcanzar 0,90.

## Advertencias de interpretación

El `ia_imagen.py` incluido en GitHub calcula métricas del modelo antes del fine-tuning, con umbral 0,50. No atribuir esas cifras al checkpoint final. Las métricas del modelo fine-tuned deben calcularse con una ejecución de evaluación propia sobre el conjunto independiente.

Sin imágenes y manifiesto no es posible establecer el número real de fotografías por fuente, clase y partición, ni evaluar empíricamente el checkpoint.

La clasificación binaria implementada sirve como componente funcional en la simulación; no basta para acreditar diagnóstico nutricional de guanábana.
