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
| Runtime CODESYS Control Win y bibliotecas usadas por el proyecto | [ ] | Verificar en línea el runtime y las bibliotecas de `Grado.project`; capturar compilación sin errores |
| Versión/driver activo y prueba OPC DA de Factory I/O | [ ] | Confirmar conexión con `CoDeSys.OPC.DA` y 14 señales |
| Demostración de instalación desde cero | [ ] | Registrar errores, ajustes y evidencia de arranque de las tres plataformas |
| `.pkl` RF definitivo, trazable y validado | [ ] | El artefacto publicado aún no tiene validación satisfactoria confirmada |
| Excel consolidado final de RF y particiones | [ ] | Exportar y publicar desde nuevo cuaderno, conservar sesiones y criterios de filtrado |
| Resultados RF de la misma ejecución: CSV, JSON y comparación con persistencia | [ ] | Publicar en `07_Resultados/`, además del error de próximo riego si se presenta |
| Evaluación independiente del checkpoint MobileNetV2 a 0,90 | [ ] | Completar matrices, métricas y procedencia de particiones |
| Archivos con métricas y evidencia visual del sistema en ejecución | [ ] | [`07_Resultados/`](../07_Resultados/) con datos, fecha, condiciones y versiones |
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
