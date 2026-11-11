# Texto propuesto para el Anexo C: Repositorio y reproducibilidad

> **Versión de trabajo.** Actualizar este apartado tras comprobar la ejecución, documentar las versiones y cotejar el modelo Random Forest v2 publicado con el archivo original generado por Colab y comprobar su carga en la aplicación, si procede. No declarar pruebas ni resultados que no se hayan realizado.

## Anexo C. Repositorio digital del sistema de riego inteligente

Los archivos fuente de la simulación del sistema de riego inteligente para cultivos de guanábana se encuentran disponibles en el repositorio:

**https://github.com/pealvaga/riego-inteligente-guanabana-simulacion**

El repositorio está organizado por componentes: aplicación Python de simulación ambiental e intercambio de datos mediante Modbus TCP; proyecto de controlador virtual y visualización SCADA de CODESYS; escena de Factory I/O para representar tanques, sensores y actuadores; código y artefactos de los modelos de inteligencia artificial Random Forest y MobileNetV2; bases de datos y documentación de respaldo.

La carpeta `08_Documentacion` incluye instrucciones de instalación, mapa de comunicaciones, inventario técnico y una [guía de reproducción integral](GUIA_REPRODUCCION_INTEGRAL.md). La carpeta `06_Datos` contiene un archivo Excel de registros simulados y documentación de procedencia. El conjunto de imágenes empleado por MobileNetV2 se mantiene fuera de GitHub por su volumen; su acceso y sus fuentes se describen en el README del componente, sujeto a los permisos y licencias de las imágenes.

La disponibilidad de código y proyectos permite la revisión del funcionamiento propuesto. La confirmación de compatibilidad, los resultados de evaluación independiente y la reproducción integral deben consultarse en los archivos de estado y evidencia del repositorio, identificando la versión de cada artefacto.

### Modelo Random Forest actualizado

El modelo Random Forest se distribuye como archivo adjunto en [GitHub Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2), por exceder el límite de carga de la interfaz web para archivos normales. Se publicaron el Excel consolidado de entrenamiento, las predicciones de prueba y las métricas en la carpeta `04_Random_Forest`. La evaluación reportó 4.552 muestras de entrenamiento, 922 de prueba, RMSE de 0,114327 para Random Forest y 0,172037 para la referencia de persistencia. Es una mejora observada en escenarios simulados; queda pendiente la comprobación de compatibilidad en la aplicación y la evaluación del error del instante de próximo riego. Véase el [informe de resultados v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md).

## Información para completar antes de entregar

- Fecha y commit/tag de GitHub que corresponde a la entrega final.
- Versiones instaladas con las que se reprodujo el funcionamiento (Python, librerías, CODESYS, Control Win y Factory I/O).
- Ubicación de capturas de funcionamiento, archivos de registro y resultados de evaluación contrastados.
- Verificación de identidad SHA-256 entre el paquete `.pkl` original de Colab y el adjunto de Release, y prueba de carga de ese paquete en la aplicación.
- Enlace a la versión definitiva de la metodología de evaluación de ambas IA.
- Condiciones de acceso a los datasets publicados fuera del repositorio.

No presentar esta sección como demostración de ejecución por sí sola; anexar evidencia real y verificable.
