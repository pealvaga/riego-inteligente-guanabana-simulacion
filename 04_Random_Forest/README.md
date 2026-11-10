# Random Forest: predicción de humedad y próximo riego

Este componente del proyecto utiliza un regresor Random Forest para predecir la humedad disponible del suelo y apoyar la estimación del próximo riego dentro del entorno simulado.

## Separación del entrenamiento y la aplicación

La versión de simulación instalada en `01_Python/Sensores.py` se conserva **sin modificaciones**. En esta carpeta se desarrollan de forma independiente los procesos de preparación de datos, entrenamiento, validación y evaluación del modelo.

**Flujo de trabajo:** registros CSV originales → preparación y separación de trayectorias → entrenamiento y validación temporal → evaluación independiente → exportación del modelo `.pkl` → copia del modelo final a `01_Python/modelo_prediccion_humedad.pkl`.

La copia a `01_Python` debe realizarse únicamente después de comprobar la compatibilidad del paquete y las métricas. No es necesario modificar la interfaz Python, la lógica de CODESYS ni la escena Factory I/O para cambiar el modelo serializado si conserva su interfaz esperada.

El historial de CODESYS se describe como `HistorialCultivo.csv` y contiene columnas `Dia`, `Hora`, `Minuto`, `Temperatura`, `Precipitacion`, `HumedadSuelo`, `NivelAgua`, `NivelNutrientes`, `RiegoActivo` y `TipoRiego`. Como no incorpora un identificador de sesión, los archivos de distintas ejecuciones se deben etiquetar **antes** de construir rezagos, de modo que no se combinen trayectorias discontinuas.

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
