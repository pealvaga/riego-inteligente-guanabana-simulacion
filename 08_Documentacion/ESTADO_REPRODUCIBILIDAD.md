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

## Reproducción del entrenamiento Random Forest

El [simulador alternativo de registro](../04_Random_Forest/simulador_guanabana_grado_registro_RF.py), el [cuaderno vigente](../04_Random_Forest/RF_Guanaba%20(1).ipynb) y el [Excel usado en ese cuaderno](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx) están publicados. El Excel contiene **2.878 filas en `Registro_10min` (tres sesiones)**, pero solo **813 muestras en `Entrenamiento_RF` (un escenario)**. El cuaderno usa estas 813 muestras y una división temporal exploratoria: **647 para entrenamiento y 163 para prueba**.

La salida actual **no validó** Random Forest: RMSE RF **0,6144**, frente a **0,1386** de persistencia. El archivo publicado `modelo_prediccion_humedad.pkl` aún no está ligado inequívocamente a esa ejecución (que exportó `_NO_VALIDADO.pkl`). No copiarlo a `01_Python/` hasta verificar formato, procedencia y desempeño en escenarios independientes. Ver [revisión del entrenamiento vigente](../04_Random_Forest/REVISION_ENTRENAMIENTO_ACTUAL.md) y [resumen de salida](../07_Resultados/RF_metricas_preliminares_notebook.json).

**Corrección disponible (pendiente de ejecución):** [`RF_Guanaba_todas_sesiones.ipynb`](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb) parte de `Registro_10min` y reconstruye muestras con rezagos para todas las sesiones y escenarios, aplicando validaciones por ventana. Ver [guía de uso](../04_Random_Forest/COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md). Los resultados 813/647/163 corresponden al notebook anterior, no a la ejecución futura de este cuaderno corregido.

## Reproducción de MobileNetV2

El [script original](../05_MobileNetV2/ia_imagen.py) y el [modelo fine-tuned](../05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) están publicados. El script separa rutas con `train_test_split` (70/15/15, semilla 42), pero no conserva agrupación por imagen original o planta. Calcula métricas con umbral 0,50 **antes** del fine-tuning y luego guarda el checkpoint; la evaluación de dicho checkpoint debe realizarse de forma independiente, usando umbrales 0,50 y 0,90 y documentando la matriz de confusión. Ver [guía de evaluación final](../05_MobileNetV2/GUIA_EVALUACION_FINAL.md) y [plantilla del manifiesto](../06_Datos/plantilla_manifest_imagenes.csv).

El [inventario de 2.247 imágenes](../06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md) identificó **74 pares idénticos** en la clase Deficiencia. Debe evaluarse si los archivos duplicados u otras variantes quedaron en particiones distintas antes de presentar resultados del checkpoint final.

## Evidencia de ejecución integrada aportada

