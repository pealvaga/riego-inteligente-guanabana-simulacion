# Procedimiento de verificación y reproducibilidad

Esta guía establece la secuencia de comprobación de la simulación y sus dos modelos de IA.

## Componentes de la simulación

- **Python:** `01_Python/Sensores.py`, comunicación Modbus TCP y simulación ambiental.
- **CODESYS:** `02_CODESYS/Codesys.zip` contiene `Grado.project`, servidor Modbus TCP, programas `OPERACIONES`, `RIEGO` y `REGISTRO_DATOS`.
- **Factory I/O:** `03_Factory_IO/Grado.factoryio`, versión 2.5.10; escena con dos tanques, controles y **14 variables OPC DA** dirigidas al servidor `CoDeSys.OPC.DA`.
- **Datos:** `HistorialCultivo.csv`, que contempla muestreo cada 10 minutos simulados mediante CAA File.

## Verificación de funcionamiento

1. Abrir y compilar `Grado.project` en CODESYS, contrastando bibliotecas y dispositivo.
2. Confirmar que el servidor Modbus TCP utiliza el puerto 502 y que HR0–HR7/IR0 se corresponden con las variables programadas.
3. Abrir la escena de Factory I/O y comprobar la conexión **OPC DA**, la disponibilidad de `CoDeSys.OPC.DA` y el intercambio de las 14 variables `FO_*` con CODESYS; verificar luego el vínculo de estas variables con la HMI y los actuadores.
4. Iniciar la simulación Python y verificar las lecturas/escrituras Modbus.
5. Confirmar el comportamiento de la histéresis y el estado real del riego.
6. Ubicar el archivo `HistorialCultivo.csv`, comprobar sus diez columnas y guardar una ejecución de prueba.
7. Comprobar el manejo de reinicios de reloj y separar las trayectorias antes de construir los conjuntos de aprendizaje.

## Reproducción del entrenamiento Random Forest — modelo actual `rf-v2`

La nueva versión del modelo está publicada en [GitHub Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2) como `modelo_prediccion_humedad.pkl` (53.111.758 bytes). El repositorio incluye [cuaderno de entrenamiento](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb), [Excel de datos](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx), [consolidado](../04_Random_Forest/Base_guanabana_consolidada_para_RF.xlsx), [métricas](../04_Random_Forest/metricas_random_forest.json), [922 predicciones](../04_Random_Forest/resultados_prueba_random_forest.csv) y [registro de procedencia del Excel](../04_Random_Forest/origen_excel_RF.json).

Según el JSON, el entrenamiento utilizó **4.552 muestras**, la prueba **922**, con división por escenarios y **13 grupos** en total. **RMSE RF 0,114327 vs. persistencia 0,172037**, mejora relativa del **33,55 %**, `supera_referencia=true` y `apto_para_prueba_en_aplicacion=true`. Los resultados se recalcularon desde el CSV y se desglosan por escenarios en el [informe v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md). Los **cuatro escenarios de prueba** pertenecen a una sesión; la validación con sesión nueva y el error del tiempo del siguiente riego siguen pendientes.

El archivo del Release tiene SHA-256 publicado por GitHub `c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`. **La copia local del archivo `.pkl` tiene la misma huella SHA-256, según la captura de PowerShell aportada. Falta probar su carga y compatibilidad en la aplicación**. La publicación no implica que se haya instalado en `01_Python`.

### Resultados históricos que no corresponden a `rf-v2`

Los informes y métricas anteriores (813 muestras, o el entrenamiento posterior con 3.243 muestras) reportaron **NO VALIDADO** frente a persistencia. Permanecen conservados como antecedentes, no como estado actual del modelo. El cuaderno antiguo `RF_Guanaba (1).ipynb` ya no figura en el árbol actual de GitHub. Consultar la [revisión histórica](../04_Random_Forest/REVISION_ENTRENAMIENTO_ACTUAL.md).

## Reproducción de MobileNetV2

El [script original](../05_MobileNetV2/ia_imagen.py) y el [modelo fine-tuned](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) están publicados. El script separa rutas con `train_test_split` (70/15/15, semilla 42), pero no conserva agrupación por imagen original o planta. Calcula métricas con umbral 0,50 **antes** del fine-tuning y luego guarda el checkpoint; la evaluación de dicho checkpoint debe realizarse de forma independiente, usando umbrales 0,50 y 0,90 y documentando la matriz de confusión. Ver [guía de evaluación final](../05_MobileNetV2/GUIA_EVALUACION_FINAL.md) y [plantilla del manifiesto](../06_Datos/plantilla_manifest_imagenes.csv).

El [inventario de 2.247 imágenes](../06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md) identificó **74 pares idénticos** en la clase Deficiencia. Debe evaluarse si los archivos duplicados u otras variantes quedaron en particiones distintas antes de presentar resultados del checkpoint final.

## Evidencia de ejecución integrada

