# Comprobación complementaria de 21 predicciones de humedad — 11/11/2026

## Datos comunicados y alcance

Se registran **21 parejas de valores de humedad predicha y humedad real** proporcionadas durante la revisión funcional del proyecto. Se informaron con **dos decimales**. **Aclaración del procedimiento:** se confirmó que cada humedad real se anotó **10 minutos simulados después** de que se mostró la humedad predicha; se registraron y compararon sucesivamente cada 10 minutos simulados. Por tanto, las 21 parejas **sí representan el pronóstico a +10 minutos bajo la secuencia declarada**. No obstante, la tabla no incluye marcas de tiempo individualizadas, identificadores de escenario ni capturas que acrediten externamente cada transición; se conserva como comprobación funcional complementaria, no como conjunto independiente de evaluación estadística.

La tabla numérica reproducible está en [`RF_comparacion_operativa_21_pares_20261111.csv`](RF_comparacion_operativa_21_pares_20261111.csv). Cada fila mantiene el orden de entrega.

## Métricas calculadas sobre los valores redondeados

| Indicador | Resultado |
|---|---:|
| Pares comparados | **21** |
| Diferencia cero a dos decimales | **12** |
| Diferencia absoluta de 0,01 puntos porcentuales | **9** |
| MAE | **0.00428571 puntos porcentuales** |
| RMSE | **0.00654654 puntos porcentuales** |
| Error absoluto máximo | **0,01 puntos porcentuales** |
| Humedad real mínima observada | **75,52 %** |
| Humedad real máxima observada | **76,61 %** |

**Fórmulas:** `error_i = predicción_i - observado_i`; `MAE = (1/n) × suma(|error_i|)`; `RMSE = raíz(suma(error_i²)/n)`.

### Interpretación

Las 21 estimaciones presentan **concordancia muy cercana** con las lecturas emparejadas. No obstante, se trabaja con datos **redondeados a 0,01 %** y variaciones de humedad en un intervalo reducido alrededor de **75,52–76,61 %**. Esto **no prueba precisión general** para umbrales cercanos a 60 %, sequía, precipitación, riego activo u otras sesiones. Tampoco permite asegurar que el tiempo transcurrido entre la estimación y la lectura fuese exactamente de 10 minutos simulados.

Estas comparaciones a **+10 minutos simulados**, con intervalo confirmado durante la revisión, no reemplazan el [informe de evaluación de Random Forest v2](RF_INFORME_EVALUACION_V2_20261111.md), calculado sobre **922 predicciones de prueba** con **RMSE RF 0,114327** frente a **persistencia 0,172037**. Son **dos pruebas de distinto alcance**.

## Para cerrar la verificación funcional del modelo rf-v2 en Python

1. Conservar una captura que muestre `IA predictiva: MODELO NUEVO CARGADO` y una **predicción numérica** con la aplicación que se esté ejecutando.
2. Registrar el **nombre del script y ruta del `.pkl`** utilizado, así como el SHA-256 del modelo cargado (el archivo local ya coincide por hash con la Release `rf-v2`).
3. **El intervalo de +10 minutos simulados ya fue confirmado.** Para hacer la evidencia más reproducible, añadir si se conservan las anotaciones **instante de emisión t e instante de observación t+10**, además del escenario y cambios de lluvia/riego.
4. La funcionalidad de la aplicación se puede documentar con capturas y un registro breve sin repetir todo el entrenamiento ni toda la simulación.

**Estado:** comparación de pronósticos a **+10 minutos simulados**, intervalo confirmado por la persona que registró los 21 pares. **Pendiente aportar marcas de tiempo por fila y captura que vincule esta ejecución concreta al modelo `rf-v2`**. Las métricas estadísticas principales son las de las 922 muestras de prueba. No se ha modificado el código ni los modelos.
