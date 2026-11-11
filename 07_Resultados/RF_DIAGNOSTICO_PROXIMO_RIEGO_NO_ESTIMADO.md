# Interpretación de «Próximo riego: NO ESTIMADO CON LAS CONDICIONES ACTUALES»

## Estado de la comprobación (11/11/2026)

Se confirmó que se recopilaron **21 parejas de predicción de humedad a +10 minutos simulados** y su lectura real **exactamente 10 minutos simulados más tarde**. Los resultados redondeados se documentaron en [la comparación operativa](RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md): MAE **0,00429** y RMSE **0,00655 puntos porcentuales**. La humedad real de esa muestra se situó entre **75,52 y 76,61 %**.

El sistema también presenta, en algunas condiciones, el mensaje **«Próximo riego: NO ESTIMADO CON LAS CONDICIONES ACTUALES»**. Esta situación **no demuestra que falle la predicción de humedad a +10 minutos**, porque el aviso corresponde a un **cálculo adicional del tiempo futuro de cruce del umbral de riego**, no a la predicción directa del siguiente paso.

## Lógica exacta revisada en Python

La misma función está en [`01_Python/Sensores.py`](../01_Python/Sensores.py) y [`04_Random_Forest/simulador_guanabana_grado_registro_RF.py`](../04_Random_Forest/simulador_guanabana_grado_registro_RF.py): `_estimate_next_irrigation()`.

1. Si `irrigation_on == True`, muestra «RIEGO ACTIVO».
2. Si la humedad actual es **menor o igual a 60 %**, indica «UMBRAL DE 60 % ALCANZADO».
3. En caso contrario proyecta recursivamente **12 pasos de 10 minutos** (dos horas simuladas) con el modelo Random Forest y riego supuesto desactivado.
4. Si no alcanza 60 % en esos pasos, calcula el **descenso medio de las cuatro transiciones más recientes** de la trayectoria proyectada.
5. Si el descenso es **≤ 0,01 puntos porcentuales por paso** devuelve `not_found`.
6. Si el descenso es mayor, extrapola linealmente hasta 60 %. Si la estimación requiere **más de 72 horas simuladas**, también devuelve `not_found`.
7. En los otros casos muestra el día y la hora simulada estimados.

Por tanto, el mensaje de «NO ESTIMADO» significa que **no se encontró cruce en las primeras dos horas y la tendencia recursiva no fue suficiente, o que la extrapolación excede el horizonte de 72 horas**. No se ha medido todavía cuál de las dos condiciones se activó en la ejecución concreta.

## Ejemplo ilustrativo sin atribuirlo al resultado del modelo

Desde **75,52 %** para alcanzar el umbral de 60 % se necesitan **15,52 puntos porcentuales**. Si el descenso fuese constante:

| Descenso por 10 min simulados | Tiempo aproximado |
|---|---|
| 0,02 p.p. | 129,3 horas |
| 0,04 p.p. | 64,7 horas |
| 0,06 p.p. | 43,1 horas |

Esto solo ilustra la sensibilidad al descenso, **no es una proyección calculada por el bosque ni valida el instante del próximo riego**.

## Diagnóstico adicional: mismo 65 %, estados de riego distintos

El entrenamiento **agrupa los registros por `Sesion` y `Escenario`** para construir rezagos y separar conjuntos de prueba, pero **no entrega esos identificadores al Random Forest**. Las 12 variables de entrada incluyen `RiegoActivo`, `RiegoActivo_lag1`, `RiegoActivo_lag2` y los valores recientes de humedad, temperatura y precipitación. Por tanto, **no se puede afirmar que el modelo «recuerde que la sesión 1 siempre regaba»**: su predicción depende de las entradas suministradas y de los patrones que aprendió.

En CODESYS, la histéresis pone el riego en marcha con humedad **< 60 %** y lo mantiene hasta una humedad **> 75 %**. El mismo **65 %** puede ocurrir en dos estados:

