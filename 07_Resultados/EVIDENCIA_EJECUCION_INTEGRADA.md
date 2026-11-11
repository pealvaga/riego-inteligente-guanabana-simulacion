# Evidencia de ejecución integrada — Python, CODESYS y Factory I/O

## Origen y alcance

Revisión inicial de **cinco capturas de pantalla proporcionadas por el autor**, ampliada posteriormente con **tres capturas adicionales** (compilación CODESYS, escena Factory I/O y tabla de variables GVL) de la simulación del sistema de riego para guanábana. Las capturas se obtuvieron durante una sesión operativa, con instantes simulados diferentes; **no se deben interpretar como una única medición sincronizada**. Los archivos de imagen originales **todavía no están incluidos** en el repositorio. Este documento transcribe la evidencia observable y registra lo que falta demostrar.

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

## Ampliación de evidencia: compilación CODESYS y señales visibles

Se recibieron tres capturas adicionales que complementan la serie anterior:

| Evidencia | Vista | Datos observados | Interpretación acotada |
|---|---|---|---|
| E6 | CODESYS, ventana «Mensajes > Compilar» | **0 errores, 0 advertencias, 3 mensajes informativos**; «The application is up to date» y «Compilación terminada -- 0 errores, 0 advertencias» | Evidencia concreta de compilación exitosa de **`Device.Application`** en la sesión capturada |
| E7 | Factory I/O, escena con dos depósitos | Tanques virtuales, niveles de líquido diferentes, válvulas/sensores y tablero de control | Evidencia visual de que la escena fue abierta y se muestran sus elementos; una imagen fija no permite medir por sí sola los cambios en tiempo real |
| E8 | CODESYS, monitor en línea `Device.Application.GVL` | `FO_Riego1=TRUE`, `FO_Riego2=FALSE`, `FO_S_DESCARGA1=TRUE`, `FO_S_DESCARGA2=FALSE`; `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644`; `FO_LEDV=TRUE`, `FO_START=FALSE`, `FO_STOP=TRUE`, `FO_EMERGENCIA=FALSE`, `MB_Temp=350` | Evidencia de variables en vivo mostradas por CODESYS, con salidas y mediciones relacionadas con Factory I/O y un registro de temperatura proveniente de Python |

El registro **`MB_Temp=350`** es consistente con **35,0 °C** al utilizar la escala ×10 que describe el programa Python y que aparece en las capturas previas de la HMI/SCADA.

Los valores **`FO_S_NIVEL1` y `FO_S_NIVEL2` se transcriben tal como aparecen en la tabla GVL**; no se convierten a porcentajes porque esta captura no demuestra la unidad ni el escalamiento de esa variable. Que `FO_STOP=TRUE` y `FO_Riego1=TRUE` aparezcan al mismo tiempo no permite inferir, sin una secuencia de eventos, si se trata de una condición transitoria, la interpretación eléctrica del pulsador o un problema lógico. Para resolverlo sería necesario observar las transiciones y las condiciones en CODESYS.

El árbol de dispositivos muestra un símbolo de advertencia junto a **Ethernet**. Esto **no contradice** el contador **0 advertencias de compilación**: un posible diagnóstico de dispositivo y los resultados del compilador corresponden a ámbitos distintos. Se debe inspeccionar su descripción sin afirmar que es un fallo funcional.

### Comprobaciones ya reforzadas

- **Compilación del proyecto:** corroborada por ventana de mensajes con cero errores y cero advertencias.
- **Aplicación del PLC en ejecución:** identificada por el árbol del proyecto en las capturas E5 y E6.
- **Existencia de variables integradas y valores numéricos:** verificada en GVL (E8), incluida temperatura Modbus coherente con la mostrada en Python.
- **Escena Factory I/O abierta:** corroborada visualmente (E7), además de su configuración de conexión observada en E1.

**Límite:** una tabla de valores instantáneos **no demuestra** una prueba de variación controlada de esas señales. Para cerrar la verificación funcional, tomar por lo menos dos capturas o un video breve con una entrada/actuador cambiando y observar la misma variable en CODESYS.

## Qué se puede afirmar de forma sustentada

1. Factory I/O **muestra una conexión activa** con el servidor `CoDeSys.OPC.DA` y 14 símbolos.
2. Python muestra conexión **Modbus TCP** a `127.0.0.1:502` (Device ID 1).
3. El proyecto CODESYS se muestra **conectado y ejecutándose**; la visualización SCADA presenta variables de la misma simulación.
4. La aplicación Python muestra humedad, estado de riego, evolución del tiempo simulado y un módulo de registro para Random Forest.
5. La evidencia es de una **simulación**, no de medición en un cultivo físico ni de validación agronómica.

## Qué no prueban todavía estas capturas

- **La compilación sin errores ya se documentó con la captura E6.** En el árbol de dispositivos aparece un icono de advertencia junto a `Ethernet`; debe revisarse por separado para determinar si corresponde a un diagnóstico activo o configuración pendiente.
- No se ha observado una prueba dirigida donde se conmuten los pulsadores de Factory I/O y se verifique la variación correspondiente de `FO_START`, `FO_STOP`, válvulas, niveles y `FO_*` en CODESYS.
- No se ha verificado numéricamente la transmisión real de todos los registros HR0–HR7 ni el retorno IR0 para valores de prueba conocidos, pese a mostrarse «COMUNICACIÓN OK».
- No se ha comprobado en esta serie el cambio de modalidad entre riego normal y fertirriego, ni el cálculo efectivo de MobileNetV2.
- No se han publicado aquí las capturas originales, el archivo histórico `HistorialCultivo.csv`, la base Excel anunciada o un acta de prueba independiente.
- No se aportan métricas independientes o trazabilidad completa de los modelos de IA.

## Próximas evidencias mínimas sugeridas

1. **Compilación lograda (E6)**. Conservar el PNG original y, si procede, documentar el significado del icono de advertencia en Ethernet.
2. Ejecutar una prueba corta de **Factory I/O ↔ CODESYS**: accionar `FO_START` y `FO_STOP`; capturar sus cambios en variables, al igual que una salida de válvula y una lectura de nivel.
3. Ejecutar una prueba corta de **Python ↔ CODESYS**: comparar en el mismo instante `Temperatura`, `Precipitacion`, `HumedadSuelo` y `MB_RiegoOn` en ambos lados; comprobar HR0–HR7/IR0.
4. Conservar evidencia del **evento de riego** (inicio y parada alrededor de los umbrales programados) y del histórico guardado; verificar qué señales representan `GVL.Riego` y `GVL.Regando`.
5. Documentar una prueba de **MobileNetV2** con hoja de muestra y umbral 0,90, sin considerarla diagnóstico agronómico definitivo.
6. Publicar las capturas originales, si se desea, en `07_Resultados/evidencias_integracion/` y vincularlas desde este reporte.

## Conclusión

Las ocho capturas son evidencia favorable de **compilación sin errores, aplicación conectada/en ejecución, variables online y conectividad indicada por las interfaces** de los tres componentes. Con ellas se puede sustentar una demostración funcional preliminar para la primera observación del docente. **No son una certificación de ejecución completamente reproducida por terceros, ni prueba de exactitud de las IA**.

El reporte se elaboró a partir de las capturas aportadas por el autor; no se modificaron `Sensores.py`, CODESYS, Factory I/O ni los modelos.
