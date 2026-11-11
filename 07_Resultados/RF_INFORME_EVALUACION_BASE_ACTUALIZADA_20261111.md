# Evaluación del entrenamiento Random Forest con base actualizada — 11 de noviembre de 2026

## Fuente y trazabilidad de la ejecución

Los resultados analizados proceden del archivo `resultados_RF_guanabana.zip`, generado mediante el cuaderno [`RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb). El ZIP contenía cinco elementos:

1. `Base_guanabana_consolidada_para_RF.xlsx`
2. `resultados_prueba_random_forest.csv`
3. `metricas_random_forest.json`
4. `origen_excel_RF.json`
5. **`modelo_prediccion_humedad_NO_VALIDADO.pkl`** (no sustituir el modelo de la simulación).

El registro de origen confirma la descarga de la base vigente de GitHub: `06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx`, rama `main`, **478.235 bytes**, blob SHA GitHub `74a832fd6b1101ff21220526d983ce65e36cb61c`, SHA-256 `73dd7c32d8473993a5523e224578964b7585ccc12171d0cbe0519780b83b3d56`. La descarga quedó fechada en el JSON el 11/11/2026 a las 06:13:25 UTC.

Las cantidades se verificaron revisando las hojas `Registro_10min`, `Entrenamiento_RF` y `ResumenEscenarios` del Excel consolidado y contrastando el JSON de métricas con las **571 predicciones** del CSV. No se ejecutó nuevamente el entrenamiento ni se cargó el archivo `.pkl`.

## Cantidades de datos

| Concepto | Resultado |
|---|---:|
| Registros brutos `Registro_10min` | **3.819** |
| Muestras preparadas `Entrenamiento_RF` | **3.243** |
| Sesiones incluidas en los registros | 4 |
| Grupos sesión/escenario registrados | 11 |
| Grupos con muestras preparadas | 7 |
| Muestras de entrenamiento | **2.672** |
| Muestras de prueba | **571** |
| Método de división reportado | Por escenarios |
| Versión de simulador | `balance_hidrico_temperatura_v2` |
| Objetivo | Humedad disponible a +10 minutos simulados |

La partición mantiene **cuatro grupos completos en entrenamiento** y **tres grupos completos en prueba**, todos los de prueba de la sesión `20261110_221621`, escenarios 4, 5 y 7. No se debe confundir separación de escenarios con una validación de generalización en campo.

## Métricas: Random Forest frente a persistencia

| Métrica | Random Forest | Persistencia (humedad actual) | Mejor |
|---|---:|---:|---|
| MAE (puntos porcentuales) | **0,883139** | **0,294453** | Persistencia |
| RMSE (puntos porcentuales) | **1,769800** | **0,630353** | Persistencia |
| R² (Random Forest) | **0,995743** | No informado en JSON | — |

La referencia de persistencia predice para t+10 la humedad observada en t. En esta prueba, el **RMSE de Random Forest es aproximadamente 2,81 veces el de persistencia**; aunque R² es alto, no supera la referencia operacional.

El JSON registra `supera_referencia=false` y `apto_para_prueba_en_aplicacion=false`. **Resultado: NO VALIDADO**. El nombre del archivo serializado también indica `_NO_VALIDADO.pkl`. No incorporarlo a `01_Python` sin una evaluación posterior satisfactoria y una prueba de compatibilidad.

## Desglose de los tres escenarios de prueba

| Sesión | Escenario | Muestras | RMSE RF | RMSE persistencia | MAE RF | MAE persistencia |
|---|---:|---:|---:|---:|---:|---:|
| `20261110_221621` | 4 | 421 | 0,7872 | **0,1989** | 0,3757 | **0,1854** |
| `20261110_221621` | 5 | 117 | 3,6082 | **1,3351** | 2,8823 | **0,7065** |
| `20261110_221621` | 7 | 33 | 0,3637 | **0,2255** | 0,2688 | **0,2255** |

La persistencia supera a Random Forest en los **tres escenarios**. En el escenario 5 existen predicciones de aproximadamente **88,10 %** cuando el objetivo observado está alrededor de **81,34–81,70 %**, lo que concentra errores importantes. La presencia de esos errores se observa en el CSV: el motivo causal deberá investigarse con los parámetros ambientales y de riego de ese escenario, no inferirse automáticamente.

En el CSV de prueba, la humedad actual mínima es aproximadamente **0,44 %** y el objetivo mínimo a +10 minutos es aproximadamente **0,66 %**; no puede inferirse a partir de ese CSV que el modelo fue evaluado en una muestra con **0,00 % exacto** de agua disponible.

## Implicaciones y próximas acciones

1. **Conservar la nueva base consolidada**: incluye más registros y grupos que el conjunto anterior y permite documentar la preparación de datos. Mantener trazabilidad con `origen_excel_RF.json`.
2. **No sustituir `modelo_prediccion_humedad.pkl`** de la aplicación por el `_NO_VALIDADO.pkl`. El rendimiento fuera de los grupos entrenados sigue siendo inferior a persistencia.
3. Revisar los escenarios con peor desempeño, especialmente el 5, sin utilizar las observaciones de prueba para ajustar el modelo y luego presentarlas como prueba independiente.
4. En un entrenamiento posterior, considerar alternativas que representen el cambio `H(t+10)-H(t)`, ya que la persistencia es una referencia muy exigente para horizontes cortos, y comparar los resultados en **escenarios nuevos** separados.
5. Obtener escenarios con cambios de riego, lluvias y condiciones secas físicamente coherentes; no modificar manualmente las etiquetas para forzar un resultado.
6. Publicar el Excel y los resultados completos, después de revisar el contenido; el presente informe conserva métricas y trazabilidad verificadas pero no sustituye el ZIP original.
7. **Falta evaluar específicamente el error del momento estimado del próximo riego**, distinto del error de humedad a +10 min.

**Conclusión:** la actualización de datos y el entrenamiento en Colab se ejecutaron; la evaluación confirma **más cobertura de datos**, pero **no valida la capacidad predictiva de Random Forest** frente a persistencia. Esto no afecta la compilación y el funcionamiento ya demostrados de Python–CODESYS–Factory I/O.
