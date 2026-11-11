# Evidencia de ejecución integrada — Python, CODESYS y Factory I/O

## Origen y alcance

Revisión inicial de **cinco capturas de pantalla proporcionadas por el autor**, ampliada posteriormente con **quince capturas adicionales** (compilación CODESYS, escena Factory I/O, tabla GVL, emergencia, salidas detenidas, secuencia de rearme y estado de parada con indicador amarillo) de la simulación del sistema de riego para guanábana. Las capturas se obtuvieron durante una sesión operativa, con instantes simulados diferentes; **no se deben interpretar como una única medición sincronizada**. Los archivos de imagen originales **todavía no están incluidos** en el repositorio. Este documento transcribe la evidencia observable y registra lo que falta demostrar.

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

Los valores **`FO_S_NIVEL1` y `FO_S_NIVEL2` se transcriben tal como aparecen en la tabla GVL**; no se convierten a porcentajes porque esta captura no demuestra la unidad ni el escalamiento de esa variable. Que `FO_STOP=TRUE` y `FO_Riego1=TRUE` aparezcan al mismo tiempo es **coherente con la lógica normalmente cerrada declarada posteriormente por el autor**: TRUE corresponde al pulsador sin accionar. La prueba de pulsación TRUE→FALSE sigue pendiente.

El árbol de dispositivos muestra un símbolo de advertencia junto a **Ethernet**. Esto **no contradice** el contador **0 advertencias de compilación**: un posible diagnóstico de dispositivo y los resultados del compilador corresponden a ámbitos distintos. Se debe inspeccionar su descripción sin afirmar que es un fallo funcional.

### Comprobaciones ya reforzadas

- **Compilación del proyecto:** corroborada por ventana de mensajes con cero errores y cero advertencias.
- **Aplicación del PLC en ejecución:** identificada por el árbol del proyecto en las capturas E5 y E6.
- **Existencia de variables integradas y valores numéricos:** verificada en GVL (E8), incluida temperatura Modbus coherente con la mostrada en Python.
- **Escena Factory I/O abierta:** corroborada visualmente (E7), además de su configuración de conexión observada en E1.

**Límite:** una tabla de valores instantáneos **no demuestra** una prueba de variación controlada de esas señales. Para cerrar la verificación funcional, tomar por lo menos dos capturas o un video breve con una entrada/actuador cambiando y observar la misma variable en CODESYS.

## Ampliación: cambio observado en la señal de emergencia

Se recibieron dos capturas adicionales:

| Evidencia | Vista | Dato observado | Alcance |
|---|---|---|---|
| **E9** | Panel de control de Factory I/O con pulsador de emergencia | Se observa físicamente el control de emergencia en la escena simulada | Documenta la ubicación y el accionamiento presentado por el autor; el fotograma aislado no identifica automáticamente su estado eléctrico |
| **E10** | Monitor en línea `Device.Application.GVL` de CODESYS | **`FO_EMERGENCIA = TRUE`** | Documenta la recepción/visualización del estado lógico activo de la variable en el PLC virtual |

En una captura **anterior E8**, tomada sobre `Device.Application.GVL`, se observaba **`FO_EMERGENCIA = FALSE`**. La comparación **FALSE → TRUE** en el registro de CODESYS, acompañada de la captura del pulsador en Factory I/O, es **evidencia favorable de cambio de estado de una entrada vinculada entre la escena y el controlador**. Las imágenes no muestran un único instante sincronizado, por lo que no sustituyen una grabación completa ni una prueba automatizada de latencia.

**No queda demostrada aún la actuación de seguridad**: para comprobar que la emergencia detiene realmente el riego simulado se requiere observar qué sucede, tras activarla, con `FO_Riego1`, `FO_Riego2`, las válvulas, el indicador de emergencia, y cómo se restablece el sistema. El hecho de que `FO_EMERGENCIA=TRUE` no demuestra por sí solo que el control pase a estado seguro.

Esta es una prueba de **simulación industrial virtual**; no certifica una función de seguridad física ni un nivel de integridad de seguridad.

## Ampliación: salidas de riego con emergencia activada

Se aportaron **dos capturas adicionales (E11–E12)** para comprobar la respuesta del sistema después de la activación de la emergencia.

