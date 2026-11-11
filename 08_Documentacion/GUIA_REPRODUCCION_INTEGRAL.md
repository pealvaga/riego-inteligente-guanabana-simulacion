# Guía de reproducción integral — simulación de riego de guanábana

## Alcance y estado

Esta guía permite identificar y preparar los artefactos publicados, y describe las comprobaciones necesarias para ejecutar la simulación. **No constituye un certificado de prueba funcional**: el controlador, OPC DA, Modbus TCP, SCADA y modelos deben verificarse en el equipo de reproducción. Los resultados históricos de Random Forest todavía no demuestran un modelo definitivo validado.

Se mantiene intacta la simulación original en `01_Python/Sensores.py`, `02_CODESYS/Codesys.zip` y `03_Factory_IO/Grado.factoryio`.

## 1. Descargar el repositorio

En Windows, con Git instalado:

```powershell
git clone https://github.com/pealvaga/riego-inteligente-guanabana-simulacion.git
cd riego-inteligente-guanabana-simulacion
```

También se puede descargar ZIP desde la página principal del repositorio y extraerlo conservando la estructura de carpetas.

**Identificación de los proyectos:** `01_Python/Sensores.py` es la aplicación principal; `04_Random_Forest/simulador_guanabana_grado_registro_RF.py` es una **variante independiente para registrar y exportar datos**, no el archivo que se debe ejecutar cuando se desea reproducir el sistema original.

## 2. Registrar el entorno exacto

Instalar una versión de Python compatible con las bibliotecas y con los modelos entregados, incluyendo el módulo Tkinter. **No se debe asumir que cualquier versión de Python 3.9+ o de TensorFlow es compatible con el modelo `.keras` publicado.** Usar los números de versión del equipo donde el sistema funciona y registrarlos antes de intentar reproducirlo.

En la raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\01_Python\requirements.txt
.\.venv\Scripts\python.exe .\08_Documentacion\registrar_entorno.py --salida .\08_Documentacion\ENTORNO_EJECUTADO.json
.\.venv\Scripts\python.exe -m pip freeze > .\08_Documentacion\DEPENDENCIAS_EJECUTADAS.txt
```

Los `requirements.txt` actuales describen **nombres de bibliotecas sin versiones fijadas**; para una reproducción equivalente hay que completar la captura anterior desde el equipo original en que los programas y los modelos fueron probados.

El script de captura no importa ni deserializa los modelos, no consulta la red y solo guarda información básica de Python y versiones de paquetes. No recopila credenciales.

## 3. Colocar los modelos esperados por la aplicación principal

La aplicación busca **ambos modelos en la misma carpeta que `Sensores.py`**, con nombres exactos:

| Modelo | Ubicación documental | Ubicación de ejecución |
|---|---|---|
| MobileNetV2 | `05_MobileNetV2/mejor_modelo_hojas_finetuning.keras` | `01_Python/mejor_modelo_hojas_finetuning.keras` |
| Random Forest | `04_Random_Forest/modelo_prediccion_humedad.pkl` | `01_Python/modelo_prediccion_humedad.pkl` |

Para la IA de imagen puede copiarse su archivo publicado:

```powershell
Copy-Item .\05_MobileNetV2\mejor_modelo_hojas_finetuning.keras .\01_Python\mejor_modelo_hojas_finetuning.keras
```

**No copiar todavía el archivo Random Forest `.pkl` publicado a `01_Python`: su procedencia y desempeño aún no están validados.** Para comprobar la interfaz principal sin un modelo RF aprobado, mantener la ubicación de ese archivo vacía y registrar el mensaje de carga de modelo no disponible. El resto de la simulación deberá comprobarse por separado; la función de pronóstico RF no se puede certificar sin un modelo compatible.

Un paquete RF apto debe incluir `modelo` con `predict`, `variables` en el orden de las 12 entradas, `simulador_modelo_version=balance_hidrico_temperatura_v2` y `paso_minutos=10`. Solo deserializar archivos `joblib/pkl` cuya procedencia sea confiable.

## 4. Preparar CODESYS

1. Descargar y descomprimir `02_CODESYS/Codesys.zip`.
2. Abrir el proyecto `Codesys/Grado.project` en una instalación compatible de CODESYS, con CODESYS Control Win V3.
3. Revisar y registrar versión del entorno, dispositivo, bibliotecas y dependencias requeridas. El paquete tiene referencias a componentes 3.5.9.0 / 3.5.9.10, **no una versión completa de instalación certificada**.
4. Compilar y comprobar errores; arrancar el controlador virtual y ejecutar la aplicación.
5. Verificar el dispositivo Modbus TCP Slave/Server con puerto 502, y el mapa de HR0–HR7 e IR0 descrito en [MAPA_MODBUS.md](MAPA_MODBUS.md).
6. Comprobar que las variables de símbolo `PLC1.Application.GVL.FO_*` estén expuestas al servidor OPC clásico.

El uso del puerto 502 y de un servidor OPC DA depende de la instalación, los servicios y permisos disponibles en el PC. Anotar cualquier cambio de IP, puerto o configuración necesaria para la prueba real.

## 5. Abrir Factory I/O

1. Abrir `03_Factory_IO/Grado.factoryio` en una versión compatible de Factory I/O (el archivo declara versión 2.5.10).
2. Revisar **OPC Client DA** con servidor `CoDeSys.OPC.DA`, no confundirlo con OPC UA.
3. Verificar los **14 símbolos** `PLC1.Application.GVL.FO_*` documentados en [03_Factory_IO/README.md](../03_Factory_IO/README.md).
4. Probar niveles, actuadores de los dos tanques, inicio, parada, emergencia y torre luminosa.

El fichero de escena incluye un perfil guardado de OPC DA, pero eso **no garantiza** que el servidor y el driver funcionen sin ajustes en otra instalación.

## 6. Abrir la aplicación Python

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe .\01_Python\Sensores.py
```

