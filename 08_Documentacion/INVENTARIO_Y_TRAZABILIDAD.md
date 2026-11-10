# Inventario técnico y trazabilidad

Cada artefacto del sistema se relaciona con su función, parámetros de configuración, fuente y evidencia.

| Componente | Artefacto | Trazabilidad técnica |
|---|---|---|
| Simulación ambiental | [Sensores.py](../01_Python/Sensores.py) | Balance hídrico, parámetros, mapa Modbus, interfaz y carga de modelos |
| Controlador y SCADA | [Codesys.zip](../02_CODESYS/Codesys.zip) | `Grado.project`, programas `OPERACIONES`, `RIEGO` y `REGISTRO_DATOS`, controlador virtual y símbolos |
| Planta virtual | [03_Factory_IO](../03_Factory_IO/) | Escena, símbolos y vinculación con CODESYS |
| Predicción de humedad | [04_Random_Forest](../04_Random_Forest/) | Datos, particiones, código de entrenamiento, modelo y evaluación |
| Clasificación foliar | [05_MobileNetV2](../05_MobileNetV2/) | Etiquetas, modelo, particiones y resultados |
| Datos | [06_Datos](../06_Datos/) | Procedencia, sesiones, licencias, esquema y separación temporal |
| Resultados | [07_Resultados](../07_Resultados/) | Comparaciones, métricas y evidencias por versión |

## Identificación del proyecto de controlador

- Archivo: `02_CODESYS/Codesys.zip`
- Proyecto interno: `Codesys/Grado.project`
- SHA-256 del ZIP: `5d0eeeca385fd6437f93a5bc6c887b8fa57304a7dda9498cdc42dfb0102cd60c`
- Controlador identificado: CODESYS Control Win V3
- Servidor de comunicación: Modbus TCP, puerto 502
- Datos: histórico `HistorialCultivo.csv` con diez columnas y separación `;`
- Configuración de símbolos: `Grado.Device.Application.xml` con variables `FO_*` para la planta virtual.

## Criterios de consistencia para el modelo Random Forest

Conservar versiones de `Sensores.py`, `Grado.project`, datos de origen y scripts de entrenamiento. En los registros originales el tiempo se identifica como día, hora y minuto simulados; para separar trayectorias independientes debe preservarse el origen y el identificador de cada sesión.

La compatibilidad del modelo entrenado con Python requiere un paquete `joblib` con el esquema de variables y la versión de dinámica hídrica `balance_hidrico_temperatura_v2`.
