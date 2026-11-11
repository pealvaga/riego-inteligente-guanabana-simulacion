# Cómo completar la evaluación final de MobileNetV2 en Google Colab

## Objetivo

Evaluar el **checkpoint posterior al fine-tuning** `mejor_modelo_hojas_finetuning.keras`, sin cambiar sus pesos ni volver a entrenarlo. Generar **accuracy, precision, recall, F1 y matrices de confusión** con el umbral estándar de **0,50** y el umbral de decisión de fertirriego de **0,90**.

[**Abrir directamente el cuaderno de evaluación en Google Colab**](https://colab.research.google.com/github/pealvaga/riego-inteligente-guanabana-simulacion/blob/main/05_MobileNetV2/EVALUAR_MOBILENETV2.ipynb)

## Paso 1. Crear el conjunto de prueba

En Google Drive crear una **carpeta nueva**:

```text
Mi unidad/
  IA_prueba_independiente/
    Sanas/
      imagen_001.jpg
      ...
    Nutrientes/
      imagen_002.jpg
      ...
    manifest_prueba.csv   (opcional durante la ejecución)
```

Usar **fotografías nuevas que nunca participaron en entrenamiento ni validación**, sin duplicados, recortes o variaciones del mismo original que se utilizó antes. Verificar las etiquetas verdaderas; no inferirlas a partir de la propia IA.

**NO copiar directamente `IA/Sanas` y `IA/Nutrientes` a esa carpeta:** son parte del conjunto utilizado para el entrenamiento previo. El script original dividió las 2.247 imágenes en 70 %/15 %/15 %, pero no guardó una lista de las rutas o grupos originales efectivamente asignados a cada partición. Volver a ejecutar `train_test_split(random_state=42)` no garantiza reconstruir la partición histórica, porque `os.walk` no fija un orden de archivos y el dataset puede haber cambiado desde el entrenamiento.

**Si se conserva un manifiesto histórico de `rutas_test` de la ejecución del entrenamiento**, también es posible evaluar esas imágenes, siempre que se demuestre que nunca participaron en train/val y que no comparten imagen/planta de origen. Si no se dispone de ese manifiesto, el procedimiento recomendado es crear un conjunto nuevo e independiente.

Las clases del proyecto son **`Sanas` = 0** y **`Nutrientes` = 1 (Deficiencia)**. La segunda denominación procede del entrenamiento original y puede agrupar alteraciones que no son carencias nutricionales; **no confundir el resultado del clasificador con una determinación agronómica de nutrientes en guanábana**.

## Paso 2. Registrar procedencia de las imágenes

Opcional para **ejecutar** el cuaderno, pero necesario para la **trazabilidad académica final**: crear dentro de `IA_prueba_independiente` un CSV llamado `manifest_prueba.csv`, con estas columnas:

```csv
archivo,fuente,especie,clase_original,grupo_original,criterio_reclasificacion,licencia_o_referencia
```

- `archivo`: ruta relativa, por ejemplo `Sanas/foto_001.jpg`, **exactamente** como el nombre del archivo en Drive.
- `fuente`: conjunto original, captura propia o publicación autorizada.
- `especie`: especie real fotografiada, no asumir siempre `Annona muricata`.
- `clase_original`: condición original con respaldo, antes de reunir clases.
- `grupo_original`: identificador de hoja, planta o fotografía de origen; nunca debe repetirse entre ajuste y prueba.
- `criterio_reclasificacion`: justificación para pasar a Sana o Deficiencia.
- `licencia_o_referencia`: licencia y enlace de procedencia cuando correspondan.

Los campos de procedencia faltantes se informarán como no documentados, no se rellenarán con valores supuestos.

## Paso 3. Ejecutar el cuaderno

1. Abrir [`EVALUAR_MOBILENETV2.ipynb`](EVALUAR_MOBILENETV2.ipynb) en Colab desde el enlace anterior.
2. Conectar Google Drive en la primera celda.
3. Revisar `CARPETA_PRUEBA`, `MODELO_DRIVE`, `INVENTARIO_ENTRENAMIENTO` y `SALIDA`. Si el modelo no está en Drive, el cuaderno descarga el `.keras` publicado en este repositorio.
4. `CONFIRMO_IMAGENES_NO_USADAS` debe quedar `False` hasta que se haya verificado documentalmente que las fotografías son realmente independientes; entonces puede cambiarse a `True`.
5. Ejecutar todas las celdas y comprobar las tablas y las dos matrices de confusión.
6. Descargar `evaluacion_mobilenetv2_checkpoint.zip`.

Se usa el mismo procesamiento del entrenamiento: `tf.io.decode_image`, RGB, `tf.image.resize(224,224)`, `float32` **sin normalizar previamente** porque `mobilenet_v2.preprocess_input` ya forma parte de la arquitectura. Se carga el checkpoint con `compile=False` y se evalúa en modo inferencia, sin aumentos aleatorios.

Si la carpeta de prueba no existe, o faltan una de las dos clases, la ejecución se detiene con un mensaje que permite corregirla.

## Paso 4. Interpretar y publicar resultados

El script [`evaluar_checkpoint_final.py`](evaluar_checkpoint_final.py) genera fuera de la carpeta de prueba:

| Archivo | Contenido |
|---|---|
| `metricas_mobilenetv2.json` | Métricas por clase, matriz numérica, umbrales, versiones, huella del checkpoint y estado de independencia |
| `metricas_resumen.csv` | Comparación accuracy / precision / recall / F1 entre 0,50 y 0,90 |
| `matriz_confusion_05.png` | Sana / Deficiencia con umbral 0,50 |
| `matriz_confusion_09.png` | Sana / Deficiencia con umbral 0,90 |
| `predicciones_mobilenetv2.csv` | Ruta relativa, etiqueta real, probabilidad, clasificación y metadatos |
| `resultados_por_fuente.csv` | Exactitud desglosada por fuente, cuando el manifiesto contiene ese campo |
| `duplicados_en_prueba.csv` | Copias exactas dentro del nuevo conjunto |
| `solapes_con_entrenamiento.csv` | Coincidencias exactas con el inventario de las 2.247 imágenes de entrenamiento |
| `evaluacion_mobilenetv2_checkpoint.zip` | Todos los resultados anteriores, sin fotos |

**Solo cuando la independencia de la prueba, las etiquetas y los grupos de origen sean comprobables**, utilizar las métricas como evaluación del modelo final. Aunque no haya coincidencias SHA-256, pueden existir fotos aumentadas o similares de la misma hoja o planta; la verificación no es automática.

Los resultados se deben colocar en `07_Resultados/MobileNetV2/`. No introducir fotografías de terceros en GitHub si su licencia no lo permite. El ZIP sí permite revisar métricas y trazabilidad sin almacenar las imágenes originales.

## Qué podremos afirmar en el documento

- Número de imágenes y distribución por clase de **la prueba independiente**.
- Modelo y huella SHA-256 evaluados.
- Umbral 0,50 para clasificación estándar y 0,90 para decisión operativa.
- Accuracy, precision, recall, F1 y matriz de confusión para ambos umbrales.
- Falsos positivos y falsos negativos del proceso de decisión.
- Limitaciones del etiquetado heterogéneo (CoLeaf/SoursopBD), independencia y generalización a guanábana.

No declarar exactitud del checkpoint final antes de ejecutar las celdas y revisar los archivos generados.
