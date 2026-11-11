# Simulador ambiental: Python

La aplicación [Sensores.py](Sensores.py) integra una interfaz Tkinter, la evolución de la humedad del suelo, la comunicación Modbus TCP y la inferencia de dos modelos de IA.

## Dependencias

Python 3.9 o posterior con Tkinter, más los paquetes descritos en [requirements.txt](requirements.txt). La instalación deberá utilizar versiones compatibles con los artefactos serializados de los modelos.

Desde una terminal de Windows, ubicada en `01_Python`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Sensores.py
```

Las dependencias aún no están fijadas a versiones concretas en el archivo. Se recibió una [captura del entorno instalado](../08_Documentacion/ENTORNO_PYTHON_REGISTRADO.md) que informa CPython 3.12.9 y versiones de los paquetes; esta captura **no constituye una prueba de ejecución**. Para registrar o actualizar las versiones, utilizar **[`08_Documentacion/registrar_entorno.py`](../08_Documentacion/registrar_entorno.py)** desde el mismo intérprete que utiliza la aplicación, siguiendo [la guía integral](../08_Documentacion/GUIA_REPRODUCCION_INTEGRAL.md).

## Archivos de modelo

`Sensores.py` busca los modelos en su mismo directorio:

| Nombre esperado | Función |
|---|---|
| `modelo_prediccion_humedad.pkl` | Predicción de humedad mediante Random Forest |
| `mejor_modelo_hojas_finetuning.keras` | Clasificación foliar mediante MobileNetV2 |

**Formato del paquete Random Forest:** el archivo `.pkl` se carga mediante `joblib` y debe contener un diccionario con `modelo`, `variables`, `simulador_modelo_version` y `paso_minutos`. La versión del modelo ambiental solicitada por el código es `balance_hidrico_temperatura_v2` y el paso es de **10 minutos simulados**.

El orden exacto de las 12 variables que espera la aplicación es:

```text
Temperatura, Precipitacion, HumedadSuelo, RiegoActivo,
HumedadSuelo_lag1, HumedadSuelo_lag2,
Temperatura_lag1, Temperatura_lag2,
Precipitacion_lag1, Precipitacion_lag2,
RiegoActivo_lag1, RiegoActivo_lag2
```

Para inferencia de imágenes, el código convierte a RGB y redimensiona a **224 × 224**. El modelo debe ser consistente con la convención de salida del programa: un único valor que representa la probabilidad de la clase «deficiencia», con el preprocesamiento integrado en la red.

No cargar archivos `.pkl` de procedencia desconocida: los formatos de serialización basados en Python pueden ejecutar código al deserializar.

## Variables de simulación

- Balance hídrico con almacenamiento útil máximo de 90 mm, profundidad radicular de 0,60 m y área efectiva de 20 m².
- Caudal de referencia de riego de 32 L/h y eficiencia de aplicación del 85 %.
- Un minuto real equivale a una hora simulada.
- El modelo predictivo toma muestras cada 10 minutos simulados y emplea dos rezagos.
- El umbral de activación es 60 % de agua disponible; la finalización al 75 % depende de CODESYS.
- En la interfaz, Modbus inicia con IP `127.0.0.1`, puerto `502` y Device ID `1`.
- Se escriben ocho Holding Registers, HR0–HR7; IR0 devuelve el estado de riego.

## Registro de datos y reentrenamiento

El programa realiza muestras temporales en memoria para la predicción. El histórico del proyecto se describe en CODESYS como `HistorialCultivo.csv`. La metodología de generación de nuevos conjuntos, separación por sesiones y reentrenamiento debe documentarse junto a los scripts y archivos de la carpeta [04_Random_Forest](../04_Random_Forest/).

No confundir el almacenamiento en memoria de tres muestras para inferencia con la persistencia de un conjunto de entrenamiento.

## Pruebas de funcionamiento

La verificación incluye: apertura de la interfaz, conexión Modbus, variación del balance hídrico, lectura del estado de riego, coherencia del tiempo simulado, carga de ambos modelos y validación de sus salidas. Ver [procedimiento general](../08_Documentacion/INSTALACION_Y_EJECUCION.md).
