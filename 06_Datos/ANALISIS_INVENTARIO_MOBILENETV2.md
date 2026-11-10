# Auditoría del inventario de imágenes de MobileNetV2

## Identificación del análisis

El inventario se generó en Google Colab, mediante el script [`generar_inventario_imagenes.py`](../05_MobileNetV2/generar_inventario_imagenes.py), sobre la carpeta de Drive `/content/drive/MyDrive/IA` y se compartió como `IA_documentacion-20261110T011717Z-1-001.zip`.

Se revisaron los archivos de metadatos `inventario_imagenes.csv`, `resumen_inventario.json`, `duplicados_exactos.csv` y `errores_lectura.csv`; **las fotografías no fueron transferidas ni inspeccionadas visualmente**. Los resultados describen el estado de las carpetas al generar el inventario y no acreditan que sea exactamente la misma versión utilizada durante el entrenamiento anterior.

## Resultados del inventario

| Indicador | Valor |
|---|---:|
| Archivos de imagen inventariados | 2.247 |
| Clase Sana | 1.220 (54,3 %) |
| Clase Deficiencia | 1.027 (45,7 %) |
| Huellas SHA-256 distintas | 2.173 |
| Pares de archivos exactamente duplicados | 74 |
| Archivos participantes en pares duplicados | 148 |
| Pares duplicados en Sana | 0 |
| Pares duplicados en Deficiencia | 74 |
| Duplicados idénticos entre ambas clases | 0 |
| Archivos con error de lectura | 0 |
| Tamaño total informado por el inventario | 1.711.675.418 bytes (~1,71 GB) |

Los 74 grupos de archivos duplicados tienen dos miembros cada uno. Al retener un representante por hash, quedarían **2.173 imágenes distintas por contenido binario**, de las cuales 1.220 pertenecen a Sana y 953 a Deficiencia.

La verificación SHA-256 solo descubre **duplicados exactos**. Imágenes muy parecidas, distintas tomas de una misma hoja, recortes, rotaciones o versiones exportadas de un mismo original podrían no coincidir en su hash.

## Alcance de la trazabilidad

Las columnas del inventario registran correctamente ruta relativa, clase final, tamaño, hash y carpeta de procedencia dentro del dataset. No obstante, no se rellenaron:

- `fuente` (CoLeaf / SoursopBD u otra);
- `especie`;
- `clase_original`;
- `grupo_original`;
- `particion` (entrenamiento / validación / prueba);
- `criterio_reclasificacion`;
- `licencia_o_referencia`.

Por tanto, **no se pueden atribuir cantidades a CoLeaf y SoursopBD ni construir todavía la tabla definitiva de fuente, especie, clase original y clase final**. Los nombres de archivo no son prueba suficiente de origen o de diagnóstico.

El código original [`ia_imagen.py`](../05_MobileNetV2/ia_imagen.py) define partición estratificada 70 % / 15 % / 15 % con `random_state=42`; sin embargo, el manifiesto no contiene las asignaciones efectivas del entrenamiento realizado. Reproducir la semilla no garantiza recuperar la misma partición si el orden de los archivos cambió.

## Implicaciones para la evaluación

Los **74 pares duplicados** podrían ocasionar fuga de información si miembros de un mismo grupo se distribuyeron entre entrenamiento, validación y prueba. No se ha demostrado que eso haya ocurrido: requiere recuperar el reparto original o construir y justificar un conjunto de prueba independiente.

Se recomienda preservar el modelo entrenado y su código, auditar el conjunto de evaluación, y calcular métricas del checkpoint final con los umbrales **0,50** (clasificación de referencia) y **0,90** (decisión operativa de fertirriego) sin reentrenar en esta etapa.

## Siguientes acciones verificables

1. Subir únicamente los archivos CSV/JSON de metadatos a `06_Datos/` cuando se revisen sus nombres y permisos, manteniendo las fotografías fuera de GitHub.
2. Documentar el mapeo entre la especie, fuente y etiqueta original para cada fotografía, usando la información de los datasets originales o un registro de preparación.
3. Identificar qué imágenes y grupos participaron en el ajuste del modelo y cuáles corresponden a la prueba.
4. Comprobar duplicados cruzados entre particiones y evitar que un original o variantes aparezcan a ambos lados.
5. Ejecutar la evaluación independiente del modelo `.keras` fine-tuned al umbral operativo 0,90 y registrar los resultados por clase y fuente.

**Precaución:** el inventario no es una evaluación del rendimiento de la IA y no contiene una matriz de confusión. Cualquier interpretación de diagnóstico nutricional en guanábana debe ser moderada por las diferencias entre CoLeaf y SoursopBD.
