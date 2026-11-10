# Simulación de un sistema de riego inteligente para cultivos de guanábana

Proyecto de grado de Ingeniería Mecatrónica (Universitaria Agustiniana, 2026) orientado a la simulación de un sistema de riego para guanábana (*Annona muricata* L.) a cielo abierto. Integra un modelo ambiental, control automático, supervisión SCADA y dos componentes de inteligencia artificial.

## Arquitectura del sistema

| Componente | Función |
|---|---|
| **Python** | Simulación ambiental y balance hídrico, interfaz gráfica y comunicación Modbus TCP |
| **CODESYS** | Controlador virtual, control por histéresis, HMI SCADA y registro histórico |
| **Factory I/O** | Representación virtual de tanques, actuadores y señales del proceso |
| **Random Forest** | Pronóstico de humedad del suelo y estimación del próximo riego |
| **MobileNetV2** | Clasificación visual foliar como apoyo a la elección entre riego normal y fertirriego |

Las condiciones de operación utilizadas en la simulación incluyen umbrales de 60 % (inicio) y 75 % (fin) de agua disponible, así como una escala de tiempo acelerada de **1 minuto real por 1 hora simulada**. Los intervalos de predicción del modelo de humedad son de 10 minutos simulados.

La arquitectura no equivale a una validación agronómica en campo. En particular, las clasificaciones visuales no sustituyen un análisis nutricional del cultivo.

## Contenido

| Ruta | Descripción |
|---|---|
| [01_Python](01_Python/) | Aplicación de simulación, interfaz y comunicación |
| [02_CODESYS](02_CODESYS/) | [Paquete CODESYS](02_CODESYS/Codesys.zip), controlador, automatización y SCADA |
| [03_Factory_IO](03_Factory_IO/) | Escena virtual y conexiones |
| [04_Random_Forest](04_Random_Forest/) | Entrenamiento, predicción y evaluación de humedad |
| [05_MobileNetV2](05_MobileNetV2/) | Clasificación de imágenes y evaluación |
| [06_Datos](06_Datos/) | Datos, procedencia y particiones |
| [07_Resultados](07_Resultados/) | Resultados, métricas y evidencias |
| [08_Documentacion](08_Documentacion/) | Configuración, reproducibilidad y mapa Modbus |

## Instalación y ejecución

- [Guía del entorno y secuencia de ejecución](08_Documentacion/INSTALACION_Y_EJECUCION.md)
- [Configuración de la aplicación Python](01_Python/README.md)
- [Mapa de registros Modbus TCP](08_Documentacion/MAPA_MODBUS.md)
- [Guía de verificación de resultados](08_Documentacion/ESTADO_REPRODUCIBILIDAD.md)

La ejecución integral requiere los proyectos y modelos correspondientes, además de las herramientas CODESYS y Factory I/O. Los nombres y rutas de los modelos utilizados por Python están especificados en su documentación.

## Reproducibilidad y alcance de las IA

La evaluación de Random Forest debe preservar el orden temporal y separar las trayectorias destinadas a entrenamiento, validación y prueba. Sus resultados deben compararse con una referencia de persistencia y acompañarse de un error del momento estimado del próximo riego.

Para MobileNetV2, las particiones deben separar las imágenes originales de sus transformaciones aumentadas. La decisión operativa sobre fertirriego usa un umbral de **probabilidad de deficiencia ≥ 0,90**, que también debe aplicarse al evaluar la matriz de confusión correspondiente a esa decisión.

Los datasets de referencia son [CoLeaf](https://doi.org/10.17632/brfgw46wzb.1) y [SoursopBD](https://doi.org/10.17632/hjrhrt5hs8.2). Las etiquetas originales requieren justificación explícita: síntomas fitosanitarios en guanábana o deficiencias en café no son automáticamente equivalentes a una deficiencia nutricional de guanábana.

Las cifras de desempeño deben leerse junto con el conjunto de prueba, el script de evaluación y la configuración que las generó.

## Demostración

[Video de funcionamiento del sistema](https://youtu.be/djTeff68Glk)

## Autoría y uso

Trabajo académico de elaboración propia. El código, los modelos, las escenas y los datos externos pueden tener condiciones de uso diferentes; consultar las licencias respectivas antes de redistribuir componentes de terceros. La publicación en GitHub no otorga por sí sola una licencia de reutilización.
