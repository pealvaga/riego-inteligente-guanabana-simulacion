# Instalación y ejecución del sistema de simulación

Esta guía describe la arquitectura del sistema y el procedimiento de configuración de la aplicación Python. Para una secuencia reproducible desde la descarga del repositorio y con pasos concretos de verificación, consultar **[la guía integral](GUIA_REPRODUCCION_INTEGRAL.md)** y **[la lista de verificación del primer punto](CHECKLIST_PRIMER_PUNTO.md)**. El funcionamiento integral depende de los proyectos CODESYS, Factory I/O y los modelos de IA utilizados en la simulación.

## Software necesario

| Software o componente | Finalidad |
|---|---|
| Windows | Ejecución del entorno de simulación |
| Python 3.9 o superior con Tkinter | Aplicación de simulación e interfaz |
| Bibliotecas de Python | Dependencias de [requirements.txt](../01_Python/requirements.txt) |
| CODESYS y CODESYS Control Win | Controlador virtual y HMI |
| Factory I/O | Escena `Grado.factoryio` (versión guardada 2.5.10), con vínculo OPC DA |
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

El archivo [`02_CODESYS/Simulación guanabana codesys (2).zip`](../02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip) es la versión final publicada por el equipo. **El contenido interno del nuevo ZIP aún no se ha extraído para verificar los archivos**; el paquete anterior sí contenía `Grado.project` y `Grado.Device.Application.xml`, además de auxiliares. En el proyecto se identifican CODESYS Control Win V3, Modbus TCP Slave (puerto 502), programas `OPERACIONES`, `RIEGO` y `REGISTRO_DATOS`, y una tarea cíclica `T#20ms`. Los metadatos mencionan componentes 3.5.9.0/3.5.9.10 y las capturas del equipo identifican el **IDE CODESYS V3.5 SP9 Patch 1**, con **Device Modbus TCP Slave 3.5.9.10**; consultar el [registro del entorno](ENTORNO_CODESYS_REGISTRADO.md). La versión del runtime Control Win y las bibliotecas realmente requeridas por el proyecto deben verificarse en línea. Consultar [documentación CODESYS](../02_CODESYS/README.md).

## Comunicación e integración

1. Descargar y extraer [`02_CODESYS/Simulación guanabana codesys (2).zip`](../02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip); comprobar que contenga `Grado.project` y abrirlo en CODESYS y seleccionar el controlador virtual.
2. Verificar las variables Modbus TCP para Python y los símbolos `FO_*` publicados por el controlador para Factory I/O.
3. Abrir [`03_Factory_IO/Grado.factoryio`](../03_Factory_IO/Grado.factoryio) en Factory I/O. Revisar su configuración `OPCClientDA` hacia `CoDeSys.OPC.DA` y los 14 vínculos `PLC1.Application.GVL.FO_*`; comprobar la disponibilidad del servidor OPC clásico antes de ejecutar la planta.
4. Ejecutar `Sensores.py`.
5. Configurar la conexión Modbus TCP en Python. Valores iniciales de la interfaz: IP `127.0.0.1`, puerto `502` e identificador `1`.
6. Conectar Modbus y comprobar el intercambio de las variables. El programa Python escribe HR0–HR7 y lee IR0.
7. Iniciar la simulación y observar la humedad, los estados de riego y los indicadores SCADA.
8. Consultar los registros de operación y ejecutar los scripts de evaluación de modelos con los conjuntos correspondientes.

Consulte el [mapa Modbus](MAPA_MODBUS.md) para el canal Python–CODESYS y la [documentación de Factory I/O](../03_Factory_IO/README.md) para el canal OPC DA entre la planta virtual y CODESYS. Son dos conexiones diferentes.

## Acceso a datos de MobileNetV2

La carpeta de imágenes declarada para el entrenamiento puede consultarse mediante [Google Drive — carpeta IA](https://drive.google.com/drive/folders/1dSFK86hFvjr4cZiNZvvqDZDGeydOIcys?usp=sharing), sujeto a permisos de acceso y licencias de las fuentes. El script `05_MobileNetV2/ia_imagen.py` espera dos carpetas dentro de `/content/drive/MyDrive/IA`: `Sanas` y `Nutrientes`. Si las imágenes se descargan en otra ubicación, será necesario adaptar la ruta de entrada en una copia del script de entrenamiento.

El [inventario documentado](../06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md) facilita la identificación de los 2.247 archivos. Para reproducir métricas se deben verificar las clases originales, las particiones y la evaluación del checkpoint final con umbral operativo de 0,90.

## Comprobaciones de funcionamiento

Las pruebas de reproducción deben verificar que el balance hídrico evoluciona con temperatura, precipitación y riego; que los umbrales del controlador corresponden a 60 % y 75 % de agua disponible; que el tiempo simulado es coherente; y que las salidas de ambos modelos corresponden a los formatos previstos.

## Registro y análisis de datos

El proyecto documenta el archivo de historial `HistorialCultivo.csv` generado por CODESYS. El proyecto contiene una rutina con bloques CAA File que construye un CSV separado por punto y coma y considera `MB_MINUTO MOD 10 = 0` para el muestreo. Es necesario localizar y comprobar el archivo generado en el sistema de ejecución de CODESYS, ya que el ZIP entregado incluye el proyecto pero no una base CSV de entrenamiento. Para reentrenamiento, el conjunto de registros usado y los scripts de preparación deben permitir distinguir sesiones e identificar la versión de la dinámica ambiental. Los resultados de modelos se documentan en [04_Random_Forest](../04_Random_Forest/) y [05_MobileNetV2](../05_MobileNetV2/).

## Recomendación de seguridad

No publicar direcciones, contraseñas, tokens, claves ni configuraciones privadas de redes. No cargar modelos `.pkl` de procedencia desconocida.