| Evidencia | Vista | Observación |
|---|---|---|
| **E11** | Escena Factory I/O | Dos depósitos con niveles distintos. En el depósito derecho se aprecia **un chorro de entrada de agua desde la parte superior**, mientras el panel de emergencia está visible. La imagen fija no indica en qué instante se inició o detuvo ese caudal. |
| **E12** | Monitor CODESYS `Device.Application.GVL` | `FO_EMERGENCIA=TRUE`, `FO_Riego1=FALSE`, `FO_Riego2=FALSE`, `FO_S_DESCARGA1=FALSE`, `FO_S_DESCARGA2=FALSE`, `FO_LEDR=TRUE`, `FO_LEDV=FALSE`, `FO_Llenado1=0`, `FO_Llenado2=0`, `FO_S_NIVEL1=5.23745632`, `FO_S_NIVEL2=9.378026`, `FO_STOP=TRUE`. |

### Comparación de salidas y señales

| Variable | GVL anterior E8, emergencia FALSE | GVL actual E12, emergencia TRUE |
|---|---|---|
| `FO_EMERGENCIA` | FALSE | **TRUE** |
| `FO_Riego1` | TRUE | **FALSE** |
| `FO_Riego2` | FALSE | **FALSE** |
| `FO_S_DESCARGA1` | TRUE | **FALSE** |
| `FO_S_DESCARGA2` | FALSE | **FALSE** |
| `FO_LEDR` | FALSE | **TRUE** |
| `FO_LEDV` | TRUE | **FALSE** |

La secuencia observada es **coherente con desactivación de salidas de riego y encendido del indicador rojo cuando la emergencia está activa**, y aporta evidencia adicional de comportamiento lógico del sistema. Sin embargo, las capturas no son una grabación sincronizada; no es posible aislar rigurosamente la causa única del cambio. Según la aclaración posterior del autor, `FO_STOP=TRUE` es el estado de reposo de su pulsador NC, no una orden de parada. **No se certifica con ello una función de parada de seguridad física.**

**Hallazgo que requiere comprobación:** en E11 se ve un chorro entrando al tanque derecho, mientras que en E12 `FO_Llenado2=0`. Puede deberse a instantes distintos, animación/flujo residual o configuración de la válvula. Para determinarlo es necesario capturar la escena y el valor de la variable simultáneamente, observar si el chorro se detiene al cabo de unos segundos simulados y verificar el mapeo del actuador correspondiente. No declarar que *todas* las válvulas se han cerrado únicamente a partir de esta serie.

**Pendiente de completar:** registrar el rearme de la emergencia, la recuperación controlada de indicadores y salidas, y el comportamiento del llenado; preferiblemente con un video corto o capturas simultáneas de Factory I/O y el monitor GVL.

## Ampliación E13–E16: rearme de emergencia y regreso de una salida de riego

Se revisaron **cuatro capturas adicionales**: dos vistas de los tanques en Factory I/O (E13, E15) y dos capturas de `Device.Application.GVL` en CODESYS (E14, E16). Permiten describir los estados observados en diferentes instantes; **no son una grabación sincronizada del ciclo de rearme**.

| Señal | Captura E14: emergencia activa | Captura E16: emergencia liberada |
|---|---|---|
| `FO_EMERGENCIA` | **TRUE** | **FALSE** |
| `FO_Riego1` | FALSE | FALSE |
| `FO_Riego2` | FALSE | **TRUE** |
| `FO_S_DESCARGA1` | FALSE | FALSE |
| `FO_S_DESCARGA2` | FALSE | **TRUE** |
| `FO_LEDR` | **TRUE** | **FALSE** |
| `FO_LEDV` | FALSE | **TRUE** |
| `FO_STOP` | **TRUE** | **TRUE** |
| `FO_START` | FALSE | FALSE |
| `FO_Llenado1` | 0 | 0 |
| `FO_Llenado2` | 0 | 0 |
| `FO_S_NIVEL1` | 5.23745632 | 5.23745632 |
| `FO_S_NIVEL2` | 6.993286 | 6.487397 |

