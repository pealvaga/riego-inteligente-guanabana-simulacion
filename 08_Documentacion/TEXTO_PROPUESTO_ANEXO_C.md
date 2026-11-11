# Anexo C. Repositorio digital y reproducibilidad del sistema de riego inteligente

Como complemento al desarrollo del proyecto, se organizó un repositorio digital en GitHub que contiene los archivos de programación, modelos de inteligencia artificial, datos de simulación, resultados de evaluación y evidencias de funcionamiento del sistema de riego inteligente para cultivos de guanábana a cielo abierto.

El repositorio se encuentra disponible en el siguiente enlace:

**https://github.com/pealvaga/riego-inteligente-guanabana-simulacion**

Su estructura permite consultar por separado los principales componentes del sistema: la aplicación de simulación ambiental desarrollada en Python, el proyecto de automatización y visualización SCADA en CODESYS, la escena virtual implementada en Factory I/O y los modelos de inteligencia artificial Random Forest y MobileNetV2.

La carpeta `01_Python` contiene el programa de simulación y comunicación Modbus TCP. En `02_CODESYS` se encuentra el [paquete final declarado del controlador virtual](../02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip) y su configuración de supervisión, mientras que `03_Factory_IO` contiene la representación virtual de los tanques, sensores y actuadores. La integración entre CODESYS y Factory I/O se realiza mediante **OPC DA**, mientras que el intercambio de información entre Python y CODESYS utiliza **Modbus TCP**.

En cuanto a la inteligencia artificial, la carpeta `04_Random_Forest` incluye el código de entrenamiento, la base de datos consolidada, las predicciones de prueba y las métricas del modelo encargado de estimar la humedad del suelo a intervalos de diez minutos simulados. La versión actualizada del modelo, identificada como `rf-v2`, se encuentra disponible en:

**https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2**

La evaluación de esta versión comprendió **4.552 registros de entrenamiento y 922 registros de prueba**, obteniendo una raíz del error cuadrático medio (**RMSE**) de **0,1143 puntos porcentuales**, frente a **0,1720** de una referencia basada en persistencia. Adicionalmente, se documentaron **21 comparaciones** realizadas durante el funcionamiento de la aplicación, en las cuales la humedad observada se registró diez minutos simulados después de cada predicción.

La carpeta `05_MobileNetV2` contiene el código y el modelo de clasificación de imágenes foliares para apoyar la selección entre riego normal y fertirriego. También se incluye una evaluación **preliminar** de **100 imágenes seleccionadas como hojas de guanábana**. Los resultados y las limitaciones del conjunto de prueba se describen en `07_Resultados`.

Las evidencias de funcionamiento están disponibles en la carpeta `07_Resultados/evidencias_integracion_guanabana`, que reúne **21 capturas** de la aplicación Python, CODESYS y Factory I/O. Estas permiten observar la comunicación entre componentes, el monitoreo de variables, la ejecución de la simulación, las respuestas de control y la visualización de una estimación del próximo riego.

Finalmente, `08_Documentacion` reúne las instrucciones de instalación y ejecución, el mapa de comunicaciones, los registros de versiones y la información necesaria para reproducir el entorno. Se documentó el uso de **Python 3.12.9** y un [inventario de 53 paquetes](versiones_librerias_python_20261111.txt) con sus respectivas versiones, además de las versiones de CODESYS y Factory I/O utilizadas durante el desarrollo.

La publicación del repositorio facilita la consulta y revisión técnica de la simulación. Los resultados corresponden al entorno virtual desarrollado y no constituyen una validación directa del desempeño del sistema en condiciones reales de cultivo. Las limitaciones de los modelos de inteligencia artificial y las recomendaciones para futuros trabajos se encuentran documentadas en los informes de resultados.

---

**Nota de control documental (no copiar al Anexo):** el equipo confirmó que el ZIP final se guardó y se abrió correctamente. La revisión remota del ZIP binario no se pudo extraer mediante la conexión a GitHub; esa limitación es de verificación independiente y no modifica la declaración sobre el equipo local. La prueba de RF a +10 min y su evaluación de 922 casos no demuestran todavía la exactitud de la **hora** estimada del siguiente riego. Las conclusiones de MobileNet se consideran preliminares, no diagnósticos nutricionales de campo.
