# Instalación y ejecución — revisión inicial

> **Alcance:** guía provisional basada en `01_Python/Sensores.py`. Sin verificación en un entorno limpio. Los archivos de CODESYS, Factory I/O y modelos entrenados aún están pendientes.

## Requisitos del entorno

| Componente | Estado |
|---|---|
| Windows | Plataforma de referencia; versión exacta pendiente |
| Python | Código requiere sintaxis de Python 3.9+; versión efectiva pendiente |
| Paquetes Python | [Lista provisional](../01_Python/requirements.txt), sin versiones fijadas |
| Tkinter | Interfaz gráfica incluida en instalaciones compatibles de Python |
| CODESYS, Control Win, bibliotecas | Pendiente de incorporar/verificar |
| Factory I/O y OPC UA | Pendiente de incorporar/verificar |

## Preparación de Python en Windows

Abrir terminal en `01_Python`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Sensores.py
```

La creación del entorno virtual y el comando de inicio son propuestas de ejecución, no un procedimiento probado con el sistema del autor. Validar especialmente compatibilidad de Python, TensorFlow y `pymodbus`. Si no está disponible `tkinter`, instalar una distribución de Python que lo incluya.

## Archivos de modelos buscados por la aplicación

En la misma carpeta que `Sensores.py`:
- `modelo_prediccion_humedad.pkl`
- `mejor_modelo_hojas_finetuning.keras`

Sin dichos archivos, los componentes de IA respectivos no funcionarán. El modelo Random Forest debe ser compatible con el esquema de variables y la versión de dinámica del suelo indicada en [documentación Python](../01_Python/README.md).

## Comunicación prevista

Configuración predeterminada en el código Python: IP `127.0.0.1`, puerto `502`, Device ID `1`. Es modificable en la interfaz. Se escribe HR0–HR7 y se lee IR0. Ver [mapa actualizado](MAPA_MODBUS.md).

## Orden previsto de ejecución integral

1. Abrir el proyecto de CODESYS, compilarlo y habilitar su controlador virtual y Modbus TCP.
2. Cargar la escena Factory I/O y confirmar OPC UA con CODESYS.
3. Ejecutar `Sensores.py` con los modelos correspondientes.
4. Conectar Modbus y comprobar las lecturas/escrituras.
5. Iniciar la simulación, verificar histéresis y tiempos simulados.
6. Verificar el registro CSV en CODESYS y la evaluación de cada IA.

Este orden es preliminar: faltan el proyecto, los archivos y las pruebas de extremo a extremo.

## Estado de registro para reentrenamiento

`Sensores.py` **no escribe un CSV de datos de simulación**. En el documento de grado se menciona que el registro histórico `HistorialCultivo.csv` se realiza en CODESYS; hay que contrastarlo con su programa antes de utilizar el CSV para entrenamiento. Reincorporar la generación de datos desde Python será una tarea separada, incluyendo identificación de trayectorias y condiciones de simulación.

## Evidencia pendiente

Versiones exactas, capturas de ejecución, archivos fuente completos, particiones independientes, scripts de entrenamiento, métricas y resultados replicados.
