# Controlador virtual, automatización y SCADA — CODESYS

## Proyecto fuente

El paquete [Codesys.zip](Codesys.zip) contiene el proyecto **Grado.project**, la configuración de símbolos `Grado.Device.Application.xml` y archivos auxiliares generados por el entorno de CODESYS. El paquete fue verificado íntegro (sin errores de extracción).

**Identidad del archivo ZIP (SHA-256):**
`5d0eeeca385fd6437f93a5bc6c887b8fa57304a7dda9498cdc42dfb0102cd60c`

**Identidad del proyecto `Grado.project` (SHA-256):**
`670603ca32ab3f241f4c226eb9047cd0f57489dd9531abac82326fd297b79093`

Los metadatos internos incluyen referencias a componentes CODESYS **3.5.9.0 / 3.5.9.10**. Las capturas del entorno de programación muestran **CODESYS V3.5 SP9 Patch 1** (la ventana de inicio muestra «Patch 1 +»), con **Device Modbus TCP Slave 3.5.9.10**, **Engine 3.5.9.10** y otros componentes. Ver el [registro de versiones CODESYS](../08_Documentacion/ENTORNO_CODESYS_REGISTRADO.md). La versión de **CODESYS Control Win V3** quedó identificada por captura como **3.5.9.10** y la herramienta **OPCConfig** como **3.5.9.0**. Ver el [resumen de versiones](../08_Documentacion/VERSIONES_SOFTWARE_CONFIRMADAS.md). El estado RUN, las bibliotecas utilizadas por el proyecto y la conexión OPC DA siguen pendientes de prueba.

## Contenido identificado

| Archivo interno | Finalidad |
|---|---|
| `Grado.project` | Proyecto editable en formato propietario CODESYS |
| `Grado.Device.Application.xml` | Configuración de símbolos exportados para la integración |
| `*.opt` | Preferencias locales del entorno |
| `*.bootinfo` / `*.compileinfo` | Archivos auxiliares de compilación y aplicación |

Las preferencias `*.opt` y los auxiliares generados no sustituyen el proyecto fuente. Para distribución profesional conviene conservar también una exportación **Project Archive** de CODESYS con las dependencias, cuando la herramienta lo permita.

## Programas de aplicación

Se identificaron los programas:

- **`OPERACIONES`**: conversión de variables recibidas por Modbus y lógica de humedad; fragmentos del proyecto utilizan `WORD_TO_REAL(GVL.MB_Temp/MB_Lluvia/MB_Hum) / 10.0`.
- **`RIEGO`**: selección y accionamiento de modalidades normal/fertirriego con señal `GVL.MB_Tiporiego` y variables de la planta virtual.
- **`REGISTRO_DATOS`**: máquina de estados con bloques `FILE.Open`, `FILE.GetSize`, `FILE.Write` y `FILE.Close` para mantener un historial CSV.
- **`PLC_PRG`** y tarea principal **`MainTask`**: la configuración del proyecto incluye una tarea cíclica con intervalo `T#20ms`.

La lectura del formato propietario permite recuperar los nombres y fragmentos de programación, pero no reemplaza la compilación ni una revisión de ejecución dentro de CODESYS.

## Comunicación Modbus TCP

El proyecto contiene un dispositivo **Modbus TCP Slave** (servidor) con puerto configurado **502** y áreas de registros Holding/Input. También están identificadas variables `MB_Temp`, `MB_Lluvia`, `MB_Hum`, `MB_Heartbeat`, `MB_Tiporiego`, `MB_DIA`, `MB_HORA`, `MB_MINUTO` y `MB_RiegoOn`.

La aplicación [Sensores.py](../01_Python/Sensores.py) escribe **HR0–HR7** y consulta **IR0**. Confirmar en la asignación de E/S del dispositivo de CODESYS que los offsets se corresponden exactamente; consultar [mapa Modbus](../08_Documentacion/MAPA_MODBUS.md).

## Control de riego

En el proyecto aparecen las condiciones:

```iecst
IF (GVL.Humedad < 60) THEN
    GVL.Riego := 1;
END_IF;

IF (GVL.Humedad > 75) THEN
    GVL.Riego := 0;
END_IF;
```

Estos extractos reflejan desigualdades **estrictas**. El documento académico utiliza `<= 60` y `>= 75` en la explicación. Para que ambas fuentes sean coherentes, se debe verificar el control efectivo en CODESYS y normalizar la redacción o el programa.

En los fragmentos del proyecto también se observa `GVL.MB_RiegoOn := BOOL_TO_WORD(GVL.Regando)`. La equivalencia entre `GVL.Riego`, `GVL.Regando` y las salidas de los actuadores debe probarse en línea.

## Registro histórico para análisis de datos

