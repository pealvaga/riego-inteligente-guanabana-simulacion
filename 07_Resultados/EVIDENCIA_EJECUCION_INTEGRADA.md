# Evidencia de ejecución integrada — Python, CODESYS y Factory I/O

## Origen y alcance

Revisión de **cinco capturas de pantalla proporcionadas por el autor** de la simulación del sistema de riego para guanábana. Las capturas se obtuvieron durante una sesión operativa, con instantes simulados diferentes; **no se deben interpretar como una única medición sincronizada**. Los archivos de imagen originales **todavía no están incluidos** en el repositorio. Este documento transcribe la evidencia observable y registra lo que falta demostrar.

**Software registrado:**
- CODESYS IDE V3.5 SP9 Patch 1; CODESYS Control Win V3 3.5.9.10.
- Factory I/O 2.5.10.
- Windows, Python 3.12.9 (según captura de entorno; pendiente de comprobar si es el mismo intérprete de la ejecución).
- OPCConfig 3.5.9.0.

## Capturas revisadas

| Evidencia | Vista mostrada | Elementos visibles | Qué sustenta |
|---|---|---|---|
| E1 | Factory I/O: Driver | «OPC Client DA/UA», símbolo de verificación verde, servidor **`CoDeSys.OPC.DA (14)`**, mapeo de `FO_*` a sensores y actuadores | El driver aparece conectado con **14 señales configuradas** sobre un servidor OPC **DA** |
| E2 | Python: Simulación ambiental | «Modbus: COMUNICACIÓN OK»; estado «EN EJECUCIÓN»; humedad **33,28 % de agua disponible**, riego recibido desde CODESYS **ACTIVO**; temperatura configurada **35 °C** y precipitación **0 mm/h** | La aplicación de simulación está operando y muestra intercambio de estado de riego; no es una prueba cuantitativa de precisión |
| E3 | Python: Comunicación Modbus | `127.0.0.1:502`, Device ID `1`, «COMUNICACIÓN OK», día 2 y hora 01:23; mapa **HR0–HR7/IR0** | La aplicación muestra el canal Modbus establecido y su mapeo |
| E4 | CODESYS: Visualización HMI | Día 2, aprox. 01:41, temperatura **35 °C**, precipitación **0,0 mm/h**, tanques de fertilizante/agua con porcentajes | SCADA abierto con variables y estados de proceso presentados |
| E5 | CODESYS: Vista de proyecto | `Grado.project*`; dispositivo marcado **«Conectado»**, `Application [ejecutar]`, visualización con fecha/hora simulada y niveles; programas `OPERACIONES`, `RIEGO`, `REGISTRO_DATOS` visibles en árbol | Controlador conectado y aplicación mostrada en ejecución con HMI activa |

En E4 se observan aproximadamente **95,4 %** en el tanque de fertilizante y **84,9 %** en el de agua; en E5 se observan **95,4 %** y **80,4 %**, respectivamente. La diferencia es coherente con capturas en tiempos distintos, pero **no certifica por sí sola el intercambio dinámico OPC** ni el balance de caudales.

En E2 la interfaz muestra además:

- Escenario **4**.
- **338 muestras** registradas y **319 filas aptas para RF**.
- Archivo anunciado por el programa: `Datos_entrenamiento_guanabana_20261110_221621.xlsx` (no se ha comprobado que ese archivo esté publicado en GitHub).
- «IA predictiva: **MODELO NUEVO CARGADO**»; humedad pronosticada a +10 minutos **55,46 %**; «Próximo riego: **RIEGO ACTIVO**».
- «Tipo de riego: **SIN DECISIÓN**» en la cabecera. No es inconsistente por sí solo con el estado **RIEGO ACTIVO**, ya que la selección de tipo de riego y la histéresis de activación son señales distintas.

**Importante sobre Random Forest:** «MODELO NUEVO CARGADO» indica disponibilidad del archivo para inferencia, **no validación estadística**, ni demuestra que haya superado la referencia de persistencia. Los resultados de evaluaciones anteriores estaban marcados como NO VALIDADOS. La captura parece corresponder a la **variante de simulador con registro y exportación de RF**; no se debe atribuir automáticamente a `01_Python/Sensores.py` sin cotejar el archivo realmente ejecutado.

## Qué se puede afirmar de forma sustentada

1. Factory I/O **muestra una conexión activa** con el servidor `CoDeSys.OPC.DA` y 14 símbolos.
2. Python muestra conexión **Modbus TCP** a `127.0.0.1:502` (Device ID 1).
3. El proyecto CODESYS se muestra **conectado y ejecutándose**; la visualización SCADA presenta variables de la misma simulación.
4. La aplicación Python muestra humedad, estado de riego, evolución del tiempo simulado y un módulo de registro para Random Forest.
5. La evidencia es de una **simulación**, no de medición en un cultivo físico ni de validación agronómica.

## Qué no prueban todavía estas capturas

- No se ve el **resultado de compilación sin errores** o el panel de mensajes. En el árbol del dispositivo aparece un icono de advertencia junto a `Ethernet`; debe revisarse si corresponde a un diagnóstico activo o una configuración que requiera atención.
- No se ha observado una prueba dirigida donde se conmuten los pulsadores de Factory I/O y se verifique la variación correspondiente de `FO_START`, `FO_STOP`, válvulas, niveles y `FO_*` en CODESYS.
- No se ha verificado numéricamente la transmisión real de todos los registros HR0–HR7 ni el retorno IR0 para valores de prueba conocidos, pese a mostrarse «COMUNICACIÓN OK».
- No se ha comprobado en esta serie el cambio de modalidad entre riego normal y fertirriego, ni el cálculo efectivo de MobileNetV2.
- No se han publicado aquí las capturas originales, el archivo histórico `HistorialCultivo.csv`, la base Excel anunciada o un acta de prueba independiente.
- No se aportan métricas independientes o trazabilidad completa de los modelos de IA.

## Próximas evidencias mínimas sugeridas

1. Guardar una captura del panel **Compilar / Mensajes** que muestre compilación de `Grado.project` sin errores y, si procede, explicar iconos de advertencia en el árbol.
2. Ejecutar una prueba corta de **Factory I/O ↔ CODESYS**: accionar `FO_START` y `FO_STOP`; capturar sus cambios en variables, al igual que una salida de válvula y una lectura de nivel.
3. Ejecutar una prueba corta de **Python ↔ CODESYS**: comparar en el mismo instante `Temperatura`, `Precipitacion`, `HumedadSuelo` y `MB_RiegoOn` en ambos lados; comprobar HR0–HR7/IR0.
4. Conservar evidencia del **evento de riego** (inicio y parada alrededor de los umbrales programados) y del histórico guardado; verificar qué señales representan `GVL.Riego` y `GVL.Regando`.
5. Documentar una prueba de **MobileNetV2** con hoja de muestra y umbral 0,90, sin considerarla diagnóstico agronómico definitivo.
6. Publicar las capturas originales, si se desea, en `07_Resultados/evidencias_integracion/` y vincularlas desde este reporte.

## Conclusión

Las capturas son evidencia favorable de **funcionamiento concurrente y conectividad indicada por las interfaces** de los tres componentes. Con ellas se puede sustentar una demostración funcional preliminar para la primera observación del docente. **No son una certificación de ejecución completamente reproducida por terceros, ni prueba de exactitud de las IA**.

El reporte se elaboró a partir de las capturas aportadas por el autor; no se modificaron `Sensores.py`, CODESYS, Factory I/O ni los modelos.
