# Entorno Python registrado — simulación de guanábana

**Origen:** archivo `ENTORNO_EJECUTADO.json`, generado mediante `registrar_entorno.py`.

**Fecha de captura (UTC):** 2026-11-11 04:02:04 +00:00  
**Python:** CPython **3.12.9**  
**Sistema:** Windows / AMD64

## Paquetes instalados según captura

| Paquete | Versión informada |
|---|---|
| numpy | 2.5.3 |
| pandas | 3.0.5 |
| Pillow | 12.3.0 |
| pymodbus | 3.15.0 |
| joblib | 1.6.0 |
| scikit-learn | 1.6.1 |
| tensorflow | 2.21.0 |
| openpyxl | 3.1.5 |
| matplotlib | 3.11.2 |
| keras | 3.15.1 |
| ipykernel | No instalado o no detectado |

La captura se conserva también en [`ENTORNO_EJECUTADO.json`](ENTORNO_EJECUTADO.json) como **declaración de las versiones registradas en un equipo Windows**, no como verificación ejecutada por el revisor.

## Compatibilidad y limitaciones

- El programa [`01_Python/Sensores.py`](../01_Python/Sensores.py) importa `ModbusTcpClient` de `pymodbus.client` y prueba el argumento `device_id`, con alternativa `slave` cuando aparece `TypeError`. La existencia de `pymodbus 3.15.0` **no certifica por sí sola** una conexión con CODESYS.
- El código del modelo de imágenes utiliza `tensorflow.keras.models.load_model(..., compile=False)`. La instalación de TensorFlow/Keras no demuestra que el archivo `.keras` se haya cargado o ejecutado.
- Random Forest se deserializa mediante `joblib.load`. La versión de `scikit-learn` usada para entrenar el `.pkl` debe verificarse y compararse con la captura local (**1.6.1**). No abrir `.pkl` de origen desconocido.
- `ipykernel` es opcional para la aplicación de escritorio; los cuadernos de Colab tienen su propio entorno.
- La captura **no registra** la versión de CODESYS, del controlador virtual, de Factory I/O ni la de las bibliotecas del proyecto. Tampoco comprueba comunicación Modbus, OPC DA, SCADA, sensores o salidas.
- No se han fijado versiones en `01_Python/requirements.txt` para no introducir una combinación de paquetes como si estuviera probada. El archivo de captura permite preparar un bloqueo de dependencias **cuando se confirme ejecución funcional**.

## Verificación que corresponde realizar en el equipo original

1. Confirmar que este Python 3.12.9 es exactamente el que se utiliza al ejecutar `Sensores.py`; si se usa un entorno virtual u otro ejecutable, generar una captura adicional desde ese Python.
2. Abrir la aplicación y documentar el estado de carga de MobileNetV2 y del modelo RF (solo si el artefacto RF está validado).
3. Probar la conexión Modbus con CODESYS y guardar evidencia de HR0–HR7 / IR0.
4. Registrar las versiones instaladas de CODESYS, Control Win, Factory I/O y del driver OPC DA.
5. Si todas las comprobaciones son satisfactorias, conservar un `pip freeze` del mismo intérprete, diferenciando paquetes directos y transitivos.

**Estado:** captura de dependencias obtenida; pruebas de ejecución y compatibilidad pendientes.
