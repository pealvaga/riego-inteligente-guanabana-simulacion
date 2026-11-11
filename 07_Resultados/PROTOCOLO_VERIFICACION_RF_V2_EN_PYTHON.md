# Verificación funcional del modelo Random Forest `rf-v2` en Python

## Objetivo y alcance

Comprobar que el mismo archivo `modelo_prediccion_humedad.pkl` publicado en [Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2) puede **cargarse y utilizarse para inferencia** en la simulación Python, **sin modificar** el código del proyecto, CODESYS ni Factory I/O. Esta comprobación de integración **no sustituye** la evaluación estadística ya realizada sobre 922 predicciones de prueba.

La **identidad del modelo local y del adjunto de GitHub ya se comprobó** por SHA-256: `c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`. Sin embargo, a fecha de redacción **no se ha aportado una captura de esta ejecución específica con el archivo `rf-v2`**. Las capturas anteriores muestran un modelo cargado, pero pueden corresponder a otra revisión del archivo.

## Procedimiento mínimo sugerido

1. **Conservar respaldo** del `.pkl` anterior y colocar **una copia** de `rf-v2` con el nombre `modelo_prediccion_humedad.pkl` junto al archivo de Python que realmente se ejecuta. Si se ejecuta `01_Python/Sensores.py`, ambos archivos deben estar en `01_Python/`; si se usa el simulador alternativo de `04_Random_Forest`, indicar expresamente esa ruta. No es necesario modificar Python ni el PLC.
2. Ejecutar la misma aplicación que se utilizó durante la simulación integrada. Confirmar la conexión Modbus y el inicio del escenario. **Captura A:** interfaz, nombre del script en ejecución y estado `IA predictiva: MODELO NUEVO CARGADO`. Una pantalla de "modelo cargado" sin identificación del `.pkl` utilizado no demuestra por sí sola la versión.
3. Dejar que el sistema reúna los rezagos requeridos: tres muestras temporales de entrada a intervalos de **10 minutos simulados**. Confirmar que aparece una cifra numérica en `Humedad estimada en +10 min`. **Captura B:** escenario, tiempo simulado, humedad actual, humedad estimada y estado de próximo riego.
4. Opcional para reforzar la evidencia: elegir **3 a 5 instantes de predicción** y anotar en cada uno el instante `t`, el valor predicho para `t+10` minutos simulados y la humedad observada exactamente en `t+10`. Calcular `error absoluto = |predicho − observado|` en **puntos porcentuales**. Registrar también cambios de riego, precipitación o condiciones entre ambos instantes. No comparar lecturas de instantes diferentes sin señalarlo.
5. **Captura C o tabla breve:** mostrar al menos un registro con predicción y humedad observada, indicando fecha/escenario/tiempo simulado, o un video corto que muestre la aplicación cargando y produciendo estimaciones.
6. Guardar capturas bajo `07_Resultados/` cuando se disponga de ellas; incluir nombre del archivo `.pkl`, hash SHA-256, script utilizado, fecha, versión de Python y resultado. La ejecución se marca **verificada** solo después de contar con estas evidencias.

## Tabla sugerida para observación

| Escenario | Hora simulada `t` | Humedad actual (%) | Pronóstico `t+10` (%) | Observada `t+10` (%) | Error absoluto (p.p.) | Cambio de lluvia/riego |
|---|---|---:|---:|---:|---:|---|
| Sin completar | Sin completar | — | — | — | — | — |
| Sin completar | Sin completar | — | — | — | — | — |
| Sin completar | Sin completar | — | — | — | — | — |

**Criterios mínimos de éxito de la integración:**

- El programa carga `rf-v2` sin errores de formato ni versión del simulador.
- Se obtiene una predicción numérica plausible en el intervalo 0–100 % después de acumular los rezagos.
- La aplicación sigue ejecutando simulación y comunicación con CODESYS, sin fallos atribuibles al modelo.

**No afirmar** que una sola predicción correcta prueba precisión, generalización a campo o calidad agronómica. Las métricas verificadas de la evaluación publicada son: **922 muestras de prueba**, RMSE RF **0,114327**, RMSE persistencia **0,172037**, RMSE reducido **33,55 %**. Ver el [informe estadístico](RF_INFORME_EVALUACION_V2_20261111.md).

## Pruebas integradas realizadas previamente

Según la declaración de operación del proyecto, las pruebas funcionales de Python, CODESYS y Factory I/O (incluidas maniobras de riego, START/STOP, emergencia y rearme) **se realizaron repetidamente y funcionaron sin inconvenientes reportados**. Esta información se registra como **declaración de ejecución**, no como mediciones nuevas ni una evidencia adicional de cada transición de señal. Las [20 capturas E1–E20 publicadas](evidencias_integracion_guanabana/) documentan varias etapas observables; para detalles sobre lo que cada captura demuestra y lo que no permite verificar aisladamente, consultar el [informe de integración](EVIDENCIA_EJECUCION_INTEGRADA.md).

No se exige repetir las maniobras ya realizadas por el mero hecho de redactar este informe. Si se requiere acreditación específica de STOP/START u otra señal en la sustentación, es preferible recuperar capturas o video existente y dejar explícito su alcance.
