# Inventario y trazabilidad

Inventario provisional para organizar la evidencia de reproducción. Cada artefacto final debería registrar versión, origen, configuración, entradas, salidas, fecha y, cuando aplique, huella SHA-256.

| Artefacto | Estado | Verificación pendiente |
|---|---|---|
| `01_Python/Sensores.py` | Incorporado y revisado estáticamente | Ejecución en entorno limpio, registro de versiones |
| `01_Python/requirements.txt` | Incorporado, sin fijar versiones | Confirmar versiones del entorno del autor |
| CODESYS | No incorporado | Proyecto, bibliotecas, PLC virtual, HMI y registro |
| Factory I/O | No incorporado | Escena, configuración OPC UA |
| CSV de simulación | No incorporado | Esquema, sesiones, origen y seguimiento de trayectorias |
| Random Forest | No incorporado | Script, partición, parámetros, evaluación y modelo |
| MobileNetV2 | No incorporado | Modelo, etiquetas, partición, scripts y umbral 0,90 |
| Datasets originales | No incorporados | Fuentes, cantidades, clases y permisos de uso |

Ver [hallazgos y limitaciones actuales](ESTADO_REPRODUCIBILIDAD.md).

No se debe declarar una evaluación reproducida hasta verificar insumos, configuración y resultados.