Se revisaron inicialmente cinco capturas del entorno operativo: Factory I/O muestra servidor **`CoDeSys.OPC.DA (14)`** conectado, Python muestra **«COMUNICACIÓN OK»** mediante Modbus TCP a `127.0.0.1:502`, y CODESYS muestra el dispositivo conectado, la aplicación **`[ejecutar]`** y la visualización SCADA activa. La prueba incorpora el simulador alternativo con registro para Random Forest, cuyo mensaje **«MODELO NUEVO CARGADO» no certifica validez predictiva**. Para detalles y limitaciones consultar [reporte de evidencia integrada](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Actualización:** tres capturas adicionales evidencian compilación de `Device.Application` con **0 errores y 0 advertencias**, escena Factory I/O con dos depósitos, y monitor en línea `Device.Application.GVL` con `FO_Riego1=TRUE`, `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644` y `MB_Temp=350` (35,0 °C a escala ×10). **Archivos de evidencia E1–E20 publicados en GitHub:** queda pendiente documentar un cambio de señales OPC antes/después, verificar las lecturas Modbus HR0–HR7/IR0 con valores conocidos, revisar diagnóstico de Ethernet y completar evaluaciones independientes de los modelos.

Se aportaron dos capturas adicionales de una prueba del pulsador de emergencia. La variable `FO_EMERGENCIA` aparece **TRUE** en el monitor GVL, frente a **FALSE** en la captura GVL anterior. Esto respalda una **transición de entrada observada** desde la escena hacia el PLC. No demuestra aún el efecto de parada/rearme en válvulas y salidas. Consultar [E9/E10 en el informe](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

Las capturas **E11 y E12** que muestran, con `FO_EMERGENCIA=TRUE`, las salidas de riego `FO_Riego1=FALSE` y `FO_Riego2=FALSE`, ambas señales de descarga en FALSE y el indicador rojo `FO_LEDR=TRUE`. Frente a la captura anterior (E8), `FO_Riego1` y `FO_S_DESCARGA1` cambiaron de TRUE a FALSE y el indicador verde cambió a FALSE. Ello respalda una respuesta lógica coherente con la parada durante la emergencia, aunque no prueba de forma aislada la causa ni certifica seguridad física. **Pendiente** comprobar rearme y revisar por qué Factory I/O muestra un chorro de llenado en el tanque derecho mientras CODESYS presenta `FO_Llenado2=0`. Ver [informe E11/E12](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Rearme observado (E13–E16):** nuevas capturas de Factory I/O y GVL muestran la transición `FO_EMERGENCIA` TRUE→FALSE, `FO_LEDR` TRUE→FALSE, `FO_LEDV` FALSE→TRUE y `FO_Riego2` FALSE→TRUE junto con `FO_S_DESCARGA2` FALSE→TRUE. Ya no se aprecia el chorro de llenado en las vistas posteriores. `FO_STOP` permanece TRUE; su valor TRUE es normal según la configuración NC declarada; se deben comprobar la pulsación a FALSE y las condiciones de reactivación del riego tras liberar emergencia. Esta secuencia es evidencia funcional de la simulación, no certificación de seguridad. Consultar [E13–E16](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Estado posterior sin riego (E17–E20):** nuevas vistas de Factory I/O y monitor GVL presentan `FO_EMERGENCIA=FALSE`, `FO_Riego1=FALSE`, `FO_Riego2=FALSE`, `FO_S_DESCARGA1=FALSE`, `FO_S_DESCARGA2=FALSE`, `FO_LEDA=TRUE` y `FO_LEDV=FALSE`. Son coherentes con detención/espera del proceso, pero `FO_STOP` aparece TRUE tanto antes como después; **no debe atribuirse el cambio únicamente a una nueva pulsación de STOP** sin comprobar la lógica y transiciones. Ver [E17–E20](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Aclaración del pulsador STOP:** `FO_STOP` se configuró con lógica **normalmente cerrada (NC)**: `TRUE` representa el pulsador en reposo y `FALSE` es el estado esperado al pulsarlo. Por eso, las capturas anteriores con `FO_STOP=TRUE` **no deben interpretarse como una parada solicitada**. Esta configuración debe verificarse con una captura de la pulsación `TRUE→FALSE` y la reacción de salidas. El cambio a indicador amarillo observado en E17–E20 **no puede atribuirse a STOP** sin ese evento. El retorno automático o mediante START aún requiere comprobación.

## Correspondencia académica

La documentación técnica debe acompañarse de evidencias de ejecución, configuración y resultados medidos con los mismos artefactos publicados. La comprobación de componentes a partir de archivos **no equivale** a una prueba funcional realizada en CODESYS/Factory I/O.

### Aspectos que requieren conciliación en el documento escrito

- La escena entregada configura `OPCClientDA` (`CoDeSys.OPC.DA`), mientras que el informe escrito describe el enlace con Factory I/O como OPC UA. Debe verificarse el protocolo utilizado en la ejecución final y corregirse el informe o la configuración para que coincidan.

- El proyecto de CODESYS incluye comparaciones estrictas `< 60` y `> 75`; el trabajo escrito utiliza límites inclusivos.
- La Tabla 1 del trabajo describe HR0–HR4 e IR0, mientras que Python utiliza HR0–HR7 para incluir día, hora y minuto.
- El CSV registra `RiegoActivo` a partir de `GVL.Riego`, mientras que Python lee un registro construido desde `GVL.Regando`: verificar que ambas variables representen efectivamente el mismo estado.
- El CSV no incluye identificador de sesión; documentar los cambios de trayectoria al preparar los datos para evaluación temporal independiente.
