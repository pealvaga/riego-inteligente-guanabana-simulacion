# Mapa Modbus TCP documentado

Direcciones según la Tabla 1 de la versión V9(3) del trabajo de grado (pp. 33–34). **Verificar contra el código final:** puede haber registros adicionales para el reloj simulado.

| Offset Python | Dirección habitual | Tipo | Variable | Flujo |
|---:|---:|---|---|---|
| 0 | 40001 | Holding Register | Temperatura | Python → CODESYS |
| 1 | 40002 | Holding Register | Precipitación | Python → CODESYS |
| 2 | 40003 | Holding Register | Humedad del suelo | Python → CODESYS |
| 3 | 40004 | Holding Register | Heartbeat | Python → CODESYS |
| 4 | 40005 | Holding Register | Tipo de riego | Python → CODESYS |
| 0 | 30001 | Input Register | Riego activo (0/1) | CODESYS → Python |

Temperatura, precipitación y humedad se multiplican por diez antes de transmitirlas y se dividen entre diez al recibirlas en CODESYS.

Tipo de riego: 0 = sin decisión; 1 = normal; 2 = fertirriego.