Se revisaron inicialmente cinco capturas del entorno operativo: Factory I/O muestra servidor **`CoDeSys.OPC.DA (14)`** conectado, Python muestra **«COMUNICACIÓN OK»** mediante Modbus TCP a `127.0.0.1:502`, y CODESYS muestra el dispositivo conectado, la aplicación **`[ejecutar]`** y la visualización SCADA activa. La prueba incorpora el simulador alternativo con registro para Random Forest, cuyo mensaje **«MODELO NUEVO CARGADO» no certifica validez predictiva**. Para detalles y limitaciones consultar [reporte de evidencia integrada](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Actualización:** tres capturas adicionales evidencian compilación de `Device.Application` con **0 errores y 0 advertencias**, escena Factory I/O con dos depósitos, y monitor en línea `Device.Application.GVL` con `FO_Riego1=TRUE`, `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644` y `MB_Temp=350` (35,0 °C a escala ×10). **Pendiente:** subir los veinte PNG originales, documentar un cambio de señales OPC antes/después, verificar las lecturas de los registros Modbus HR0–HR7/IR0 con valores conocidos, revisar diagnóstico de Ethernet y realizar evaluaciones independientes de los modelos.

Se aportaron dos capturas adicionales de una prueba del pulsador de emergencia. La variable `FO_EMERGENCIA` aparece **TRUE** en el monitor GVL, frente a **FALSE** en la captura GVL anterior. Esto respalda una **transición de entrada observada** desde la escena hacia el PLC. No demuestra aún el efecto de parada/rearme en válvulas y salidas. Consultar [E9/E10 en el informe](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

Se recibieron **dos nuevas capturas (E11 y E12)** que muestran, con `FO_EMERGENCIA=TRUE`, las salidas de riego `FO_Riego1=FALSE` y `FO_Riego2=FALSE`, ambas señales de descarga en FALSE y el indicador rojo `FO_LEDR=TRUE`. Frente a la captura anterior (E8), `FO_Riego1` y `FO_S_DESCARGA1` cambiaron de TRUE a FALSE y el indicador verde cambió a FALSE. Ello respalda una respuesta lógica coherente con la parada durante la emergencia, aunque no prueba de forma aislada la causa ni certifica seguridad física. **Pendiente** comprobar rearme y revisar por qué Factory I/O muestra un chorro de llenado en el tanque derecho mientras CODESYS presenta `FO_Llenado2=0`. Ver [informe E11/E12](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Rearme observado (E13–E16):** nuevas capturas de Factory I/O y GVL muestran la transición `FO_EMERGENCIA` TRUE→FALSE, `FO_LEDR` TRUE→FALSE, `FO_LEDV` FALSE→TRUE y `FO_Riego2` FALSE→TRUE junto con `FO_S_DESCARGA2` FALSE→TRUE. Ya no se aprecia el chorro de llenado en las vistas posteriores. `FO_STOP` permanece TRUE; se deben verificar su polaridad y las condiciones de reactivación del riego tras liberar emergencia. Esta secuencia es evidencia funcional de la simulación, no certificación de seguridad. Consultar [E13–E16](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

**Estado posterior sin riego (E17–E20):** nuevas vistas de Factory I/O y monitor GVL presentan `FO_EMERGENCIA=FALSE`, `FO_Riego1=FALSE`, `FO_Riego2=FALSE`, `FO_S_DESCARGA1=FALSE`, `FO_S_DESCARGA2=FALSE`, `FO_LEDA=TRUE` y `FO_LEDV=FALSE`. Son coherentes con detención/espera del proceso, pero `FO_STOP` aparece TRUE tanto antes como después; **no debe atribuirse el cambio únicamente a una nueva pulsación de STOP** sin comprobar la lógica y transiciones. Ver [E17–E20](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md).

## Correspondencia académica

La documentación técnica debe acompañarse de evidencias de ejecución, configuración y resultados medidos con los mismos artefactos publicados. La comprobación de componentes a partir de archivos **no equivale** a una prueba funcional realizada en CODESYS/Factory I/O.

### Aspectos que requieren conciliación en el documento escrito

- La escena entregada configura `OPCClientDA` (`CoDeSys.OPC.DA`), mientras que el informe escrito describe el enlace con Factory I/O como OPC UA. Debe verificarse el protocolo utilizado en la ejecución final y corregirse el informe o la configuración para que coincidan.

- El proyecto de CODESYS incluye comparaciones estrictas `< 60` y `> 75`; el trabajo escrito utiliza límites inclusivos.
- La Tabla 1 del trabajo describe HR0–HR4 e IR0, mientras que Python utiliza HR0–HR7 para incluir día, hora y minuto.
- El CSV registra `RiegoActivo` a partir de `GVL.Riego`, mientras que Python lee un registro construido desde `GVL.Regando`: verificar que ambas variables representen efectivamente el mismo estado.
- El CSV no incluye identificador de sesión; documentar los cambios de trayectoria al preparar los datos para evaluación temporal independiente.
