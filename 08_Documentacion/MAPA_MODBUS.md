# Mapa de comunicación Modbus TCP

La aplicación Python `01_Python/Sensores.py` actúa como **cliente Modbus TCP**, mientras que el proyecto CODESYS incluye un dispositivo **Modbus TCP Slave**, que funciona como servidor. El puerto configurado en el proyecto es **502**.

La tabla corresponde a los offsets enviados y leídos por `Sensores.py`. El proyecto de CODESYS contiene las variables homólogas; para certificar el mapeo físico se debe revisar en línea la asignación de registros del dispositivo.

| Offset Python | Dirección convencional | Área | Señal | Flujo |
|---:|---:|---|---|---|
| 0 | 40001 | Holding Register | Temperatura × 10 (`MB_Temp`) | Python → CODESYS |
| 1 | 40002 | Holding Register | Precipitación × 10 (`MB_Lluvia`) | Python → CODESYS |
| 2 | 40003 | Holding Register | Agua disponible × 10 (`MB_Hum`) | Python → CODESYS |
| 3 | 40004 | Holding Register | Heartbeat (`MB_Heartbeat`) | Python → CODESYS |
| 4 | 40005 | Holding Register | Tipo de riego (`MB_Tiporiego`) | Python → CODESYS |
| 5 | 40006 | Holding Register | Día simulado (`MB_DIA`) | Python → CODESYS |
| 6 | 40007 | Holding Register | Hora simulada (`MB_HORA`) | Python → CODESYS |
| 7 | 40008 | Holding Register | Minuto simulado (`MB_MINUTO`) | Python → CODESYS |
| 0 | 30001 | Input Register | Estado de riego (`MB_RiegoOn`) | CODESYS → Python |

**Escalamiento:** Python multiplica temperatura, precipitación y humedad por 10 y transmite enteros. CODESYS reconstruye sus valores mediante `WORD_TO_REAL(...) / 10.0`.

**Tipo de riego:** 0 = sin decisión; 1 = normal; 2 = fertirriego. En el código Python el tipo 2 se habilita cuando la clasificación foliar supera el umbral operativo del 90 %.

**Condición de ejecución:** revisar que las señales del histórico, del estado de riego y de la planta virtual correspondan a las mismas variables que el intercambio Modbus y que el dispositivo use los offsets indicados.

La Tabla 1 del trabajo de grado V9(3) registra HR0–HR4 e IR0, pero `Sensores.py` también utiliza HR5–HR7 para el reloj simulado. La tabla del documento deberá actualizarse para reflejar el mapeo completo.