| Trayectoria | Estado `RiegoActivo` | Comportamiento físico esperado sin lluvia |
|---|---:|---|
| Humedad 59 → 65 % después de activar el riego | 1 | Aumento si el riego aporta más agua que la evapotranspiración |
| Humedad 80 → 65 % mientras el riego está detenido | 0 | Descenso por evapotranspiración |

**Detalle de reinicio:** `reset_simulation()` reinicia humedad, reloj e historial de IA en Python, **pero no modifica la variable `self.irrigation_on` ni resetea el estado retenido de CODESYS**. Al iniciar, Python vuelve a leer IR0 por Modbus. Por eso, cambiar «Humedad inicial» a 65 % después de una prueba con riego activo puede mantener la señal de riego en 1: en ese caso, una humedad ascendente es coherente con la lógica del controlador.

**Si `RiegoActivo=0`, `Precipitacion=0` y aun así el modelo predice aumentos**, esa es una discrepancia concreta entre la predicción del bosque y el balance hídrico implementado. También puede manifestarse solo en el pronóstico **recursivo** del próximo riego, aunque la predicción individual a +10 minutos sea correcta. Requiere revisar cobertura de datos por estado de riego y estabilidad de la recursión; **no demuestra por sí sola mezcla incorrecta de sesiones**.

En el proyecto hay una diferencia de nombres que conviene inspeccionar en CODESYS: algunos registros históricos usan `GVL.Riego`, mientras que el estado enviado a Python por IR0 proviene de `GVL.Regando` mediante `GVL.MB_RiegoOn`. Si no coinciden, sería necesaria una comprobación del significado operativo de la etiqueta `RiegoActivo`.

## Prueba funcional propuesta, sin modificar código ni modelos

1. Abrir Python conectado a CODESYS, con precipitación **0 mm/h**, y observar simultáneamente **«Riego recibido desde CODESYS: ACTIVO/INACTIVO»** y, si es posible, `GVL.Regando` / `GVL.Riego`.
2. **Recorrido de secado:** configurar una humedad inicial **por encima de 75 %** (por ejemplo 80 %), pulsar **Reiniciar**, comprobar en CODESYS que el riego queda **INACTIVO**, iniciar y dejar descender la humedad **naturalmente** hasta ~65 %. Anotar humedad actual, `RiegoActivo` y pronóstico a +10 minutos.
3. **Recorrido con riego:** configurar menos de **60 %** (por ejemplo 59 %), permitir que CODESYS active el riego y registrar lo que ocurre cuando la humedad asciende hacia 65 %. Debe verificarse **RiegoActivo=1** durante esta trayectoria.
4. **No comparar solamente «reiniciar en 65 %» frente a «llegar bajando a 65 %»** sin verificar IR0: el estado de riego retenido por histéresis cambia el significado físico del mismo porcentaje.
5. Si en el recorrido de secado `RiegoActivo=0` y no llueve, pero **la IA calcula una subida sostenida**, anotar 3–5 predicciones individuales y el mensaje de «Próximo riego». Habría que estudiar si el error aparece en **el primer paso** o **solo después de varios pasos recursivos**.
6. No modificar la histéresis del PLC, el modelo `.pkl` ni las etiquetas de entrenamiento para forzar una predicción. Identificar antes qué variable o etapa genera la discrepancia.

No se ha confirmado todavía cuál de las dos causas (estado de riego retenido o extrapolación recursiva incorrecta) explica la observación concreta: **falta la lectura de `RiegoActivo` cuando aparece el aumento pronosticado a 65 %**.

Se mantienen separados dos objetivos: **(a) predicción de humedad a +10 minutos**, ya respaldada por el CSV de 922 casos y las 21 parejas complementarias; **(b) predicción del instante de próximo riego**, aún sin error cuantitativo validado.

No se modificó el código de la aplicación ni CODESYS/Factory I/O para elaborar este diagnóstico.
