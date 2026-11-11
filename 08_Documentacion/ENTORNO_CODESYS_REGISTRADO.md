# Entorno CODESYS identificado mediante capturas de «Información de versión»

## Versión del sistema de programación

**CODESYS V3.5 SP9 Patch 1**. La ventana «Acerca de» muestra la denominación **«CODESYS V3.5 SP9 Patch 1 +»**; las ventanas «Información de versión» muestran **«CODESYS V3.5 SP9 Patch 1»**.

La información se transcribió de las capturas del cuadro «Acerca de» y del listado de componentes aportadas por el autor. **No constituye una comprobación de instalación efectuada por el revisor** ni demuestra que el proyecto haya sido compilado o ejecutado.

| Componente observado | Versión mostrada |
|---|---|
| DataSource Editor | 3.5.9.0 |
| DataSource Object | 3.5.9.0 |
| Default Gateway client | 3.5.9.0 |
| Device Categories | 3.5.9.0 |
| Device CIP | 3.5.9.10 |
| Device Communication Editor | 3.5.9.0 |
| Device Modbus Serial Slave | 3.5.9.10 |
| **Device Modbus TCP Slave** | **3.5.9.10** |
| Device Ethernet Adapter | 3.5.9.0 |
| Device EtherCAT | 3.5.9.10 |
| Engine | 3.5.9.10 |
| Device SoftMotion (ext) | 4.0.0.0 |
| Project Archive | 3.5.9.10 |
| Symbol Configuration Object | 3.5.9.10 |
| ST Editor | 3.5.9.0 |
| ST Implementation Object | 3.5.9.0 |
| Festo.PlcDiagnosis (ext) | 3.5.7.48 |
| Festo.CpxCEC (ext) | 3.5.7.48 |
| Festo.CoDeSys.Management (...) | 3.5.7.48 |
| Festo.DeviceEditorCPX (ext) | 3.5.7.48 |

Las imágenes muestran una lista parcial de componentes instalados, desplazada verticalmente. La tabla es **selectiva** y no pretende sustituir una exportación completa del listado. No todos los componentes observados tienen por qué ser dependencias del proyecto `Grado.project`.

## Información de sistema mostrada por CODESYS

En «Información de versión» se lee:

- `Versión SO: Microsoft Windows NT 6.2.9200.0`.
- `Versión .NET: 4.0.30319.42000`.

**Precaución:** el identificador de Windows NT mostrado por la aplicación no demuestra necesariamente la edición/versión actual del sistema operativo instalado; las capas de compatibilidad y los mecanismos de detección de Windows pueden mostrar valores distintos. Para documentar la versión real de Windows, consultar la herramienta del sistema (`winver`).

## Correspondencia con el proyecto publicado

Los componentes **3.5.9.0** y **3.5.9.10** vistos en las capturas concuerdan con las referencias internas observadas previamente en `02_CODESYS/Codesys.zip`. La presencia de **Device Modbus TCP Slave 3.5.9.10** resulta relevante porque el proyecto contiene un servidor Modbus TCP que comunica con Python en el puerto 502.

Esta coincidencia respalda la identificación del entorno de programación, pero no certifica:

1. Que el paquete `Grado.project` abra sin avisos de actualización o bibliotecas faltantes.
2. Qué versión concreta de **CODESYS Control Win V3**, runtime/servicio de ejecución, bibliotecas IEC y servidor **OPC DA `CoDeSys.OPC.DA`** se encuentran instalados y activos.
3. Que compile correctamente, se encuentre en ejecución o que los registros Modbus HR0–HR7/IR0 intercambien valores.
4. Que Factory I/O reciba correctamente los 14 símbolos OPC DA.
5. Que `HistorialCultivo.csv` se genere en el sistema de ejecución.

## Evidencia recomendada para completar

- Una captura del proyecto `Grado.project` abierto y **compilado sin errores**, con fecha de prueba.
- Captura de **CODESYS Control Win V3** en línea, aplicación en RUN, e identificación de la versión del runtime si aparece.
- Captura de la asignación **Modbus TCP Slave** (puerto 502, HR0–HR7/IR0) y lectura/escritura real desde Python.
- Captura del administrador de bibliotecas del proyecto, con versiones **realmente utilizadas** por `Grado.project`, no solo el catálogo instalado.
- Captura del enlace **OPC DA** desde Factory I/O y de la recepción de las variables.
- Captura del archivo `HistorialCultivo.csv` generado en una sesión.

La [guía integral](GUIA_REPRODUCCION_INTEGRAL.md) contiene el orden propuesto para comprobar esos elementos. Las imágenes de «Acerca de» se recibieron en la conversación; **no están publicadas como archivos binarios dentro de este repositorio**. Este documento registra los datos visibles en ellas para la trazabilidad de versiones.

**Estado:** versión del IDE y componentes relevantes documentados; versión del runtime y pruebas de funcionamiento pendientes.
