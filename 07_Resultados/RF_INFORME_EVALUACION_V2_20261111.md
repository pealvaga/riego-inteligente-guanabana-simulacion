# Evaluación de Random Forest — entrenamiento v2 y publicación del modelo (11/11/2026)

## Estado verificado en GitHub

La rama `main` contiene el Excel original de entrenamiento y los archivos de la nueva evaluación. El artefacto de modelo se publicó en **[GitHub Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2)** como archivo adjunto, fuera del árbol del repositorio.

| Archivo | Ubicación |
|---|---|
| Excel de origen | [`06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx) |
| Excel consolidado | [`04_Random_Forest/Base_guanabana_consolidada_para_RF.xlsx`](../04_Random_Forest/Base_guanabana_consolidada_para_RF.xlsx) |
| Script reproducible de entrenamiento | [`04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) |
| Métricas originales | [`04_Random_Forest/metricas_random_forest.json`](../04_Random_Forest/metricas_random_forest.json) |
| Predicciones originales | [`04_Random_Forest/resultados_prueba_random_forest.csv`](../04_Random_Forest/resultados_prueba_random_forest.csv) |
| Archivo de procedencia del Excel | [`04_Random_Forest/origen_excel_RF.json`](../04_Random_Forest/origen_excel_RF.json) |
| Modelo RF serializado | [`modelo_prediccion_humedad.pkl` — Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/download/rf-v2/modelo_prediccion_humedad.pkl) |

**Identidad de la base de origen:** Git blob SHA `6b5a285bf66ea871ff190bd191a1220066652440`, idéntico al listado del árbol vigente; tamaño **729.049 bytes**; SHA-256 informado en `origen_excel_RF.json` `5c8618e1ada2a961301c8a4bd21bd671a0ea34cd7d88802909f453a20afc4bd7`. La descarga de Colab se registró el 11/11/2026 a las 20:12:14 UTC.

**Identidad de la Release:** `rf-v2`, publicado el 11/11/2026 a las 20:24:55 UTC, modelo de **53.111.758 bytes**. SHA-256 que publica el servidor GitHub para el adjunto: `c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`. La huella acredita la identidad del archivo *publicado*, pero **todavía no se ha contrastado con una huella del `.pkl` generado localmente en la ejecución de Colab**. Tampoco se ha deserializado para verificar estructura, versiones y compatibilidad con `Sensores.py`.

## Métricas verificadas contra el CSV de 922 predicciones

| Indicador | Random Forest | Persistencia |
|---|---:|---:|
| MAE | **0,05997622** | 0,14436797 |
| RMSE | **0,11432701** | 0,17203679 |
| R² reportado del RF | **0,99994231** | No figura en el JSON |
| Muestras de entrenamiento | 4.552 | — |
| Muestras de prueba | 922 | — |
| Escenarios totales reportados | 13 | — |
| Método de separación | Por escenarios | — |

En el archivo `metricas_random_forest.json` constan `supera_referencia=true` y `apto_para_prueba_en_aplicacion=true`. Se comprobó que las métricas MAE y RMSE pueden reproducirse a partir de las 922 filas del CSV, así como una **reducción relativa del RMSE de 33,55 %** con respecto a persistencia.

### Desglose de escenarios de prueba

Los **922 registros de prueba corresponden a cuatro grupos** de la sesión `20261111_083605` (escenarios 3, 4, 5 y 6). Los recuentos y errores se calcularon desde el CSV publicado.

| Escenario | Registros | RMSE RF | RMSE persistencia | Reducción relativa de RMSE |
|---|---:|---:|---:|---:|
| 3 | 397 | 0,143166 | 0,183375 | 21,93 % |
| 4 | 265 | 0,096905 | 0,177276 | 45,34 % |
| 5 | 122 | 0,104243 | 0,212003 | 50,83 % |
| 6 | 138 | 0,026892 | 0,030332 | 11,34 % |

En los cuatro grupos se observa un RMSE inferior a persistencia. La separación por escenario está implementada en el cuaderno, pero **los cuatro escenarios de prueba son de una misma sesión**. Todavía debe comprobarse la robustez en sesiones o condiciones adicionales completamente nuevas; se trata de simulaciones generadas por el mismo modelo ambiental, no datos reales de campo.

## Estado y controles restantes

**Resultado verificado: el nuevo Random Forest supera persistencia en la evaluación publicada, con partición por escenarios.** Esto constituye evidencia cuantitativa positiva. No equivale automáticamente a validar la estimación del **momento del próximo riego** ni el diagnóstico de campo.

Pendientes:

1. Comprobar que el `.pkl` descargable de Release proviene exactamente de esta ejecución de Colab: comparar SHA-256 de la copia original descargada desde Colab con el SHA-256 publicado para el adjunto.
2. En un equipo confiable y usando el propio archivo generado, comprobar claves `modelo`, `variables`, `paso_minutos=10`, `simulador_modelo_version=balance_hidrico_temperatura_v2`, versión de `scikit-learn` y carga/estimación desde `01_Python/Sensores.py`. Los archivos `joblib/pickle` pueden ejecutar código al abrirse y no deben deserializarse si su origen no es confiable.
3. Realizar una validación adicional con una **sesión nueva reservada para prueba**, sin reajustar el modelo después de verla.
4. Reportar, si se mantiene el objetivo de pronosticar el próximo riego, la diferencia entre su hora real simulada y la estimada, en minutos simulados.
5. Actualizar el texto y tablas del documento de grado a este entrenamiento, sin atribuirle resultados de las evaluaciones históricas.

El informe anterior [`RF_INFORME_EVALUACION_BASE_ACTUALIZADA_20261111.md`](RF_INFORME_EVALUACION_BASE_ACTUALIZADA_20261111.md) permanece en el repositorio como **resultado histórico de un entrenamiento distinto, NO VALIDADO**: RF RMSE 1,7698 frente a persistencia 0,6304. No debe confundirse con `rf-v2`.

No se modificaron `01_Python/Sensores.py`, CODESYS, Factory I/O, los modelos serializados ni los archivos de datos.
