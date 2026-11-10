# Controlador virtual, automatización y SCADA — CODESYS

## Proyecto fuente

El paquete [Codesys.zip](Codesys.zip) contiene el proyecto **Grado.project**, la configuración de símbolos `Grado.Device.Application.xml` y archivos auxiliares generados por el entorno de CODESYS. El paquete fue verificado íntegro (sin errores de extracción).

**Identidad del archivo ZIP (SHA-256):**
`5d0eeeca385fd6437f93a5bc6c887b8fa57304a7dda9498cdc42dfb0102cd60c`

**Identidad del proyecto `Grado.project` (SHA-256):**
`670603ca32ab3f241f4c226eb9047cd0f57489dd9531abac82326fd297b79093`

Los metadatos internos incluyen referencias a componentes CODESYS **3.5.9.0 / 3.5.9.10**; la versión exacta del entorno y los paquetes instalados deberá registrarse desde CODESYS para facilitar una apertura reproducible.

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

El archivo `Grado.Device.Application.xml` declara como símbolos `ReadWrite` las variables:

`FO_EMERGENCIA`, `FO_LEDA`, `FO_LEDR`, `FO_LEDV`, `FO_Llenado1`, `FO_Llenado2`, `FO_Riego1`, `FO_Riego2`, `FO_S_DESCARGA1`, `FO_S_DESCARGA2`, `FO_S_NIVEL1`, `FO_S_NIVEL2`, `FO_START`, `FO_STOP`.

Las vinculaciones y su ejecución efectiva deben comprobarse con la escena de Factory I/O correspondiente.

## Reproducción en CODESYS

1. Extraer `Codesys.zip` y abrir `Grado.project`.
2. Comprobar versiones, bibliotecas y dispositivos; instalar los elementos que requiera el proyecto.
3. Compilar y ejecutar el controlador virtual.
4. Verificar la asignación de registros Modbus y la exposición de símbolos.
5. Vincular la escena Factory I/O y conectar la aplicación Python.
6. Comprobar las reglas de control y la escritura de `HistorialCultivo.csv`.
7. Documentar las versiones definitivas y guardar evidencias de una ejecución completa.