El programa `REGISTRO_DATOS` utiliza CAA File, genera el archivo **`HistorialCultivo.csv`** y contempla una frecuencia de **10 minutos simulados**. El encabezado, separado por **punto y coma**, es:

```text
Dia;Hora;Minuto;Temperatura;Precipitacion;HumedadSuelo;NivelAgua;NivelNutrientes;RiegoActivo;TipoRiego
```

Las filas se construyen con valores recibidos por Modbus, mediciones del controlador y niveles de tanques de Factory I/O. Se identificó el modo de apertura `FILE.MODE.MAPPD` para anexar registros y una condición `MB_MINUTO MOD 10 = 0` combinada con el cambio de minuto simulado.

**Consideraciones para reentrenamiento:** verificar la ruta real donde escribe CODESYS, comprobar que el historial se genera en una ejecución completa, y **separar las sesiones de simulación** (en especial tras reiniciar el reloj a día 1). El encabezado original no contiene un identificador de sesión; ese identificador puede añadirse durante la preparación de la base, manteniendo trazabilidad de cada archivo de origen.

La columna `RiegoActivo` se construye según un fragmento que consulta `GVL.Riego`; Python, en cambio, lee `GVL.MB_RiegoOn` producido desde `GVL.Regando`. Comparar estas señales antes de utilizarlas como etiquetas de entrenamiento.

## Integración con Factory I/O

La escena [`Grado.factoryio`](../03_Factory_IO/Grado.factoryio) ha sido inspeccionada. Contiene dos tanques, controles, una torre luminosa y **14 vínculos OPC Client DA** al servidor `CoDeSys.OPC.DA`. El archivo no muestra un enlace OPC UA equivalente; las referencias a OPC UA del informe deberán revisarse frente a la configuración efectivamente guardada. La disponibilidad del servidor OPC DA debe comprobarse al ejecutar CODESYS y Factory I/O.


El archivo `Grado.Device.Application.xml` declara como símbolos `ReadWrite` las variables:

`FO_EMERGENCIA`, `FO_LEDA`, `FO_LEDR`, `FO_LEDV`, `FO_Llenado1`, `FO_Llenado2`, `FO_Riego1`, `FO_Riego2`, `FO_S_DESCARGA1`, `FO_S_DESCARGA2`, `FO_S_NIVEL1`, `FO_S_NIVEL2`, `FO_START`, `FO_STOP`.

Los 14 símbolos de la escena coinciden por nombre con la lista de señales `FO_*` del proyecto CODESYS. La ejecución y comunicación efectivas aún deben validarse en ambos entornos abiertos.

## Evidencia de compilación y señales en ejecución

Una captura reciente del proyecto `Grado.project` abierto en CODESYS muestra el panel de compilación de `Device.Application`: **0 errores y 0 advertencias** (3 mensajes informativos), con «The application is up to date». El árbol muestra `Device [Conectado]` y `Application [ejecutar]`.

Otra captura del monitor en línea `Device.Application.GVL` muestra, entre otras variables, `FO_Riego1=TRUE`, `FO_Riego2=FALSE`, `FO_S_DESCARGA1=TRUE`, `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644` y `MB_Temp=350`, valor coherente con la temperatura mostrada en Python (**35,0 °C** con escala ×10).

Estas capturas evidencian compilación y valores instantáneos, pero no sustituyen una prueba **antes/después** del cambio de señales OPC ni la comprobación del icono de advertencia presente en el dispositivo Ethernet. Consultar el [informe de ejecución integrada](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md). Las imágenes originales aún están pendientes de publicación en GitHub.

## Lógica declarada del pulsador STOP

El pulsador `FO_STOP` se configuró como **normalmente cerrado (NC)**: `TRUE` corresponde al contacto sin pulsar y `FALSE` al contacto accionado. El valor `FO_STOP=TRUE` mostrado en capturas mientras el sistema funciona es, por tanto, **coherente con la configuración del sistema**; no indica una orden de parada.

Se recomienda comprobar la transición `TRUE→FALSE` accionando el pulsador en Factory I/O y verificando su efecto en CODESYS, junto con el comportamiento de arranque/rearme. La declaración sobre la polaridad no equivale a una prueba de seguridad funcional. Ver [registro de evidencias](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

## Reproducción en CODESYS

1. Extraer `Codesys.zip` y abrir `Grado.project`.
2. Comprobar versiones, bibliotecas y dispositivos; instalar los elementos que requiera el proyecto.
3. Compilar y ejecutar el controlador virtual.
4. Verificar la asignación de registros Modbus y la exposición de símbolos.
5. Vincular la escena Factory I/O y conectar la aplicación Python.
6. Comprobar las reglas de control y la escritura de `HistorialCultivo.csv`.
7. Documentar las versiones definitivas y guardar evidencias de una ejecución completa.
