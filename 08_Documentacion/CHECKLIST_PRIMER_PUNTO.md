# Lista de verificación — primera observación del docente

## Objetivo del primer punto

Publicar una versión **identificable y reproducible** del proyecto de simulación: fuentes, proyectos editables, modelos, datos pertinentes, entrenamiento, configuración, instrucciones y evidencia de funcionamiento. La existencia de los archivos en GitHub no demuestra automáticamente que el software funcione en otro equipo.

**Convención:** `[x]` = artefacto publicado o documentación preparada; `[ ]` = comprobación o entrega todavía pendiente. Esta lista no certifica ejecución física ni resultados de modelos.

| Elemento | Estado | Ubicación y comprobación pendiente |
|---|---|---|
| Repositorio público con descripción y componentes | [x] | [README principal](../README.md) |
| Python original del sistema | [x] | [`Sensores.py`](../01_Python/Sensores.py) |
| Proyecto CODESYS editable | [x] | [`Codesys.zip`](../02_CODESYS/Codesys.zip), contiene `Grado.project` |
| Escena editable Factory I/O | [x] | [`Grado.factoryio`](../03_Factory_IO/Grado.factoryio) |
| Código de entrenamiento MobileNetV2 y modelo `.keras` | [x] | [`05_MobileNetV2/`](../05_MobileNetV2/) |
| Acceso documentado a imágenes y fuentes | [x] | [README MobileNetV2](../05_MobileNetV2/README.md); comprobar permisos y licencias |
| Inventario de imagen, duplicados y trazabilidad parcial | [x] | [`06_Datos/`](../06_Datos/); completar especie, fuente y etiqueta original |
| Script y cuaderno de RF en carpeta separada | [x] | [`04_Random_Forest/`](../04_Random_Forest/) |
| Excel inicial de registros RF | [x] | [`06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx) |
| Cuaderno que prepara múltiples sesiones RF | [x] | [`RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb), pendiente de ejecución sobre datos finales |
| Guía de ejecución integrada | [x] | [`GUIA_REPRODUCCION_INTEGRAL.md`](GUIA_REPRODUCCION_INTEGRAL.md) |
| Captura de versiones instaladas de Python y paquetes | [x] | [`ENTORNO_EJECUTADO.json`](ENTORNO_EJECUTADO.json): CPython 3.12.9, Windows AMD64. **Pendiente confirmar** que es el mismo intérprete con que se ejecuta el sistema y completar `pip freeze` |
| Versión del IDE CODESYS y componentes mostrados | [x] | [Registro del entorno CODESYS](ENTORNO_CODESYS_REGISTRADO.md): V3.5 SP9 Patch 1; Device Modbus TCP Slave 3.5.9.10 |
| Versión del runtime CODESYS Control Win V3 | [x] | [Control Win **3.5.9.10**](VERSIONES_SOFTWARE_CONFIRMADAS.md), confirmada por captura de pantalla de inicio |
| OPCConfig: versión instalada | [x] | [**3.5.9.0**](VERSIONES_SOFTWARE_CONFIRMADAS.md); **no es prueba de enlace OPC DA** |
| Versión instalada de Factory I/O | [x] | [**2.5.10**](VERSIONES_SOFTWARE_CONFIRMADAS.md), confirmada por pantalla Update Checker |
| Compilación de CODESYS sin errores ni advertencias | [x] | [Evidencia E6](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): **0 errores, 0 advertencias**, 3 mensajes informativos |
| CODESYS conectado y aplicación en ejecución | [x] | Captura con `Device [Conectado]` y `Application [ejecutar]` |
| Monitorización GVL con valores del proceso | [x] | Captura E8: `FO_Riego1=TRUE`, `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644`, `MB_Temp=350` |
| Bibliotecas del proyecto y diagnóstico de Ethernet | [ ] | Registrar bibliotecas realmente usadas y verificar el icono de advertencia Ethernet |
| Conexión y driver OPC DA de Factory I/O | [ ] | Confirmar conexión real con `CoDeSys.OPC.DA` y 14 señales; no basta con identificar versiones |
| Evidencia visual de ejecución integrada | [x] | [Revisión de veinte capturas](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): incluye compilación CODESYS sin errores, variables GVL, Python Modbus OK y Factory I/O OPC DA (14) conectado; **falta publicar los PNG** |
| Cambio observado FO_EMERGENCIA en CODESYS | [x] | [Capturas E8 y E10](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): antes **FALSE**, después **TRUE**, junto con captura del pulsador de emergencia en Factory I/O; falta comprobar el efecto sobre salidas |
| Desactivación de salidas de riego con emergencia activa | [x] | [Comparación E8/E12](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_Riego1` TRUE→FALSE, `FO_Riego2` FALSE, `FO_S_DESCARGA1` TRUE→FALSE, `FO_LEDR` FALSE→TRUE. Evidencia visual de secuencia, no certificación de seguridad. |
| Rearme observado en simulación después de emergencia | [x] | [E14/E16](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_EMERGENCIA` TRUE→FALSE, `FO_LEDR` TRUE→FALSE, `FO_LEDV` FALSE→TRUE, `FO_Riego2` FALSE→TRUE |
| Estado sin riego e indicador amarillo observado | [x] | [E16/E19](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_Riego2` TRUE→FALSE, `FO_S_DESCARGA2` TRUE→FALSE, `FO_LEDA` FALSE→TRUE, sin emergencia activa |
| Polaridad prevista de STOP documentada | [x] | El autor confirma pulsador **normalmente cerrado (NC)**: `FO_STOP=TRUE` en reposo, `FALSE` esperado al pulsarlo. Ver [aclaración técnica](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md). |
| Efecto específico de pulsar STOP y orden START | [ ] | Registrar transición **TRUE→FALSE** al pulsar, verificar salidas/indicador amarillo y si se exige START para reactivar; aún sin captura dinámica de esa pulsación |
| Confirmar lógica de reinicio, pulsador STOP y llenado | [ ] | El autor declara que `FO_STOP=TRUE` es **reposo del pulsador NC**. Verificar en ejecución la pulsación TRUE→FALSE y si el riego se habilita automáticamente al soltar emergencia o requiere START. No se ve chorro de llenado en las nuevas capturas, pero falta prueba sincronizada |
| Demostración de instalación desde cero y validación funcional detallada | [ ] | Registrar compilación, errores, verificación individual de señales y evidencia de arranque en otra instalación o desde cero |
| `.pkl` RF definitivo, trazable y validado | [ ] | El artefacto publicado aún no tiene validación satisfactoria confirmada |
| Excel consolidado final de RF y particiones | [ ] | Exportar y publicar desde nuevo cuaderno, conservar sesiones y criterios de filtrado |
| Resultados RF de la misma ejecución: CSV, JSON y comparación con persistencia | [ ] | Publicar en `07_Resultados/`, además del error de próximo riego si se presenta |
| Evaluación independiente del checkpoint MobileNetV2 a 0,90 | [ ] | Completar matrices, métricas y procedencia de particiones |
| Imágenes originales de prueba y resultados cuantitativos completos | [ ] | Publicar las 20 capturas originales en `07_Resultados/`, más pruebas detalladas, registros, condiciones y versiones; véase [informe preliminar](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md) |
| Coherencia documental CODESYS/Factory I/O/tesis | [ ] | Corregir OPC DA versus OPC UA, límites de histéresis y mapa HR/IR según uso real |
| Enlace de GitHub e instrucciones incorporados en Anexo C del documento | [ ] | Comprobar que apunte a la revisión final y a las rutas correctas |

## Trabajo que puede completarse mientras se generan datos RF

- Capturar versiones de Python, scikit-learn, TensorFlow, pymodbus y demás dependencias **desde el ordenador donde funciona el sistema**.
- Obtener capturas de CODESYS compilado, visualización SCADA, configuración Modbus, Factory I/O y estado de OPC DA.
- Probar la secuencia de instalación/ejecución con la [guía integral](GUIA_REPRODUCCION_INTEGRAL.md), dejando constancia de pasos que deban corregirse.
- Completar la trazabilidad y licencias del conjunto de imágenes, revisando la disponibilidad del Drive y las fuentes oficiales.
- Preparar el inventario de pruebas/escenarios e identificar cada ejecución con fecha, hora simulada y versiones.
- Corregir el texto del documento de grado para que describa exactamente el código y los protocolos finales.

## Precauciones para nuevos registros con humedad igual a 0

En la simulación, `HumedadSuelo` es el **porcentaje de agua disponible** calculado según el balance hídrico, no humedad volumétrica directa. Por tanto, `0 %` representa el límite inferior de agua disponible del modelo y debe etiquetarse así. Guardar únicamente trayectorias coherentes con las reglas de simulación; no alterar arbitrariamente columnas para introducir ceros artificiales. Generar escenarios diversos (secos, con lluvia y con riego), con estados de Modbus válidos y sin mezclar sesiones al construir rezagos.

La primera observación se considerará cerrada cuando otro evaluador pueda **acceder a los componentes, reconstruir el entorno y repetir los pasos documentados**, con las limitaciones y resultados medidos claramente identificados. La segunda observación exige además validez metodológica de las evaluaciones de IA y comparación con las referencias.
