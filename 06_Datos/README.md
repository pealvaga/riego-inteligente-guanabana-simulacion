# Datos y trazabilidad

Esta sección organiza los conjuntos de datos asociados a la simulación hídrica y a la clasificación visual foliar.

## Actualización del conjunto Random Forest (11/11/2026)

Se reemplazó el [Excel de registros](Datos_entrenamiento_guanabana_20261110_103013.xlsx) por una versión de **729.049 bytes**; su huella Git y SHA-256 constan en el [archivo de origen del reentrenamiento](../04_Random_Forest/origen_excel_RF.json). El [Excel consolidado](../04_Random_Forest/Base_guanabana_consolidada_para_RF.xlsx) se encuentra en `04_Random_Forest/`, junto con las [métricas](../04_Random_Forest/metricas_random_forest.json) y [predicciones](../04_Random_Forest/resultados_prueba_random_forest.csv). Esta ejecución produjo **4.552 muestras de entrenamiento y 922 de prueba**. Las referencias a 813, 2.878, 3.243 o 3.819 registros en los apartados históricos no identifican esta ejecución: consultar el [informe vigente](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md).

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

La hoja `Entrenamiento_RF` de una versión **histórica** del Excel tenía 813 filas, y `Registro_10min` contenía 2.878 registros de tres sesiones. El [nuevo notebook](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) reconstruye las ventanas válidas para todas las sesiones, sin mezclar datos discontinuos y respetando el registro Modbus. El resultado se exporta como `Base_guanabana_consolidada_para_RF.xlsx`, archivo que **ya se publicó en `04_Random_Forest/`** después del reentrenamiento v2.

## Base de registros de Random Forest

Se publicó [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](Datos_entrenamiento_guanabana_20261110_103013.xlsx), **actualmente actualizado a 729.049 bytes**. Las versiones intermedias tuvieron otros tamaños. La edición original tenía 2.878 registros en `Registro_10min` y 813 filas en `Entrenamiento_RF`; **estos conteos son históricos y no representan necesariamente la versión actual**. El nuevo [cuaderno](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) calcula los conteos del archivo vigente. Los datos son compatibles con la versión declarada `balance_hidrico_temperatura_v2`.

El cuaderno histórico ya retirado de GitHub utilizaba una edición previa de ese Excel y lee las **813 filas** de la hoja `Entrenamiento_RF`. Se trata de una **evaluación preliminar y no validada**. El nuevo [`RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) ya se ejecutó y sus resultados se publicaron. La ejecución histórica previa con 2.502 filas y otro Excel no debe confundirse con la actual. Consultar la [revisión técnica del Excel](REVISION_EXCEL_RANDOM_FOREST.md) antes de entrenar o interpretar resultados.
