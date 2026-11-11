# Inventario técnico y trazabilidad

Cada artefacto del sistema se relaciona con su función, parámetros de configuración, fuente y evidencia.

| Componente | Artefacto | Trazabilidad técnica |
|---|---|---|
| Simulación ambiental | [Sensores.py](../01_Python/Sensores.py) | Balance hídrico, parámetros, mapa Modbus, interfaz y carga de modelos |
| Controlador y SCADA | [Simulación guanabana codesys (2).zip](../02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip) | ZIP final declarado por el usuario: contiene la copia completa de su carpeta de CODESYS. **Falta inspección de los archivos internos** para confirmar `Grado.project` y los símbolos. |
| Planta virtual | [`Grado.factoryio`](../03_Factory_IO/Grado.factoryio) | Formato Factory I/O 2.5.10, dos tanques, controles y 14 variables vía `OPCClientDA` / `CoDeSys.OPC.DA` |
| Predicción de humedad | [04_Random_Forest](../04_Random_Forest/) | Datos, particiones, código de entrenamiento, modelo y evaluación |
| Clasificación foliar | [Script `ia_imagen.py`](../05_MobileNetV2/ia_imagen.py) y [modelo `.keras`](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) | Script Colab con 70/15/15 y umbral de evaluación 0,50 anterior al fine-tuning; evaluación final a 0,90 y manifiesto por origen descritos en [guía](../05_MobileNetV2/GUIA_EVALUACION_FINAL.md) |
| Datos | [06_Datos](../06_Datos/) | Procedencia, sesiones, licencias, esquema y separación temporal |
| Resultados | [07_Resultados](../07_Resultados/) | Comparaciones, métricas y evidencias por versión |

## Identificación del proyecto de controlador

- Archivo final: `02_CODESYS/Simulación guanabana codesys (2).zip`
- Tamaño: **8.906.941 bytes**
- Identificador de objeto Git (blob SHA-1): `0154d1f7af90e3bec0958a563d9cbaed0d1a59a9`
- Contenido interno del ZIP **pendiente de extracción e inspección**. La ruta `Codesys/Grado.project` y el SHA-256 `5d0eeeca385fd6437f93a5bc6c887b8fa57304a7dda9498cdc42dfb0102cd60c` corresponden a la **versión anterior**, ya retirada.
- IDE de programación registrado por capturas: **CODESYS V3.5 SP9 Patch 1** ([detalles de componentes](ENTORNO_CODESYS_REGISTRADO.md))
- Controlador identificado en el entorno: **CODESYS Control Win V3 3.5.9.10** por captura de versión; las capturas E5–E6 muestran el proyecto ejecutándose y compilado sin errores, aunque la nueva revisión del ZIP no fue abierta directamente.
- Herramienta OPCConfig identificada: **3.5.9.0** por captura; conexión OPC DA mostrada en E1 y otras evidencias, sin verificar directamente la apertura del ZIP nuevo
- Servidor de comunicación: Modbus TCP, puerto 502
- Datos: histórico `HistorialCultivo.csv` con diez columnas y separación `;`
- Configuración de símbolos en paquete inspeccionado previamente: `Grado.Device.Application.xml` con variables `FO_*` para la planta virtual; verificar que esté incluida en el paquete definitivo.

## Criterios de consistencia para el modelo Random Forest

Conservar versiones de `Sensores.py`, `Grado.project`, datos de origen y scripts de entrenamiento. En los registros originales el tiempo se identifica como día, hora y minuto simulados; para separar trayectorias independientes debe preservarse el origen y el identificador de cada sesión.

La compatibilidad del modelo entrenado con Python requiere un paquete `joblib` con el esquema de variables y la versión de dinámica hídrica `balance_hidrico_temperatura_v2`.

## Identificación de la escena Factory I/O

- Archivo: `03_Factory_IO/Grado.factoryio`.
- Versión registrada en el archivo **y confirmada en la aplicación instalada**: **2.5.10** ([capturas documentadas](VERSIONES_SOFTWARE_CONFIRMADAS.md)).
- Dos tanques con sensores de nivel/caudal y válvulas de llenado/descarga.
- Comunicación almacenada: **OPC DA (`CoDeSys.OPC.DA`)**, 14 símbolos bajo `PLC1.Application.GVL.`.
- Verificar la configuración activa y la conexión mediante una prueba en ejecución.
