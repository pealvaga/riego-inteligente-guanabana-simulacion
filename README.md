# Simulación de un sistema de riego inteligente para cultivos de guanábana

Proyecto de grado de Ingeniería Mecatrónica (Universitaria Agustiniana, 2026) orientado a la simulación de un sistema de riego para guanábana (*Annona muricata* L.) a cielo abierto. Integra un modelo ambiental, control automático, supervisión SCADA y dos componentes de inteligencia artificial.

## Arquitectura del sistema

| Componente | Función |
|---|---|
| **Python** | Simulación ambiental y balance hídrico, interfaz gráfica y comunicación Modbus TCP |
| **CODESYS** | Controlador virtual, control por histéresis, HMI SCADA y registro histórico |
| **Factory I/O** | Escena virtual de tanques, actuadores y señales del proceso; archivo con enlace OPC DA a CODESYS |
| **Random Forest** | Pronóstico de humedad del suelo y estimación del próximo riego |
| **MobileNetV2** | Clasificación visual foliar como apoyo a la elección entre riego normal y fertirriego |

Las condiciones de operación utilizadas en la simulación incluyen umbrales de 60 % (inicio) y 75 % (fin) de agua disponible, así como una escala de tiempo acelerada de **1 minuto real por 1 hora simulada**. Los intervalos de predicción del modelo de humedad son de 10 minutos simulados.

La arquitectura no equivale a una validación agronómica en campo. En particular, las clasificaciones visuales no sustituyen un análisis nutricional del cultivo.

## Contenido

| Ruta | Descripción |
|---|---|
| [01_Python](01_Python/) | Aplicación de simulación, interfaz y comunicación |
| [02_CODESYS](02_CODESYS/) | [Paquete CODESYS](02_CODESYS/Codesys.zip), controlador, automatización y SCADA |
| [03_Factory_IO](03_Factory_IO/) | [Escena Grado.factoryio](03_Factory_IO/Grado.factoryio) y sus 14 señales OPC DA |
| [04_Random_Forest](04_Random_Forest/) | [Simulador de registro](04_Random_Forest/simulador_guanabana_grado_registro_RF.py), [notebook de entrenamiento](04_Random_Forest/RF_Guanaba%20(1).ipynb), [modelo publicado](04_Random_Forest/modelo_prediccion_humedad.pkl) y [revisión técnica](04_Random_Forest/REVISION_ENTRENAMIENTO_ACTUAL.md) |
| [05_MobileNetV2](05_MobileNetV2/) | [Script de entrenamiento](05_MobileNetV2/ia_imagen.py), [modelo fine-tuned](05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) y [guía de evaluación](05_MobileNetV2/GUIA_EVALUACION_FINAL.md) |
| [06_Datos](06_Datos/) | Datos, procedencia y particiones |
| [07_Resultados](07_Resultados/) | Resultados, métricas y evidencias |
| [08_Documentacion](08_Documentacion/) | Configuración, reproducibilidad y mapa Modbus |

## Instalación y ejecución

- **[Guía integral de reproducción del sistema](08_Documentacion/GUIA_REPRODUCCION_INTEGRAL.md)**
- **[Lista de verificación de la primera corrección](08_Documentacion/CHECKLIST_PRIMER_PUNTO.md)**
- [Entorno Python registrado: CPython 3.12.9 y versiones de paquetes](08_Documentacion/ENTORNO_PYTHON_REGISTRADO.md)
- [Entorno CODESYS registrado: V3.5 SP9 Patch 1 y componentes](08_Documentacion/ENTORNO_CODESYS_REGISTRADO.md)
- [Texto propuesto para el Anexo C](08_Documentacion/TEXTO_PROPUESTO_ANEXO_C.md)
- [Plantilla de evidencia de pruebas funcionales](07_Resultados/PLANTILLA_EVIDENCIAS_FUNCIONALES.md)
- [Guía del entorno y secuencia de ejecución](08_Documentacion/INSTALACION_Y_EJECUCION.md)
- [Configuración de la aplicación Python](01_Python/README.md)
- [Mapa de registros Modbus TCP](08_Documentacion/MAPA_MODBUS.md)
- [Guía de verificación de resultados](08_Documentacion/ESTADO_REPRODUCIBILIDAD.md)

