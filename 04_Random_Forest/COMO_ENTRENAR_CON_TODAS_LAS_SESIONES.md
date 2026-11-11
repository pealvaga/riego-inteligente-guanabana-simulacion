# Entrenar Random Forest con todas las sesiones de Registro_10min

El [cuaderno corregido](RF_Guanaba_todas_sesiones.ipynb) se creó porque la versión anterior leía únicamente `Entrenamiento_RF` de una **base histórica** con 813 ejemplos de una sesión, aunque `Registro_10min` contenía 2.878 registros brutos de tres sesiones. **Después se reemplazó el Excel en GitHub por una versión con más datos.** Estos recuentos describen el archivo histórico, no la cantidad de registros de la base nueva.

## Uso en Google Colab

1. Abrir el [**cuaderno actualizado en Google Colab**](https://colab.research.google.com/github/pealvaga/riego-inteligente-guanabana-simulacion/blob/main/04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb). **Si Colab ya estaba abierto antes del cambio, cerrar la copia antigua y abrir el notebook de GitHub nuevamente.**
2. En el menú Colab, utilizar **Entorno de ejecución → Reiniciar sesión y ejecutar todas**. La tercera celda de código localiza el único archivo `Datos_entrenamiento_guanabana*.xlsx` de `06_Datos/` en la **rama `main`**, lo descarga **de nuevo en cada ejecución y sobrescribe la copia local**, incluso si el nombre no cambia. Si la descarga falla, permitirá subir el Excel actual manualmente. Si se publican varios archivos con ese prefijo, indicar el nombre exacto en `NOMBRE_EXCEL_GITHUB`.
3. La celda muestra el **nombre, tamaño y SHA-256 del Excel**; comprobar que corresponden a la versión subida. El cuaderno **lee `Registro_10min`, no `Entrenamiento_RF`**, y muestra el número actual de registros y ejemplos válidos por sesión y escenario. No asumir que conserva los 2.878 registros de la versión histórica.
4. El proceso genera el archivo `/content/Base_guanabana_consolidada_para_RF.xlsx` con `Registro_10min`, `Entrenamiento_RF`, `ResumenEscenarios` y `Parametros`.
5. A continuación realiza entrenamiento y evaluación. Descargar `resultados_RF_guanabana.zip`, que incluye la base consolidada, el reporte CSV, el JSON de métricas, el `.pkl` exportado y **`origen_excel_RF.json`** con la huella del Excel utilizado. Subir la base consolidada a `06_Datos/` y los reportes CSV/JSON a `07_Resultados/`, después de comprobar que no incluyan información sensible.

## Por qué no todas las observaciones del Excel son ejemplos de entrenamiento

Cada ejemplo requiere **cuatro observaciones consecutivas** del mismo escenario (t−20, t−10, t y t+10 minutos) con lecturas válidas del estado de riego. Se descartan ventanas con intervalos interrumpidos, registros Modbus inválidos y escenarios cuyo riego inicial fue heredado, siguiendo la restricción de la exportación original.

Por tanto, los registros brutos del Excel actual **no equivalen** a la cantidad de muestras aptas. El cuaderno informa las cantidades reales de la nueva base al ejecutarse. Los 2.878 registros corresponden únicamente a la base anterior.

## Interpretación de resultados

El cuaderno mantiene la evaluación con separación por **escenarios completos** cuando hay al menos dos grupos válidos y compara Random Forest con **persistencia**. No presupone que las métricas sean satisfactorias; si la evaluación no supera la referencia, la exportación se llamará `modelo_prediccion_humedad_NO_VALIDADO.pkl`.

Tener solo dos o tres escenarios no garantiza diversidad suficiente para una validación robusta. Para la evaluación académica final se deben disponer de trayectorias suficientes, separar entrenamiento, validación y prueba sin fuga temporal y evaluar también el error del siguiente evento de riego. Si el entrenamiento no supera persistencia, **no copiar el `.pkl` al sistema original**.

La simulación principal `01_Python/Sensores.py` no ha sido modificada.