En el programa, comprobar la conexión Modbus al controlador; valores iniciales declarados: **127.0.0.1**, puerto **502**, Unit/Device ID **1**. La aplicación escribe HR0–HR7 y lee IR0.

Realizar y guardar evidencia de las siguientes comprobaciones **en la aplicación ejecutada**:

- Modificación de temperatura y precipitación y cambio consecuente de humedad simulada.
- Escala de tiempo: 1 minuto real equivale a 1 hora simulada.
- Riego por histéresis según el control activo de CODESYS. El código inspeccionado utiliza comparaciones estrictas `< 60` y `> 75`; no asumir que las condiciones de frontera inclusivas estén implementadas.
- Lectura de IR0 y estado real de riego; verificar concordancia con salidas.
- Activación de bombas/válvulas, niveles e indicadores en Factory I/O.
- Clasificación de una imagen mediante MobileNetV2, respetando el umbral operativo de 0,90 para fertirriego.
- Carga y pronóstico con Random Forest **solo una vez exista un paquete validado y compatible**.

Para registrar el histórico de CODESYS, comprobar la ubicación real de `HistorialCultivo.csv` y su contenido. El programa alternativo de Random Forest guarda por separado un Excel de sesiones; no confundir ambos orígenes de datos.

## 7. Reproducir los datos y los entrenamientos

### Random Forest

- El archivo original publicado se encuentra en [`06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx`](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx).
- Contiene 2.878 filas en `Registro_10min`, pero solo 813 en la hoja original `Entrenamiento_RF`.
- Para reconstruir las muestras de todas las sesiones usar [`04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb), siguiendo [sus instrucciones](../04_Random_Forest/COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md).
- Separar escenarios completos para prueba independiente y comparar RMSE/MAE con persistencia. Los resultados del cuaderno corregido **aún requieren ejecución** y documentación.
- No usar el modelo no validado como evidencia de que mejoró el pronóstico.

### MobileNetV2

- Código de entrenamiento: [`05_MobileNetV2/ia_imagen.py`](../05_MobileNetV2/ia_imagen.py).
- Modelo de imágenes: [`05_MobileNetV2/mejor_modelo_hojas_finetuning.keras`](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras).
- Carpeta de imágenes proporcionada por el autor: [Google Drive — IA](https://drive.google.com/drive/folders/1dSFK86hFvjr4cZiNZvvqDZDGeydOIcys?usp=sharing), sujeta a permisos y licencias. El código de Colab utiliza `/content/drive/MyDrive/IA`, con carpetas `Sanas` y `Nutrientes`.
- Reproducir la evaluación del checkpoint final siguiendo [la guía](../05_MobileNetV2/GUIA_EVALUACION_FINAL.md); comprobar independencia de imágenes originales y usar **0,90** como umbral operativo.
- Las etiquetas construidas con CoLeaf (café) y SoursopBD (guanábana con enfermedades/plagas) no prueban diagnóstico nutricional específico en guanábana.

## 8. Guardar evidencias de una ejecución comprobada

Publicar en `07_Resultados/` exclusivamente resultados con procedencia clara: fecha de prueba, versiones instaladas, captura de interfaz/SCADA, parámetros usados, CSV de registros, resultados de evaluación y cualquier error o incidencia con su solución.

Consultar [la lista de verificación del primer requerimiento](CHECKLIST_PRIMER_PUNTO.md) y [el documento de estado](ESTADO_REPRODUCIBILIDAD.md).

**Estado de esta guía:** instrucciones preparadas a partir de archivos publicados; la reproducibilidad integral sigue **pendiente de verificación práctica en el equipo original**.
