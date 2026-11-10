# Random Forest: predicción de humedad y próximo riego

Este componente del proyecto utiliza un regresor Random Forest para predecir la humedad disponible del suelo y apoyar la estimación del próximo riego dentro del entorno simulado.

## Datos y variables

Las entradas emplean cuatro señales: temperatura, precipitación, humedad del suelo y riego activo, más dos rezagos temporales para cada señal. El paso de predicción es de **10 minutos simulados**.

El conjunto de entrenamiento debe generarse con la misma dinámica hídrica implementada en el simulador de referencia. En la aplicación Python, la versión correspondiente se identifica como `balance_hidrico_temperatura_v2`.

## Partición y metodología de evaluación

1. Identificar cada trayectoria o sesión de simulación y mantener sus muestras agrupadas.
2. Respetar el orden cronológico y separar entrenamiento, validación y prueba, sin usar registros futuros en el entrenamiento.
3. Ajustar hiperparámetros y seleccionar el estimador utilizando únicamente los conjuntos permitidos para desarrollo.
4. Evaluar una sola vez el modelo definitivo sobre datos independientes.
5. Comparar el pronóstico a 10 minutos con una **línea base de persistencia**.
6. Evaluar el error de estimación del siguiente momento de riego, en minutos simulados.

Las métricas se deben presentar junto con cantidades de registros, sesiones, fechas o intervalos simulados, versión del generador, hiperparámetros y semilla aleatoria.

## Integración con Python

El archivo `modelo_prediccion_humedad.pkl` utilizado por [Sensores.py](../01_Python/Sensores.py) debe contener al menos:
- `modelo`: regresor entrenado compatible con `predict`.
- `variables`: nombres y orden de las 12 variables.
- `simulador_modelo_version`: `balance_hidrico_temperatura_v2`.
- `paso_minutos`: `10`.

La inferencia permite anticipar el siguiente riego, pero **no reemplaza la activación basada en la humedad y el control por histéresis implementado en CODESYS**.

## Reproducción de resultados

Para sustentar las métricas académicas, el conjunto de datos, los scripts de preparación, entrenamiento y evaluación y el modelo final deben asociarse mediante identificadores de versión y configuración. Consultar [guía de verificación](../08_Documentacion/ESTADO_REPRODUCIBILIDAD.md).
