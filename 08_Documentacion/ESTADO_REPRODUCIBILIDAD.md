# Estado de reproducibilidad — evaluación preliminar

Actualizado con la inspección del archivo `01_Python/Sensores.py`.

| Elemento | Presencia | Estado de revisión |
|---|---|---|
| Código principal Python | Sí, `Sensores.py` | Revisado estáticamente; ejecución pendiente |
| Dependencias declaradas | Sí, `01_Python/requirements.txt` | Nombres identificados; falta fijar versiones |
| Modelo de Random Forest `.pkl` | Pendiente | Carga requiere esquema y versión definidos en Python |
| Modelo MobileNetV2 `.keras` | Pendiente | Requiere verificar etiquetas, preprocesamiento y umbral |
| Generación de base CSV desde Python | No implementada en el archivo revisado | Restauración pendiente |
| CODESYS y registro `HistorialCultivo.csv` | Pendiente | Verificar programa y configuraciones |
| Escena Factory I/O | Pendiente | Verificar comunicación OPC UA |
| Datos y particiones | Pendiente | Documentar orígenes, licencias y conjuntos independientes |
| Scripts de entrenamiento y evaluación IA | Pendiente | Necesarios para auditar métricas |
| Ejecución integral de la simulación | No verificada | Requiere entorno y proyectos completos |

**Alcance de la inspección:** lectura estática del código; sin ejecución de CODESYS, Factory I/O ni modelos de IA.

## Hallazgos que impactan el informe

1. La tabla de registros Modbus del informe debe ampliarse a HR5–HR7.
2. La aplicación Python actual solo guarda tres muestras en memoria y no genera dataset CSV.
3. La captura de muestras para el predictor queda condicionada a que Random Forest se haya cargado correctamente.
4. Se debe verificar el umbral operativo de 0,90 con el que se evalúa la matriz de confusión de MobileNetV2.
5. Para la evaluación del regresor se necesitan conjuntos independientes por trayectoria y criterio temporal, además de una referencia sencilla de persistencia.
6. Se requiere trazabilidad entre archivos, datos y resultados.