En ambas nuevas vistas de Factory I/O **no se aprecia el chorro de llenado superior del tanque derecho** que aparecía en E11. Esta observación es compatible con un llenado detenido en esos instantes, sin establecer su causa ni demostrar de manera concluyente el funcionamiento de todas las válvulas.

### Interpretación y asuntos sin cerrar

La secuencia **muestra un retorno de `FO_EMERGENCIA` a FALSE, el cambio de indicador rojo a verde y la reactivación de la salida `FO_Riego2` con `FO_S_DESCARGA2=TRUE`**. Es evidencia de un **rearme observado en la simulación y recuperación de la lógica de riego**.

Sin embargo, **no se puede afirmar** que el riego requiera una nueva orden de inicio tras soltar la emergencia. En las capturas `FO_START=FALSE` y `FO_STOP=TRUE` tanto antes como después; el autor aclaró que `FO_STOP=TRUE` significa **reposo del pulsador NC**, no una orden de parada activa. Se recomienda registrar explícitamente si el riego vuelve automáticamente al quitar emergencia y evaluar si esa conducta es la deseada en la simulación.

Los niveles de los tanques se muestran como valores de variables `REAL` sin atribuir unidades ni porcentajes: `FO_S_NIVEL2` desciende de 6.993286 a 6.487397 entre E14 y E16. Esta diferencia es consistente con una descarga activada posteriormente, pero no equivale a una prueba cuantitativa de caudal.

**Pendientes de esta prueba:** comprobar mediante pulsación la polaridad NC declarada de `FO_STOP`, verificar si se exige rearme/START o si el restablecimiento es automático, observar valores y movimiento en el mismo instante, y conservar las capturas originales en GitHub. Este análisis **no certifica una función de seguridad física**.

## Ampliación E17–E20: estado sin riego e indicador amarillo

Se recibieron **cuatro capturas adicionales**: tres vistas de la escena Factory I/O y una tabla de variables `Device.Application.GVL`. Los depósitos se muestran con niveles diferentes, sin un chorro superior visible en las imágenes. Esta serie aporta una observación adicional del estado lógico del controlador, **sin registrar un evento de pulsación de STOP con marca de tiempo**.

| Variable | Captura E16: después de liberar la emergencia | Captura E19: estado actual |
|---|---|---|
| `FO_EMERGENCIA` | FALSE | FALSE |
| `FO_Riego1` | FALSE | FALSE |
| `FO_Riego2` | **TRUE** | **FALSE** |
| `FO_S_DESCARGA1` | FALSE | FALSE |
| `FO_S_DESCARGA2` | **TRUE** | **FALSE** |
| `FO_LEDV` (verde) | **TRUE** | **FALSE** |
| `FO_LEDA` (amarillo) | FALSE | **TRUE** |
| `FO_LEDR` (rojo) | FALSE | FALSE |
| `FO_STOP` | TRUE | TRUE |
| `FO_START` | FALSE | FALSE |
| `FO_Llenado1` / `FO_Llenado2` | 0 / 0 | 0 / 0 |
| `FO_S_NIVEL1` | 5.23745632 | 5.23745632 |
| `FO_S_NIVEL2` | 6.487397 | **5.601132** |

**Interpretación:** la captura de CODESYS registra ambas salidas de riego desactivadas, descargas desactivadas e indicador amarillo encendido, **sin emergencia activa**. Frente al estado anterior de E16, es coherente con una transición a proceso detenido o en espera. `FO_S_NIVEL2` también presenta un valor menor en una captura posterior, pero el dato no permite cuantificar caudal ni demostrar una causa concreta.

**Límite de la evidencia:** `FO_STOP` ya estaba en TRUE en E16 y permanece TRUE en E19. Por tanto, **no puede atribuirse inequívocamente el cambio al accionamiento de STOP** basándose únicamente en esas imágenes. Se recomienda una prueba antes/después en la que se vea cómo cambia el pulsador y su señal en GVL, qué salidas se desactivan y si es necesaria una nueva orden de START. El autor explicó que `FO_STOP=TRUE` corresponde al contacto NC en reposo; queda por verificar la transición a FALSE al pulsarlo y el significado de la indicación amarilla.

Esta prueba documenta estados de una **simulación virtual**, no certifica una función física de seguridad.

## Aclaración del autor: lógica normalmente cerrada de STOP