La ejecución integral requiere los proyectos y modelos correspondientes, además de las herramientas CODESYS y Factory I/O. La escena contiene configuración de **OPC DA** (`CoDeSys.OPC.DA`) para la conexión Factory I/O–CODESYS; Python se comunica con CODESYS mediante **Modbus TCP**. Los nombres y rutas de los modelos utilizados por Python están especificados en su documentación.

## Reentrenamiento desde el registro completo

Para corregir la selección de solo 813 muestras del Excel de Random Forest se creó un [cuaderno alternativo que reconstruye datos desde las tres sesiones](04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb). Consulta las [instrucciones para Google Colab](04_Random_Forest/COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md). El cuaderno nuevo está publicado **sin ejecutar**; se deben generar y documentar sus resultados antes de sustituir cualquier modelo.

## Reproducibilidad y alcance de las IA

La evaluación de Random Forest debe preservar el orden temporal y separar las trayectorias destinadas a entrenamiento, validación y prueba. Sus resultados deben compararse con una referencia de persistencia y acompañarse de un error del momento estimado del próximo riego. **La ejecución actual del cuaderno utiliza el Excel publicado (813 muestras) y no supera la persistencia (RMSE 0,6144 frente a 0,1386)**; el archivo `.pkl` publicado requiere cotejar su procedencia y evaluación antes de utilizarlo en la aplicación.

Para MobileNetV2, el script aportado usa 70/15/15 y crea sus métricas iniciales con umbral 0,50 antes de la fase fine-tuning. La evaluación del checkpoint final se documenta por separado y debe comprobar la independencia por imagen original y la matriz de confusión con el umbral operativo de **probabilidad de deficiencia ≥ 0,90**.

El [inventario de imágenes](05_MobileNetV2/COMO_GENERAR_INVENTARIO.md) puede generarse desde Google Colab sin subir las fotografías al repositorio. Los datasets de referencia son [CoLeaf](https://doi.org/10.17632/brfgw46wzb.1) y [SoursopBD](https://doi.org/10.17632/hjrhrt5hs8.2). Las etiquetas originales requieren justificación explícita: síntomas fitosanitarios en guanábana o deficiencias en café no son automáticamente equivalentes a una deficiencia nutricional de guanábana.

El [inventario de imágenes verificado](06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md) contiene 2.247 archivos y detecta 74 pares de duplicados exactos. La trazabilidad de especies, fuentes y particiones todavía debe establecerse para determinar la independencia de las pruebas.

Las cifras de desempeño deben leerse junto con el conjunto de prueba, el script de evaluación y la configuración que las generó.

## Acceso a las imágenes de entrenamiento

La base de imágenes de MobileNetV2 se mantiene fuera del repositorio por su tamaño. El autor ha facilitado el [enlace a la carpeta IA en Google Drive](https://drive.google.com/drive/folders/1dSFK86hFvjr4cZiNZvvqDZDGeydOIcys?usp=sharing). Consultar el [README de MobileNetV2](05_MobileNetV2/README.md) para la estructura, el inventario y las condiciones de trazabilidad. El acceso público y los derechos de redistribución deben comprobarse antes de utilizar o compartir fotografías de terceros.

## Demostración

[Video de funcionamiento del sistema](https://youtu.be/djTeff68Glk)

## Autoría y uso

Trabajo académico de elaboración propia. El código, los modelos, las escenas y los datos externos pueden tener condiciones de uso diferentes; consultar las licencias respectivas antes de redistribuir componentes de terceros. La publicación en GitHub no otorga por sí sola una licencia de reutilización.
