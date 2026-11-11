# Revisión técnica de los archivos Random Forest incorporados

## Artefactos recibidos

| Archivo | Función | Verificación |
|---|---|---|
| [`simulador_guanabana_grado_registro_RF.py`](simulador_guanabana_grado_registro_RF.py) | Copia independiente de la aplicación, con captura y exportación de datos para reentrenamiento | Se revisó el código fuente; no se ha hecho una ejecución con CODESYS |
| [`RF_Guanaba.ipynb`](RF_Guanaba.ipynb) | Notebook de Google Colab que carga un Excel, verifica esquema, separa escenarios, entrena, evalúa y exporta | Se revisó código y salida guardada en el cuaderno |
| [`modelo_prediccion_humedad.pkl`](modelo_prediccion_humedad.pkl) | Artefacto serializado de modelo (23.801.854 bytes) | Se comprobó existencia y tamaño en GitHub; el contenido interno y sus métricas no se han verificado |

El código original [`01_Python/Sensores.py`](../01_Python/Sensores.py), el proyecto CODESYS y la escena Factory I/O no se modificaron como parte de esta revisión.

## Generación de datos

El simulador alternativo conserva la versión declarada de dinámica de suelo `balance_hidrico_temperatura_v2`, paso de muestreo de 10 minutos simulados y los 12 campos esperados por el predictor. Dispone de registro independiente de que haya un modelo `.pkl` cargado. Construye la variable objetivo `HumedadObjetivo_10min` con una observación posterior y exige cuatro lecturas consecutivas a 10 minutos, todas con Modbus válido.

La exportación genera hojas:

- `Registro_10min`: muestras de entrada.
- `Entrenamiento_RF`: entradas con dos rezagos y objetivo a +10 min.
- `EventosRiego`: cambios de estado registrados.
- `ResumenEscenarios`: recuentos y estado de cada escenario.
- `Parametros`: versión del simulador y parámetros.

Al producirse varios archivos de sesiones, se necesita documentar cómo se consolidaron. Se publicó después [`Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx), que contiene 2.878 filas en `Registro_10min` y 813 en `Entrenamiento_RF`. **No es el mismo libro** que el `Base_guanabana_consolidada_para_RF.xlsx` de 2.502 muestras cargado en la ejecución guardada del notebook. Ver [análisis de la nueva base](../06_Datos/REVISION_EXCEL_RANDOM_FOREST.md).

## Configuración del cuaderno RF_Guanaba.ipynb

- Versión requerida: `balance_hidrico_temperatura_v2`.
- Objetivo: humedad a los siguientes **10 minutos simulados**.
- Variables: temperatura, precipitación, humedad del suelo y riego activo; dos rezagos por variable (**12 entradas**).
- Algoritmo: `RandomForestRegressor(n_estimators=300, max_depth=15, min_samples_split=4, min_samples_leaf=2, random_state=42, n_jobs=-1)`.
- Partición: escenarios completos fuera de entrenamiento cuando existen varios; es una separación de **entrenamiento y prueba**, sin conjunto de validación independiente o búsqueda de hiperparámetros en este notebook.
- Referencia: persistencia `HumedadSuelo(t+10) = HumedadSuelo(t)`.
- Exportación: archivo de modelo, `resultados_prueba_random_forest.csv`, `metricas_random_forest.json` y `resultados_RF_guanabana.zip`, según el resultado.

## Resultados documentados en la salida guardada del cuaderno

El notebook presenta los siguientes resultados para la ejecución que contiene en sus salidas:

| Indicador | Valor |
|---|---:|
| Registros del Excel | 2.502 |
| Registros válidos tras validación | 2.502 |
| Sesiones/escenarios completos | 3 |
| Escenario de prueba | `('20261110_185549', 2)` |
| Entrenamiento | 2.017 |
| Prueba | 485 |
| MAE Random Forest | 18,8275 |
| RMSE Random Forest | 23,3915 |
| R² Random Forest | 0,5176 |
| MAE de referencia | 0,2003 |
| RMSE de referencia | 0,6709 |

La ejecución **no superó la referencia de persistencia**, pese a obtener R² positivo; el error de Random Forest fue mucho mayor que la variación a +10 minutos del escenario independiente. El cuaderno imprimió explícitamente:

```text
NO VALIDADO: no reemplaces el modelo actual de la aplicación
```

Según su código, ante tal resultado el notebook guarda un archivo denominado `modelo_prediccion_humedad_NO_VALIDADO.pkl`. En GitHub, en cambio, se encuentra un archivo denominado `modelo_prediccion_humedad.pkl`. **No se debe asumir que el archivo publicado corresponde a la misma ejecución o que sus métricas son satisfactorias sin cotejar el paquete serializado y su procedencia.**

La salida de la ejecución documentada también indica la generación de CSV/JSON/ZIP de resultados, que **no aparecen publicados en `07_Resultados`** en esta revisión.

## Pasos para concluir la reproducibilidad

1. Publicar el Excel consolidado empleado, o enlazarlo con acceso y permisos adecuados; documentar la concatenación de sesiones, el origen y las condiciones de cada escenario.
2. Publicar en `07_Resultados/` el CSV de predicciones y JSON de métricas obtenidos de la misma ejecución; conservar el identificador de la versión del dataset y del modelo.
3. Cotejar el archivo `.pkl` con su procedencia, su esquema interno (`modelo`, `variables`, `paso_minutos`, `simulador_modelo_version`) y los resultados de prueba. **No copiar a `01_Python/` hasta validar su desempeño.**
4. Investigar el fallo de generalización: verificar distribuciones, escenarios y calidad del registro; incorporar escenarios suficientes, y separar entrenamiento, validación y prueba por trayectorias sin solapamiento.
5. Si se requiere demostrar error del **próximo riego** además de humedad, publicar el protocolo y las métricas correspondientes en minutos simulados. Ese resultado no se desprende de la salida actual del notebook.
6. Documentar versiones concretas de dependencias y una ejecución reproducible de principio a fin.

La existencia de los tres nuevos archivos mejora sustancialmente la **disponibilidad del código**. La **reproducibilidad de las cifras** todavía depende del Excel exacto, las métricas exportadas y la validación del artefacto definitivo.