El autor confirma que configuró el pulsador **STOP como normalmente cerrado (NC)**: `FO_STOP=TRUE` representa la **condición normal de reposo**, en la cual el circuito de parada permanece cerrado; la pulsación debe producir `FO_STOP=FALSE` y solicitar la detención según la lógica del PLC.

Por tanto, las capturas con `FO_STOP=TRUE` durante el riego o durante la emergencia **son coherentes con el diseño declarado** y no indican que STOP esté pulsado o que exista una anomalía.

| Estado previsto | `FO_STOP` | Significado declarado |
|---|---|---|
| Sin pulsar | TRUE | Contacto NC cerrado, parada no solicitada |
| Pulsado | FALSE | Contacto NC abierto, solicitud de parada |

**Alcance de la aclaración:** esta polaridad fue explicada por el autor, pero **la transición `TRUE→FALSE` causada por pulsar STOP no se ha capturado todavía**. Tampoco puede atribuirse a STOP el paso a indicador amarillo en E17–E20: la señal permanece TRUE y no hay evidencia de pulsación. La respuesta ante una solicitud STOP y la necesidad de pulsar START para reanudar quedan pendientes de una prueba dirigida. Un esquema NC habitual no sustituye la validación de seguridad de una instalación física.

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

## Control de versión del proyecto compilado

La barra de título de CODESYS muestra **`Grado.project*`**. El asterisco puede indicar que hay cambios sin guardar. Por tanto, aunque la captura **sí demuestra compilación sin errores de la sesión mostrada**, todavía se debe confirmar que el archivo `Grado.project` guardado dentro de [`02_CODESYS/Codesys.zip`](../02_CODESYS/Codesys.zip) corresponde exactamente a esa revisión. Antes de cerrar el primer punto, guardar la versión definitiva, generar de nuevo el paquete (preferentemente un archivo de proyecto con dependencias) si cambió, y dejar constancia del commit/identificador usado.

## Próximas evidencias mínimas sugeridas

1. **Compilación lograda (E6)**. Conservar el PNG original y, si procede, documentar el significado del icono de advertencia en Ethernet.
2. Ejecutar una prueba corta de **Factory I/O ↔ CODESYS**: accionar `FO_START` y `FO_STOP`; capturar sus cambios en variables, al igual que una salida de válvula y una lectura de nivel.
3. Ejecutar una prueba corta de **Python ↔ CODESYS**: comparar en el mismo instante `Temperatura`, `Precipitacion`, `HumedadSuelo` y `MB_RiegoOn` en ambos lados; comprobar HR0–HR7/IR0.
4. Conservar evidencia del **evento de riego** (inicio y parada alrededor de los umbrales programados) y del histórico guardado; verificar qué señales representan `GVL.Riego` y `GVL.Regando`.
5. Documentar una prueba de **MobileNetV2** con hoja de muestra y umbral 0,90, sin considerarla diagnóstico agronómico definitivo.
6. Conservar las dos capturas E9/E10 de la transición de emergencia y comprobar el comportamiento seguro de las salidas después de activarla.
7. **Rearme observado (E13–E16):** comprobar si `FO_Riego2` se habilita automáticamente al liberar emergencia o requiere orden de START, y corroborar con pulsación la polaridad NC declarada de `FO_STOP`. Las nuevas capturas no muestran chorro de llenado, pero falta corroborar el comportamiento en una prueba sincronizada.
8. Documentar una prueba específica del mando STOP: valor del pulsador y de `FO_STOP` antes y después, salidas desactivadas e indicador amarillo; comprobar posterior START.
9. Publicar las capturas originales, si se desea, en `07_Resultados/evidencias_integracion/` y vincularlas desde este reporte.

## Conclusión

Las veinte capturas son evidencia favorable de **compilación sin errores, aplicación conectada/en ejecución, variables online y conectividad indicada por las interfaces** de los tres componentes. Con ellas se puede sustentar una demostración funcional preliminar para la primera observación del docente. **No son una certificación de ejecución completamente reproducida por terceros, ni prueba de exactitud de las IA**.

El reporte se elaboró a partir de las capturas aportadas por el autor; no se modificaron `Sensores.py`, CODESYS, Factory I/O ni los modelos.
