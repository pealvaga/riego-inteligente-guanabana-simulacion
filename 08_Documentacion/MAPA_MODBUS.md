# Mapa de comunicación Modbus TCP

Mapa contrastado con `01_Python/Sensores.py` (constantes y método `write_all_to_codesys`). **Pendiente de cotejar con el programa de CODESYS.**

| Offset | Dirección convencional | Tipo | Señal | Dirección |
|---:|---:|---|---|---|
| 0 | 40001 | Holding Register | Temperatura × 10 | Python → CODESYS |
| 1 | 40002 | Holding Register | Precipitación × 10 | Python → CODESYS |
| 2 | 40003 | Holding Register | Humedad disponible × 10 | Python → CODESYS |
| 3 | 40004 | Holding Register | Heartbeat | Python → CODESYS |
| 4 | 40005 | Holding Register | Tipo de riego (0, 1 o 2) | Python → CODESYS |
| 5 | 40006 | Holding Register | Día simulado | Python → CODESYS |
| 6 | 40007 | Holding Register | Hora simulada | Python → CODESYS |
| 7 | 40008 | Holding Register | Minuto simulado | Python → CODESYS |
| 0 | 30001 | Input Register | Estado del riego (0 o 1) | CODESYS → Python |

La función `write_all_to_codesys` envía en una operación los ocho valores desde HR0. El código de Python lee IR0 para saber si el controlador está regando y actualizar el balance hídrico. El estado de tipo de riego se decide desde la IA foliar (HR4 = 0 sin decisión, 1 normal, 2 fertirriego). La lógica definitiva de actuación, prioridad y paradas debe comprobarse en CODESYS.

Configuración inicial de Python: `127.0.0.1:502`, Device ID 1, ajustable desde la pestaña de Modbus. Se intenta la compatibilidad con variantes de `pymodbus` que emplean `device_id` o `slave` en llamadas a registros.

## Correspondencia con el informe

La Tabla 1 del documento escrito, pp. 33–34, **solo enumera HR0–HR4 e IR0**, aunque `Sensores.py` también envía HR5, HR6 y HR7 para el reloj simulado. Esta diferencia deberá reconciliarse en la próxima edición del documento.
