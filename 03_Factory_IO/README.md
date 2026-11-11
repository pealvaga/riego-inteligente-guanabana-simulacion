# Escena de Factory I/O — planta de riego simulada

## Archivo de la escena

[Grado.factoryio](Grado.factoryio) contiene la escena utilizada para representar los componentes físicos virtuales del sistema de riego. El encabezado del archivo identifica **Factory I/O 2.5.10** y la descripción `Proyecto de grado, simulación de riego`. Una captura posterior de «Update Checker» confirma que la versión **instalada en el equipo también es 2.5.10**. Consultar el [registro de versiones](../08_Documentacion/VERSIONES_SOFTWARE_CONFIRMADAS.md).

## Elementos de la escena

| Elemento virtual | Cantidad | Señales asociadas |
|---|---:|---|
| Tanques con medición de nivel, caudal, llenado y descarga | 2 | Nivel, caudal, válvula de llenado y válvula de descarga de cada tanque |
| Tablero eléctrico | 1 | Soporte de controles |
| Pulsador de inicio | 1 | `FO_START` |
| Pulsador de parada | 1 | `FO_STOP` |
| Pulsador de emergencia | 1 | `FO_EMERGENCIA` |
| Torre luminosa de tres colores | 1 | `FO_LEDR`, `FO_LEDA`, `FO_LEDV` |
| Pilar de soporte | 1 | Elemento de la escena sin señal asociada |

Los tanques están identificados como `Tank 0` y `Tank 1` en el archivo de Factory I/O. La asignación funcional de tanque de agua y tanque de nutrientes debe interpretarse junto con el programa CODESYS, no solamente a partir de los índices de Factory I/O.

## Comunicación con CODESYS: OPC DA

**La escena entregada incluye una configuración de `OPCClientDA` (OPC clásico/DA), no una configuración explícita de OPC UA.** En el archivo se encuentran:

- Servidor: `CoDeSys.OPC.DA`
- Prefijo de variables: `PLC1.Application.GVL.`
- Número de elementos vinculados: **14**
- Identificador guardado de controlador: `CurrentDriver="16384"`

Este resultado corrige referencias anteriores que describían el vínculo Factory I/O–CODESYS como OPC UA sin verificar la escena. La configuración efectiva y el funcionamiento del servidor deben probarse al abrirla en Factory I/O. **OPC DA no es intercambiable con OPC UA**; si se migra de protocolo habrá que modificar y validar la conexión.

### Variables vinculadas

| Variable de CODESYS | Función en la escena | Sentido lógico |
|---|---|---|
| `FO_START` | Pulsador de inicio | Factory I/O → PLC |
| `FO_STOP` | Pulsador de parada | Factory I/O → PLC |
| `FO_EMERGENCIA` | Parada de emergencia | Factory I/O → PLC |
| `FO_S_NIVEL1`, `FO_S_NIVEL2` | Medición de nivel de los dos tanques | Factory I/O → PLC |
| `FO_S_DESCARGA1`, `FO_S_DESCARGA2` | Medición de caudal/descarga | Factory I/O → PLC |
| `FO_Llenado1`, `FO_Llenado2` | Válvulas de llenado | PLC → Factory I/O |
| `FO_Riego1`, `FO_Riego2` | Válvulas de descarga de los tanques | PLC → Factory I/O |
| `FO_LEDR`, `FO_LEDA`, `FO_LEDV` | Indicadores rojo, amarillo y verde | PLC → Factory I/O |

Los nombres y rutas están tomados de `Item0` a `Item13` del bloque `OPCClientDA` guardado en la escena. El paquete de CODESYS incluye la configuración de símbolos correspondientes.

## Ejecución y comprobación

1. Descargar `Grado.factoryio` y abrirlo con una versión compatible de Factory I/O (el archivo indica 2.5.10).
2. Abrir el proyecto [`Grado.project`](../02_CODESYS/README.md) y poner en ejecución su controlador virtual.
3. En Factory I/O, comprobar la configuración del controlador OPC DA y la disponibilidad del servidor `CoDeSys.OPC.DA`.
4. Confirmar que el servidor expone las 14 variables `PLC1.Application.GVL.FO_*` con los nombres esperados.
5. Accionar inicio, parada y emergencia y comprobar su lectura desde CODESYS.
6. Verificar que niveles, caudales, luces y válvulas responden a las variables del controlador.
7. Conectar por separado la aplicación Python con el servidor **Modbus TCP** de CODESYS.

**Alcance de esta revisión:** se comprobó la estructura y el mapeo almacenados en el archivo de escena. No se ha realizado aquí una sesión de Factory I/O y CODESYS ejecutándose simultáneamente.

## Relación con el SCADA

Factory I/O presenta la planta virtual; CODESYS implementa el control y el monitoreo HMI/SCADA; Python simula el clima y la dinámica hídrica. Así se separan la representación del proceso, la lógica de actuación y la generación de variables ambientales.
