# Texto propuesto para el Anexo C: Repositorio y reproducibilidad

> **Versión de trabajo.** Actualizar este apartado tras comprobar la ejecución, documentar las versiones y sustituir el modelo Random Forest por uno validado, si procede. No declarar pruebas ni resultados que no se hayan realizado.

## Anexo C. Repositorio digital del sistema de riego inteligente

Los archivos fuente de la simulación del sistema de riego inteligente para cultivos de guanábana se encuentran disponibles en el repositorio:

**https://github.com/pealvaga/riego-inteligente-guanabana-simulacion**

El repositorio está organizado por componentes: aplicación Python de simulación ambiental e intercambio de datos mediante Modbus TCP; proyecto de controlador virtual y visualización SCADA de CODESYS; escena de Factory I/O para representar tanques, sensores y actuadores; código y artefactos de los modelos de inteligencia artificial Random Forest y MobileNetV2; bases de datos y documentación de respaldo.

La carpeta `08_Documentacion` incluye instrucciones de instalación, mapa de comunicaciones, inventario técnico y una [guía de reproducción integral](GUIA_REPRODUCCION_INTEGRAL.md). La carpeta `06_Datos` contiene un archivo Excel de registros simulados y documentación de procedencia. El conjunto de imágenes empleado por MobileNetV2 se mantiene fuera de GitHub por su volumen; su acceso y sus fuentes se describen en el README del componente, sujeto a los permisos y licencias de las imágenes.

La disponibilidad de código y proyectos permite la revisión del funcionamiento propuesto. La confirmación de compatibilidad, los resultados de evaluación independiente y la reproducción integral deben consultarse en los archivos de estado y evidencia del repositorio, identificando la versión de cada artefacto.

## Información para completar antes de entregar

- Fecha y commit/tag de GitHub que corresponde a la entrega final.
- Versiones instaladas con las que se reprodujo el funcionamiento (Python, librerías, CODESYS, Control Win y Factory I/O).
- Ubicación de capturas de funcionamiento, archivos de registro y resultados de evaluación contrastados.
- Estado validado o no validado del paquete `.pkl` usado en la simulación.
- Enlace a la versión definitiva de la metodología de evaluación de ambas IA.
- Condiciones de acceso a los datasets publicados fuera del repositorio.

No presentar esta sección como demostración de ejecución por sí sola; anexar evidencia real y verificable.
