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

## Prueba funcional sencilla sin cambiar programas ni modelos

1. Conservar respaldo de las pruebas actuales y dejar la conexión Modbus activa con CODESYS.
2. En **Simulación ambiental**, poner una **humedad inicial cercana al umbral, por ejemplo 65 %**, temperatura de **30 °C** y precipitación de **0 mm/h**; son parámetros de prueba, **no recomendaciones agronómicas**.
3. Pulsar **Reiniciar** para aplicar la nueva humedad inicial (esta casilla solo se aplica al reiniciar), luego **Iniciar simulación**.
4. Verificar que el estado de riego está **inactivo** inicialmente y que se reúnen al menos **tres muestras** separadas 10 minutos simulados.
5. Registrar humedad actual, pronóstico a +10 minutos y estado de próximo riego. Si aparece fecha/hora estimada, anotar también el cruce real posterior de 60 % para medir error de instante en minutos.
6. Si continúa «NO ESTIMADO» aun cuando la humedad disminuye y se acerca a 60 %, el próximo diagnóstico técnico es **inspeccionar los 12 pasos recursivos y el descenso medio calculado**, para determinar si las predicciones se aplanan y por qué. **No cambiar el umbral de 60 %, las reglas de CODESYS ni el modelo sin una prueba controlada**.

Se mantienen separados dos objetivos: **(a) predicción de humedad a +10 minutos**, ya respaldada por el CSV de 922 casos y las 21 parejas complementarias; **(b) predicción del instante de próximo riego**, aún sin error cuantitativo validado.

No se modificó el código de la aplicación ni CODESYS/Factory I/O para elaborar este diagnóstico.
