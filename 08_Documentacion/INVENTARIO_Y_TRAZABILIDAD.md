# Inventario técnico y trazabilidad

Cada artefacto del sistema se relaciona con su función, parámetros de configuración, fuente y evidencia.

| Componente | Artefacto | Trazabilidad técnica |
|---|---|---|
| Simulación ambiental | [Sensores.py](../01_Python/Sensores.py) | Balance hídrico, parámetros, mapa Modbus, interfaz y carga de modelos |
| Controlador y SCADA | [Codesys.zip](../02_CODESYS/Codesys.zip) | `Grado.project`, programas `OPERACIONES`, `RIEGO` y `REGISTRO_DATOS`, controlador virtual y símbolos |
| Planta virtual | [`Grado.factoryio`](../03_Factory_IO/Grado.factoryio) | Formato Factory I/O 2.5.10, dos tanques, controles y 14 variables vía `OPCClientDA` / `CoDeSys.OPC.DA` |
| Predicción de humedad | [04_Random_Forest](../04_Random_Forest/) | Datos, particiones, código de entrenamiento, modelo y evaluación |
| Clasificación foliar | [Script `ia_imagen.py`](../05_MobileNetV2/ia_imagen.py) y [modelo `.keras`](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) | Script Colab con 70/15/15 y umbral de evaluación 0,50 anterior al fine-tuning; evaluación final a 0,90 y manifiesto por origen descritos en [guía](../05_MobileNetV2/GUIA_EVALUACION_FINAL.md) |
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

## Identificación de la escena Factory I/O

- Archivo: `03_Factory_IO/Grado.factoryio`.
- Versión registrada en el archivo: **2.5.10**.
- Dos tanques con sensores de nivel/caudal y válvulas de llenado/descarga.
- Comunicación almacenada: **OPC DA (`CoDeSys.OPC.DA`)**, 14 símbolos bajo `PLC1.Application.GVL.`.
- Verificar la configuración activa y la conexión mediante una prueba en ejecución.
