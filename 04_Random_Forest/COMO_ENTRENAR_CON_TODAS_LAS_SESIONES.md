# Entrenar Random Forest con todas las sesiones de Registro_10min

El [cuaderno corregido](RF_Guanaba_todas_sesiones.ipynb) se creó porque la versión anterior leía únicamente `Entrenamiento_RF` del Excel publicado, donde había **813 ejemplos de una sesión**, aunque `Registro_10min` contenía **2.878 registros brutos de tres sesiones**.

## Uso en Google Colab

1. Abrir [`RF_Guanaba_todas_sesiones.ipynb`](RF_Guanaba_todas_sesiones.ipynb) desde GitHub en Google Colab.
2. Ejecutar las celdas **de arriba abajo**. La tercera celda de código descarga automáticamente el Excel de entrenamiento desde una revisión fija del repositorio; si la descarga falla, pedirá subir manualmente `Datos_entrenamiento_guanabana_20261110_103013.xlsx`.
3. El cuaderno **lee `Registro_10min`, no `Entrenamiento_RF`**, y muestra para cada sesión y escenario el número de registros originales y ejemplos válidos.
4. El proceso genera el archivo `/content/Base_guanabana_consolidada_para_RF.xlsx` con `Registro_10min`, `Entrenamiento_RF`, `ResumenEscenarios` y `Parametros`.
5. A continuación realiza entrenamiento y evaluación. Descargar `resultados_RF_guanabana.zip`, que incluye la base consolidada, el reporte CSV, el JSON de métricas y el `.pkl` exportado. Subir la base consolidada a `06_Datos/` y los reportes CSV/JSON a `07_Resultados/`, después de comprobar que no incluyan información sensible.

## Por qué no se obtienen necesariamente 2.878 ejemplos de entrenamiento

Cada ejemplo requiere **cuatro observaciones consecutivas** del mismo escenario (t−20, t−10, t y t+10 minutos) con lecturas válidas del estado de riego. Se descartan ventanas con intervalos interrumpidos, registros Modbus inválidos y escenarios cuyo riego inicial fue heredado, siguiendo la restricción de la exportación original.

Por tanto, los **2.878 registros son observaciones brutas**, no la cantidad de muestras aptas. El recuento exacto de muestras y escenarios disponibles se conocerá cuando se ejecute el cuaderno actualizado.

## Interpretación de resultados

El cuaderno mantiene la evaluación con separación por **escenarios completos** cuando hay al menos dos grupos válidos y compara Random Forest con **persistencia**. No presupone que las métricas sean satisfactorias; si la evaluación no supera la referencia, la exportación se llamará `modelo_prediccion_humedad_NO_VALIDADO.pkl`.

Tener solo dos o tres escenarios no garantiza diversidad suficiente para una validación robusta. Para la evaluación académica final se deben disponer de trayectorias suficientes, separar entrenamiento, validación y prueba sin fuga temporal y evaluar también el error del siguiente evento de riego. Si el entrenamiento no supera persistencia, **no copiar el `.pkl` al sistema original**.

La simulación principal `01_Python/Sensores.py` no ha sido modificada.
