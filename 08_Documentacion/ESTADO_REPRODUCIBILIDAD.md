# Procedimiento de verificación y reproducibilidad

Esta guía sirve como referencia para revisar la coherencia entre el código publicado, los modelos de inteligencia artificial, los datos de origen y los resultados documentados.

## Comprobaciones del entorno

1. Contrastar la versión de cada herramienta con las instrucciones del proyecto.
2. Descargar y extraer el [paquete CODESYS](../02_CODESYS/Codesys.zip), abrir el proyecto y comprobar compilación, bibliotecas y configuración del controlador; luego conectar la escena de Factory I/O.
3. Ejecutar la aplicación Python y verificar Modbus TCP: HR0–HR7, IR0.
4. Comprobar cambios de humedad, actuación por histéresis, reloj simulado y almacenamiento de históricos.
5. Cargar los modelos serializados correspondientes a la versión de la simulación.

## Revisión del modelo Random Forest

- Confirmar identidad del conjunto de entrenamiento y número de trayectorias.
- Respetar orden temporal y evitar reutilización de muestras de una trayectoria entre etapas.
- Documentar variables, rezagos, método de selección y parámetros finales.
- Ejecutar una prueba independiente y comparar contra una referencia de persistencia.
- Calcular RMSE y error de estimación del próximo momento de riego.

## Revisión del clasificador MobileNetV2

- Identificar la especie, fuente y etiqueta original de cada imagen.
- Confirmar la correspondencia y justificación de las clases operativas.
- Verificar que aumentos del mismo original no pasen a conjuntos diferentes.
- Evaluar por clase, fuente y errores de clasificación.
- Aplicar el umbral operativo de 0,90 en la matriz de confusión utilizada para analizar la decisión de fertirriego.

## Correspondencia con el trabajo escrito

Cada indicador final reportado en el documento debe vincularse con su base de datos, partición, programa de evaluación y configuración del modelo. Las cifras históricas no deben combinarse con las de otros entrenamientos como si provinieran de una sola prueba.

**Alcance de resultados:** la simulación verifica el comportamiento de la arquitectura en condiciones modeladas, pero no demuestra por sí sola el ahorro real de agua, el rendimiento agrícola ni un diagnóstico nutricional validado en campo.
