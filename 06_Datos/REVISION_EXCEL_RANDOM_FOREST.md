# Revisión del archivo Excel de registros de Random Forest

## Archivo recibido

[**Datos_entrenamiento_guanabana_20261110_103013.xlsx**](Datos_entrenamiento_guanabana_20261110_103013.xlsx) — archivo de registro y entrenamiento, ubicado en `06_Datos/`.

La revisión se realizó sobre la estructura y valores del archivo publicado en GitHub. El archivo no fue modificado.

## Estructura del libro

| Hoja | Filas de datos | Propósito |
|---|---:|---|
| `Registro_10min` | **2.878** | Registros ambientales, riego y estado de comunicación |
| `Entrenamiento_RF` | **813** | Entradas, dos rezagos y humedad objetivo a +10 minutos simulados |
| `EventosRiego` | **3** | Transiciones observadas del riego |
| `ResumenEscenarios` | **1** | Resumen de la primera sesión |
| `Parametros` | **22** | Parámetros y versión de dinámica hídrica |

### Registro_10min

Se identificaron **tres identificadores de sesión**:

| Sesión | Filas en `Registro_10min` |
|---|---:|
| `20261110_103013` | 1.149 |
| `20261110_134831` | 1.226 |
| `20261110_185549` | 503 |
| **Total** | **2.878** |

La columna `Escenario` presenta 2.376 filas con valor `1` y 502 con valor `2`. Esto implica que las combinaciones de `Sesion` + `Escenario` **no deben confundirse con la cantidad de sesiones**. El agrupamiento del entrenamiento debe hacerse por ambos campos.

Rangos observados en la hoja de registro:
- Temperatura: **10–45 °C**.
- Precipitación: **0–30** en la escala de simulación.
- Humedad del suelo: **0–100 %**.
- Estado de riego: **424 lecturas activas** y **2.454 inactivas**.
- La versión `ModeloSueloVersion` es `balance_hidrico_temperatura_v2` en todos los 2.878 registros.

### Entrenamiento_RF

La hoja preparada para el entrenamiento contiene **813 registros**, todos pertenecientes a la sesión `20261110_103013` y al escenario 1. Contiene las **12 variables de entrada** previstas, el objetivo `HumedadObjetivo_10min` y las columnas de trazabilidad `Sesion`, `Escenario`, `TiempoSimuladoMin`, `TiempoObjetivoMin` y `ModeloSueloVersion`.

Los tiempos de entrada y objetivo están definidos para un paso de diez minutos simulados. La humedad de esta tabla varía aproximadamente entre **55,45 y 80,07 %**; la temperatura entre **28 y 45 °C**.

La hoja `ResumenEscenarios` contiene una sola fila: sesión `20261110_103013`, escenario 1, **1.149 muestras registradas**, **813 filas aptas para entrenamiento**, **330 lecturas IR0 inválidas** y **83 muestras con riego activo**. El libro no incluye un resumen consolidado de las otras sesiones.

**Conclusión importante:** la hoja de registros agrupa varias sesiones, pero la tabla preparada para el entrenamiento solo incluye la primera. No deben utilizarse como si representaran exactamente el mismo conjunto de datos.

## Relación con el notebook de entrenamiento

La salida guardada en [`RF_Guanaba.ipynb`](../04_Random_Forest/RF_Guanaba.ipynb) informa la carga de **`Base_guanabana_consolidada_para_RF.xlsx`**, con **2.502 filas válidas** y **3 escenarios independientes**. El archivo publicado en `06_Datos/` tiene un nombre distinto y **solo 813 filas en `Entrenamiento_RF`**.

En consecuencia, el archivo publicado **no reproduce directamente la ejecución almacenada en el notebook**, aunque el registro bruto pueda contener parte de sus datos originales.

Para reproducir las métricas ya registradas en el cuaderno es necesario:
1. Publicar el Excel consolidado exacto `Base_guanabana_consolidada_para_RF.xlsx`, o facilitar un enlace de descarga sujeto a los permisos correspondientes.
2. Si el consolidado se generó a partir de varias exportaciones, documentar cómo se filtraron las lecturas Modbus inválidas, cómo se construyeron las ventanas con rezagos y cómo se trataron los reinicios del reloj y las sesiones.
3. Conservar intacta la base de prueba independiente del notebook y cotejar las métricas del modelo `.pkl` con la ejecución de la cual procede.
4. No trasladar todavía el `.pkl` a `01_Python/`: la ejecución guardada en el cuaderno presenta un **RMSE de 23,3915**, muy superior al **RMSE de persistencia de 0,6709**.

## Alcance de esta revisión

Se comprobó la estructura de las hojas, columnas, conteos y valores almacenados. **No se ejecutó un nuevo entrenamiento ni se recalcularon las métricas del notebook con el Excel recibido**. Los resultados de predicción guardados en el notebook pertenecen a una base diferente a la hoja `Entrenamiento_RF` del Excel publicado.

El paso de mejora debe centrarse en verificar la preparación de los datos por sesión/escenario y el comportamiento sobre escenarios independientes, sin modificar los programas originales del sistema de riego.
