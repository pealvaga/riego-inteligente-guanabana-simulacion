# Datos y trazabilidad

Esta sección organiza los conjuntos de datos asociados a la simulación hídrica y a la clasificación visual foliar.

## Registros de simulación

Cada trayectoria debe conservar su identificador de sesión, origen, condiciones iniciales y variables registradas. Para el pronóstico de humedad se utilizan temperatura, precipitación, humedad disponible y estado de riego, con intervalos de 10 minutos simulados. Es importante distinguir datos de entrenamiento y datos independientes de prueba.

## Bases de imágenes

Fuentes citadas en el documento académico:

- **CoLeaf:** https://doi.org/10.17632/brfgw46wzb.1
- **SoursopBD:** https://doi.org/10.17632/hjrhrt5hs8.2

La trazabilidad requiere registrar especie, clase original, clase agrupada, justificación, cantidad de imágenes originales y su distribución en entrenamiento, validación y prueba.

La división por grupos de imágenes originales debe realizarse antes del aumento de datos. No redistribuir imágenes de terceros sin comprobar su licencia.

## Esquema recomendado de particiones

Para Random Forest: separar trayectorias y mantener el orden temporal. Para MobileNetV2: dividir por imagen original o planta identificada y evitar versiones aumentadas del mismo original en conjuntos diferentes.

Conservar la manifestación de las particiones y sus semillas, para reconstruir exactamente la evaluación que se presente en el documento de grado.

## Inventario ligero de MobileNetV2

No es necesario distribuir las fotografías en este repositorio para documentar el conjunto de entrenamiento. La [guía de inventario de MobileNetV2](../05_MobileNetV2/COMO_GENERAR_INVENTARIO.md) permite calcular un manifiesto CSV, conteos por clase/subcarpeta y duplicados exactos directamente sobre la carpeta de Google Drive.

Después de comprobar procedencia, clases y licencias, se deben conservar en esta carpeta los archivos de metadatos y las particiones verificables. Un resumen por carpetas no basta para demostrar que la prueba sea independiente por imagen original, y el resultado de inventario no sustituye una evaluación del modelo final.

## Resultados cuantitativos del inventario de imágenes

Se revisó un inventario de **2.247 imágenes** (1.220 Sana y 1.027 Deficiencia). Se encontraron **74 pares de archivos exactamente duplicados**, todos dentro de la clase Deficiencia, lo que deja 2.173 hashes SHA-256 distintos. No hubo errores de lectura. Los campos de origen, especie, etiqueta original y partición permanecen sin verificar.

Consultar el [análisis del inventario](ANALISIS_INVENTARIO_MOBILENETV2.md) y el [resumen en JSON](resumen_inventario_mobilenetv2.json). Estos registros no sustituyen las imágenes originales ni los resultados de evaluación independientes.

## Preparación completa de las sesiones para Random Forest

La hoja `Entrenamiento_RF` del Excel original tiene 813 filas, pero `Registro_10min` contiene 2.878 registros de tres sesiones. El [nuevo notebook](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) reconstruye las ventanas válidas para todas las sesiones, sin mezclar datos discontinuos y respetando el registro Modbus. El resultado se exporta como `Base_guanabana_consolidada_para_RF.xlsx`, archivo que se podrá publicar aquí después de ejecutar el cuaderno.

## Base de registros de Random Forest

Se publicó [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](Datos_entrenamiento_guanabana_20261110_103013.xlsx). La hoja `Registro_10min` contiene **2.878 registros y tres identificadores de sesión**, mientras que `Entrenamiento_RF` tiene **813 filas correspondientes solo a la primera sesión**. Los datos son compatibles con la versión declarada `balance_hidrico_temperatura_v2`.

La ejecución archivada en `RF_Guanaba.ipynb` utilizó otro libro, `Base_guanabana_consolidada_para_RF.xlsx`, con **2.502 filas**; por tanto, el Excel publicado no reproduce directamente esa evaluación. Consultar la [revisión técnica del Excel](REVISION_EXCEL_RANDOM_FOREST.md) antes de entrenar o interpretar resultados.
