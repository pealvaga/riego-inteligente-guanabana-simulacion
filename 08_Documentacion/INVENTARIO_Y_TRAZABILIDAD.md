# Inventario técnico y trazabilidad de artefactos

Esta guía define la información necesaria para vincular cada parte del proyecto con su respectiva evidencia de ejecución y evaluación.

| Componente | Artefactos de referencia | Datos técnicos a documentar |
|---|---|---|
| Simulación Python | `01_Python/Sensores.py` | Dependencias, parámetros, versión y ejecución |
| SCADA y automatización | [`02_CODESYS/Codesys.zip`](../02_CODESYS/Codesys.zip) | Archivo cargado; contrastar su contenido, bibliotecas, HMI y registro histórico al abrirlo en CODESYS |
| Planta virtual | `03_Factory_IO/` | Escena, variables y configuración OPC UA |
| Predicción de humedad | `04_Random_Forest/` | Dataset, particiones, configuración, modelo y métricas |
| Clasificación foliar | `05_MobileNetV2/` | Fuentes, etiquetado, particiones, modelo y métricas |
| Bases y particiones | `06_Datos/` | Procedencia, esquema, licencias, sesiones y particiones |
| Evidencia y métricas | `07_Resultados/` | Fecha, versión, script e insumos de cada resultado |

## Convenciones de identificación

Para cada modelo registrar:
- Archivo y formato del modelo.
- Versión de los datos, generador y scripts.
- Variables de entrada, etiquetas y preprocesamiento.
- Particiones de entrenamiento, validación y prueba.
- Parámetros, semilla aleatoria y librerías utilizadas.
- Métricas sobre prueba independiente y rutas de los archivos utilizados para producirlas.

Para la aplicación Python, el paquete de Random Forest debe incluir la versión `balance_hidrico_temperatura_v2` y ser compatible con las doce variables esperadas por `Sensores.py`.

La reproducibilidad requiere que los artefactos y sus referencias permitan contrastar resultados y configuración sin depender exclusivamente de fragmentos de código incluidos en el documento.
