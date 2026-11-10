# Aplicación Python de simulación ambiental

## Archivo original

- [Sensores.py](Sensores.py): aplicación Tkinter que simula la evolución de la humedad del suelo, se comunica por Modbus TCP con CODESYS y utiliza dos modelos de inteligencia artificial.
- **Estado:** archivo fuente incorporado por el autor. La ejecución integral aún no se ha comprobado en otro equipo.

## Requisitos identificados en el código

Python con soporte para `tuple[float, float]` (Python 3.9 o posterior), Tkinter y estos paquetes de terceros:
- `numpy`
- `pandas`
- `Pillow` (módulo `PIL`)
- `pymodbus`
- `joblib` (carga de Random Forest)
- `scikit-learn` (dependencia del modelo de regresión serializado)
- `tensorflow` (carga y ejecución de MobileNetV2 mediante `tensorflow.keras`)

Consultar [requirements.txt](requirements.txt). **Las versiones son provisionales, no fijadas**; registrar versiones del entorno real antes de anunciar resultados reproducibles.

## Inicio básico (aún sin validación externa)

Desde una terminal en `01_Python`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Sensores.py
```

Tkinter debe encontrarse disponible en la instalación de Python. La compatibilidad entre versiones de TensorFlow y Python necesita validarse en el entorno original.

## Modelos externos requeridos

La aplicación busca **en la misma carpeta que `Sensores.py`**:

| Archivo | Uso | Estado en el repositorio |
|---|---|---|
| `modelo_prediccion_humedad.pkl` | Regresión Random Forest | Pendiente de incorporar/verificar |
| `mejor_modelo_hojas_finetuning.keras` | Clasificación MobileNetV2 | Pendiente de incorporar/verificar |

El archivo `.pkl` debe ser un diccionario `joblib` con:
- `modelo`: estimador entrenado con método `predict`
- `variables`: **lista exacta y ordenada** de 12 variables esperadas por la aplicación
- `simulador_modelo_version`: `balance_hidrico_temperatura_v2`
- `paso_minutos`: 10

Lista de variables: `Temperatura`, `Precipitacion`, `HumedadSuelo`, `RiegoActivo`; para cada variable se incluyen los rezagos `lag1` y `lag2` en el orden especificado dentro del propio código. No cargar modelos `.pkl` de fuentes no confiables: `joblib.load` puede ejecutar contenido malicioso.

Si falta el archivo `.pkl` o es incompatible, la simulación ambiental y Modbus pueden seguir operando, pero las predicciones Random Forest quedan deshabilitadas. Si falta `.keras`, la clasificación foliar no estará disponible.

## Parámetros confirmados por inspección

- Interfaz: tres pestañas, simulación ambiental, IA foliar y comunicación Modbus.
- Escala temporal: 60 segundos reales = 1 hora simulada.
- Muestreo predictivo: cada 10 minutos simulados (memoria `deque(maxlen=3)`).
- Umbral inferior de humedad disponible: 60 %; superior de detención implementado en CODESYS: 75 %.
- Humedad: porcentaje de **agua disponible**, no humedad volumétrica directa.
- Tanque radicular simplificado: 90 mm útiles; caudal 32 L/h, eficiencia 85 %, superficie efectiva 20 m².
- Visión artificial: entrada RGB 224 × 224; el código supone que la salida escalar del modelo es la probabilidad de deficiencia; riego de tipo 2 solo con probabilidad >= 0,90.
- Modbus predeterminado: IP `127.0.0.1`, puerto `502`, ID `1`; estos valores pueden cambiarse desde la interfaz.
- Escritura Python → CODESYS: HR0–HR7; lectura del estado de riego: IR0. Ver [mapa Modbus](../08_Documentacion/MAPA_MODBUS.md).

## Registro de datos: advertencia importante

**El archivo `Sensores.py` subido no contiene llamadas a `to_csv`, `read_csv` ni escritura de archivos de historial.** El método `_capture_ai_sample` únicamente agrega muestras a una cola temporal y, además, retorna sin registrar si no está cargado el predictor Random Forest.

Por tanto **no hay generación de un dataset de entrenamiento por esta aplicación, en su estado actual**. El informe atribuye el registro histórico a CODESYS mediante `HistorialCultivo.csv`. Para regenerar un dataset desde Python debe incorporarse un registrador de sesiones independiente del estado de carga de Random Forest, conservando la dinámica hídrica y marcando los reinicios de las trayectorias.

## Validación pendiente

1. Incorporar y comprobar los archivos de modelos definitivos.
2. Registrar versiones exactas de bibliotecas y sistema operativo.
3. Verificar la correspondencia entre el mapa de registros y el proyecto CODESYS.
4. Confirmar las etiquetas y el preprocesamiento del modelo de imagen con el script de entrenamiento.
5. Verificar el manejo de pausa, reinicio, interrupciones Modbus y escritura de historial.
6. Publicar scripts y particiones reproducibles para evaluar ambos modelos.
