# Instalación y ejecución del sistema de simulación

Esta guía describe la arquitectura del sistema y el procedimiento de configuración de la aplicación Python. El funcionamiento integral depende de los proyectos CODESYS, Factory I/O y los modelos de IA utilizados en la simulación.

## Software necesario

| Software o componente | Finalidad |
|---|---|
| Windows | Ejecución del entorno de simulación |
| Python 3.9 o superior con Tkinter | Aplicación de simulación e interfaz |
| Bibliotecas de Python | Dependencias de [requirements.txt](../01_Python/requirements.txt) |
| CODESYS y CODESYS Control Win | Controlador virtual y HMI |
| Factory I/O | Representación del proceso virtual |
| Modelos `.pkl` y `.keras` | Predicción de humedad y clasificación de imágenes |

Las versiones concretas de Python, TensorFlow, CODESYS, Factory I/O y bibliotecas deben corresponder a las utilizadas para generar y ejecutar los artefactos finales.

## Preparación de Python en Windows

Desde una terminal ubicada en `01_Python`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Sensores.py
```

Si PowerShell no permite activar el entorno, se puede ejecutar `.venv\Scripts\python.exe` directamente para instalar paquetes y ejecutar la aplicación.

Colocar en el directorio de `Sensores.py` los archivos `modelo_prediccion_humedad.pkl` y `mejor_modelo_hojas_finetuning.keras` que correspondan a los modelos entrenados.

## Proyecto CODESYS incluido

El archivo [`02_CODESYS/Codesys.zip`](../02_CODESYS/Codesys.zip) contiene `Grado.project` y `Grado.Device.Application.xml`, además de archivos auxiliares. En el proyecto se identifican CODESYS Control Win V3, Modbus TCP Slave (puerto 502), programas `OPERACIONES`, `RIEGO` y `REGISTRO_DATOS`, y una tarea cíclica `T#20ms`. Los metadatos mencionan componentes 3.5.9.0/3.5.9.10: las versiones de instalación deben cotejarse con el entorno de apertura. Consultar [documentación CODESYS](../02_CODESYS/README.md).

## Comunicación e integración

1. Descargar y extraer [`02_CODESYS/Codesys.zip`](../02_CODESYS/Codesys.zip); abrir el archivo de proyecto en CODESYS y seleccionar el controlador virtual.
2. Verificar las variables Modbus TCP y los símbolos OPC UA utilizados por Factory I/O.
3. Abrir la escena de Factory I/O y conectar el intercambio de señales con CODESYS.
4. Ejecutar `Sensores.py`.
5. Configurar la conexión Modbus TCP en Python. Valores iniciales de la interfaz: IP `127.0.0.1`, puerto `502` e identificador `1`.
6. Conectar Modbus y comprobar el intercambio de las variables. El programa Python escribe HR0–HR7 y lee IR0.
7. Iniciar la simulación y observar la humedad, los estados de riego y los indicadores SCADA.
8. Consultar los registros de operación y ejecutar los scripts de evaluación de modelos con los conjuntos correspondientes.

Consulte el [mapa Modbus](MAPA_MODBUS.md) para la descripción de los registros.

## Comprobaciones de funcionamiento

Las pruebas de reproducción deben verificar que el balance hídrico evoluciona con temperatura, precipitación y riego; que los umbrales del controlador corresponden a 60 % y 75 % de agua disponible; que el tiempo simulado es coherente; y que las salidas de ambos modelos corresponden a los formatos previstos.

## Registro y análisis de datos

El proyecto documenta el archivo de historial `HistorialCultivo.csv` generado por CODESYS. El proyecto contiene una rutina con bloques CAA File que construye un CSV separado por punto y coma y considera `MB_MINUTO MOD 10 = 0` para el muestreo. Es necesario localizar y comprobar el archivo generado en el sistema de ejecución de CODESYS, ya que el ZIP entregado incluye el proyecto pero no una base CSV de entrenamiento. Para reentrenamiento, el conjunto de registros usado y los scripts de preparación deben permitir distinguir sesiones e identificar la versión de la dinámica ambiental. Los resultados de modelos se documentan en [04_Random_Forest](../04_Random_Forest/) y [05_MobileNetV2](../05_MobileNetV2/).

## Recomendación de seguridad

No publicar direcciones, contraseñas, tokens, claves ni configuraciones privadas de redes. No cargar modelos `.pkl` de procedencia desconocida.
