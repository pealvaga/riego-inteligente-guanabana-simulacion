# Lista de verificación — primera observación del docente

**Revisión del 11/11/2026:** la evaluación **Random Forest v2** ya está publicada y **supera persistencia** (RMSE 0,114327 frente a 0,172037). Los informes antiguos que reportan **NO VALIDADO** corresponden a entrenamientos **anteriores**, no al modelo publicado en [Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2). La identidad de bytes del `.pkl` **ya se verificó** mediante comparación SHA-256 de la copia local y GitHub Release; permanecen pendientes la prueba de carga/compatibilidad en Python y la evaluación de generalización.

**Estado de publicación:** las **21 capturas E1–E21 están publicadas y el PNG 21 fue cotejado con su original**. La lista detallada incluye verificaciones opcionales y metodológicas que no significan que falten archivos. Para priorizar lo necesario para la entrega, ver [PENDIENTES_CIERRE_REPOSITORIO.md](PENDIENTES_CIERRE_REPOSITORIO.md).

## Objetivo del primer punto

Publicar una versión **identificable y reproducible** del proyecto de simulación: fuentes, proyectos editables, modelos, datos pertinentes, entrenamiento, configuración, instrucciones y evidencia de funcionamiento. La existencia de los archivos en GitHub no demuestra automáticamente que el software funcione en otro equipo.

**Convención:** `[x]` = artefacto publicado o documentación preparada; `[ ]` = comprobación o entrega todavía pendiente. Esta lista no certifica ejecución física ni resultados de modelos.

| Elemento | Estado | Ubicación y comprobación pendiente |
|---|---|---|
| Repositorio público con descripción y componentes | [x] | [README principal](../README.md) |
| Python original del sistema | [x] | [`Sensores.py`](../01_Python/Sensores.py) |
| Paquete CODESYS final publicado | [x] | [`Simulación guanabana codesys (2).zip`](../02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip), **8.906.941 bytes** (objeto Git `0154d1f7af90e3bec0958a563d9cbaed0d1a59a9`), subido tras guardar el proyecto. **Falta comprobar la extracción y apertura interna de `Grado.project`**; no altera la evidencia de compilación de la aplicación previamente ejecutada. |
| Escena editable Factory I/O | [x] | [`Grado.factoryio`](../03_Factory_IO/Grado.factoryio) |
| Código de entrenamiento MobileNetV2 y modelo `.keras` | [x] | [`05_MobileNetV2/`](../05_MobileNetV2/) |
| Acceso documentado a imágenes y fuentes | [x] | [README MobileNetV2](../05_MobileNetV2/README.md); comprobar permisos y licencias |
| Inventario de imagen, duplicados y trazabilidad parcial | [x] | [`06_Datos/`](../06_Datos/); completar especie, fuente y etiqueta original |
| Script y cuaderno de RF en carpeta separada | [x] | [`04_Random_Forest/`](../04_Random_Forest/) |
| Excel de registros RF en GitHub | [x] | [Archivo actual](../06_Datos/Datos_entrenamiento_guanabana_20261110_103013.xlsx) de **729.049 bytes**, vinculado al [archivo de origen SHA-256](../04_Random_Forest/origen_excel_RF.json) y al [entrenamiento v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md) |
| Cuaderno que prepara múltiples sesiones RF | [x] | [Notebook reproducible](../04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb), ejecutado sobre el Excel actual; **4.552 muestras entrenamiento / 922 prueba**, mejora frente a persistencia. [Informe v2](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md). |
| Guía de ejecución integrada | [x] | [`GUIA_REPRODUCCION_INTEGRAL.md`](GUIA_REPRODUCCION_INTEGRAL.md) |
| Versiones instaladas de Python y paquetes verificadas | [x] | [`ENTORNO_EJECUTADO.json`](ENTORNO_EJECUTADO.json) y [salida PowerShell del 11/11/2026](VERIFICACION_POWERSHELL_LIBRERIAS_20261111.md): **Python 3.12.9**, **pip 24.3.1** y versiones coincidentes de diez librerías principales. **Por completar:** `pip freeze` completo y vínculo con el intérprete efectivo de `Sensores.py`. |
| Versión del IDE CODESYS y componentes mostrados | [x] | [Registro del entorno CODESYS](ENTORNO_CODESYS_REGISTRADO.md): V3.5 SP9 Patch 1; Device Modbus TCP Slave 3.5.9.10 |
| Versión del runtime CODESYS Control Win V3 | [x] | [Control Win **3.5.9.10**](VERSIONES_SOFTWARE_CONFIRMADAS.md), confirmada por captura de pantalla de inicio |
| OPCConfig: versión instalada | [x] | [**3.5.9.0**](VERSIONES_SOFTWARE_CONFIRMADAS.md); **no es prueba de enlace OPC DA** |
| Versión instalada de Factory I/O | [x] | [**2.5.10**](VERSIONES_SOFTWARE_CONFIRMADAS.md), confirmada por pantalla Update Checker |
| Compilación de CODESYS sin errores ni advertencias | [x] | [Evidencia E6](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): **0 errores, 0 advertencias**, 3 mensajes informativos |
| CODESYS conectado y aplicación en ejecución | [x] | Captura con `Device [Conectado]` y `Application [ejecutar]` |
| Monitorización GVL con valores del proceso | [x] | Captura E8: `FO_Riego1=TRUE`, `FO_S_NIVEL1=5.045404`, `FO_S_NIVEL2=9.539644`, `MB_Temp=350` |
| Bibliotecas del proyecto y diagnóstico de Ethernet | [ ] | Registrar bibliotecas realmente usadas y verificar el icono de advertencia Ethernet |
| Conexión indicada por Factory I/O con OPC DA y 14 señales | [x] | La captura E1 publicada muestra estado verde y `CoDeSys.OPC.DA (14)`; queda pendiente verificar cambios de señales durante una prueba sincronizada |
| Verificación dinámica de señales OPC DA | [ ] | Contrastar al menos una señal de entrada y una de salida antes/después en Factory I/O y CODESYS |
| Evidencia visual de ejecución integrada | [x] | [Revisión de veinte capturas](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): incluye compilación CODESYS sin errores, variables GVL, Python Modbus OK y Factory I/O OPC DA (14) conectado; **20 PNG (E1–E20) publicados** |
| Cambio observado FO_EMERGENCIA en CODESYS | [x] | [Capturas E8 y E10](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): antes **FALSE**, después **TRUE**, junto con captura del pulsador de emergencia en Factory I/O; falta comprobar el efecto sobre salidas |
| Desactivación de salidas de riego con emergencia activa | [x] | [Comparación E8/E12](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_Riego1` TRUE→FALSE, `FO_Riego2` FALSE, `FO_S_DESCARGA1` TRUE→FALSE, `FO_LEDR` FALSE→TRUE. Evidencia visual de secuencia, no certificación de seguridad. |
| Rearme observado en simulación después de emergencia | [x] | [E14/E16](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_EMERGENCIA` TRUE→FALSE, `FO_LEDR` TRUE→FALSE, `FO_LEDV` FALSE→TRUE, `FO_Riego2` FALSE→TRUE |
| Estado sin riego e indicador amarillo observado | [x] | [E16/E19](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md): `FO_Riego2` TRUE→FALSE, `FO_S_DESCARGA2` TRUE→FALSE, `FO_LEDA` FALSE→TRUE, sin emergencia activa |
| Polaridad prevista de STOP documentada | [x] | El pulsador STOP está configurado como **normalmente cerrado (NC)**: `FO_STOP=TRUE` en reposo, `FALSE` esperado al pulsarlo. Ver [aclaración técnica](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md). |
| Efecto específico de pulsar STOP y orden START | [ ] | Registrar transición **TRUE→FALSE** al pulsar, verificar salidas/indicador amarillo y si se exige START para reactivar; aún sin captura dinámica de esa pulsación |
| Confirmar lógica de reinicio, pulsador STOP y llenado | [ ] | `FO_STOP=TRUE` corresponde al **reposo del pulsador NC**. Verificar en ejecución la pulsación TRUE→FALSE y si el riego se habilita automáticamente al soltar emergencia o requiere START. No se ve chorro de llenado en las nuevas capturas, pero falta prueba sincronizada |
| Demostración de instalación desde cero y validación funcional detallada | [ ] | Registrar compilación, errores, verificación individual de señales y evidencia de arranque en otra instalación o desde cero |
| Modelo RF v2 publicado y superior a persistencia | [x] | [Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2): `modelo_prediccion_humedad.pkl` de 53.111.758 bytes. **RMSE 0,114327 vs. persistencia 0,172037**, 4 escenarios de prueba favorables. [Métricas](../04_Random_Forest/metricas_random_forest.json). |
| Integridad de la copia local y adjunto GitHub de RF v2 | [x] | La salida de PowerShell aportada del archivo local muestra SHA-256 **`c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`**, idéntico al hash anunciado por [GitHub Release `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2). Identidad de bytes confirmada. |
| Estructura, compatibilidad y funcionamiento del `.pkl` RF v2 | [ ] | Verificar carga de paquete, versión `scikit-learn`, variables/orden, paso de 10 minutos e inferencia desde `01_Python/Sensores.py`; **la coincidencia de hash no prueba ejecución funcional**. |
| Excel consolidado final de RF y particiones | [x] | [Excel consolidado v2](../04_Random_Forest/Base_guanabana_consolidada_para_RF.xlsx) publicado; se reconstruyen **5.474 muestras** (4.552/922 según métricas) en **13 grupos de sesión/escenario**. **Pendiente** manifestar formalmente qué grupos se reservaron para la prueba y conservar parámetros de los escenarios. |
| Resultados RF v2: CSV, JSON y comparación con persistencia | [x] | [CSV de 922 predicciones](../04_Random_Forest/resultados_prueba_random_forest.csv), [JSON original](../04_Random_Forest/metricas_random_forest.json) e [informe con desglose por escenario](../07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md). **Supera persistencia en cuatro escenarios**. |
| Evidencia visual de estimación del próximo riego | [x] | [Captura revisada y datos transcritos](../07_Resultados/RF_EVIDENCIA_ESTIMACION_PROXIMO_RIEGO_20261111.md): humedad inicial 70 %, humedad actual 69,61 %, +10 min 69,60 %, riego inactivo y **próximo riego estimado Día 3 – 23:30**. **PNG original ya publicado y verificado por SHA-1 de objeto Git**: [captura 21](../07_Resultados/evidencias_integracion_guanabana/21_rf_v2_pronostico_proximo_riego.png); la fecha de riego sigue siendo proyectada, sin contrastar aún con el evento real. |
| Evaluación del momento del próximo riego en minutos simulados | [ ] | La exactitud a +10 minutos fue corroborada con **21 parejas tomadas con 10 minutos simulados de separación** ([informe](../07_Resultados/RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md)), pero el **instante del próximo riego** continúa sin error medido. La función puede mostrar «NO ESTIMADO» si el descenso proyectado es ≤0,01 p.p./10 min o la extrapolación supera 72 horas ([diagnóstico y prueba controlada](../07_Resultados/RF_DIAGNOSTICO_PROXIMO_RIEGO_NO_ESTIMADO.md)). |
| Validación RF con sesión completamente nueva | [ ] | Los 4 escenarios de prueba (922 filas) pertenecen a la misma sesión `20261111_083605`. Comprobar generalización sin volver a ajustar el modelo con esa sesión. |
| Script y cuaderno de evaluación MobileNetV2 | [x] | [Script y Colab disponibles](../05_MobileNetV2/COMO_EVALUAR_CHECKPOINT_FINAL.md), con primera ejecución final del checkpoint ya realizada; evaluación preliminar, independencia no acreditada |
| Evaluación exploratoria checkpoint MobileNetV2 ejecutada | [x] | [100 imágenes: 50 sanas + 50 deficiencia](../07_Resultados/MobileNetV2/INFORME_PRELIMINAR_20261111.md); accuracy 0,67 a 0,50 y 0,63 a 0,90; métricas agregadas publicadas. **Independencia no acreditada.** |
| Procedencia declarada de las 50 imágenes de deficiencia de prueba | [x] | Las **100 imágenes de prueba** (50 sanas y 50 etiquetadas con deficiencia) se seleccionaron como **guanábana (`Annona muricata`)**. Las 50 con deficiencia se localizaron mediante Google Imágenes. **Pendiente verificar las páginas originales, la independencia entre fotos, los diagnósticos y los permisos de uso**. |
| Evaluación independiente del checkpoint MobileNetV2 a 0,90 | [ ] | Completar procedencia/especie y grupos de origen de las 100 capturas, verificar que no participaron en ajuste, y publicar matrices/CSV de prueba verificable; hay 37 falsos negativos de 50 con umbral 0,90 |
| Evidencias visuales de integración E1–E21 publicadas | [x] | **21 capturas PNG (E1 a E21)** presentes en [evidencias_integracion_guanabana/](../07_Resultados/evidencias_integracion_guanabana/); el [informe de integración](../07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md) describe E1–E20 y el [informe de RF](../07_Resultados/RF_EVIDENCIA_ESTIMACION_PROXIMO_RIEGO_20261111.md) describe E21. Publicación comprobada; quedan límites de validación documentados. |
| Coherencia documental CODESYS/Factory I/O/tesis | [ ] | Corregir OPC DA versus OPC UA, límites de histéresis y mapa HR/IR según uso real |
| Enlace de GitHub e instrucciones incorporados en Anexo C del documento | [ ] | Comprobar que apunte a la revisión final y a las rutas correctas |

## Evidencia complementaria de predicción de humedad

Se recibió una tabla con **21 parejas de humedad estimada y observada**, conservada en el [informe](../07_Resultados/RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md) y [CSV](../07_Resultados/RF_comparacion_operativa_21_pares_20261111.csv): **MAE 0,00429** y **RMSE 0,00655**, calculados con valores redondeados a dos decimales. La humedad real se mantuvo entre **75,52 y 76,61 %**. **Se confirmó que cada valor real se tomó exactamente 10 minutos simulados después de su predicción.** La tabla no conserva marcas de tiempo de cada pareja ni captura que identifique `rf-v2` en esa ejecución; adjuntar esas evidencias si están disponibles. No equivale a nueva evaluación independiente por escenarios.

## Estado aclarado tras la revisión con el equipo

- **Prueba funcional de Python, CODESYS y Factory I/O:** se reporta que se realizaron **múltiples veces con funcionamiento satisfactorio**. Las 20 capturas ya publicadas respaldan distintos estados y secuencias. Los controles específicos que todavía figuran como pendientes (p. ej., transición STOP NC en GVL) se refieren a la **evidencia documental de una transición concreta**, no a que el sistema se haya declarado averiado ni a la necesidad de repetirlo todo.
- **Integridad del modelo RF:** el archivo de PowerShell aportado confirma SHA-256 idéntico entre la copia local y GitHub Release. **Queda pendiente la prueba específica de carga e inferencia con `rf-v2` en Python**; se preparó el [protocolo mínimo](../07_Resultados/PROTOCOLO_VERIFICACION_RF_V2_EN_PYTHON.md).
- **MobileNetV2:** se propone cerrar la explicación académica con el desempeño observado: **50/50 sanas correctamente clasificadas**, **13/50 deficientes detectadas a 0,90**; fotos deficientes recopiladas mediante Google Imágenes; umbral **0,90** conservador para **autorizar fertirriego**, no margen de error estadístico. Se recomienda una base futura de imágenes de guanábana **con deficiencia nutricional verificada**. La prueba independiente/diagnóstica no queda acreditada solo por esta explicación.

## Trabajo que puede completarse mientras se generan datos RF

- Capturar versiones de Python, scikit-learn, TensorFlow, pymodbus y demás dependencias **desde el ordenador donde funciona el sistema**.
- Obtener capturas de CODESYS compilado, visualización SCADA, configuración Modbus, Factory I/O y estado de OPC DA.
- Probar la secuencia de instalación/ejecución con la [guía integral](GUIA_REPRODUCCION_INTEGRAL.md), dejando constancia de pasos que deban corregirse.
- Completar la trazabilidad y licencias del conjunto de imágenes, revisando la disponibilidad del Drive y las fuentes oficiales.
- Preparar el inventario de pruebas/escenarios e identificar cada ejecución con fecha, hora simulada y versiones.
- Corregir el texto del documento de grado para que describa exactamente el código y los protocolos finales.

## Precauciones para nuevos registros con humedad igual a 0

En la simulación, `HumedadSuelo` es el **porcentaje de agua disponible** calculado según el balance hídrico, no humedad volumétrica directa. Por tanto, `0 %` representa el límite inferior de agua disponible del modelo y debe etiquetarse así. Guardar únicamente trayectorias coherentes con las reglas de simulación; no alterar arbitrariamente columnas para introducir ceros artificiales. Generar escenarios diversos (secos, con lluvia y con riego), con estados de Modbus válidos y sin mezclar sesiones al construir rezagos.

La primera observación se considerará cerrada cuando otro evaluador pueda **acceder a los componentes, reconstruir el entorno y repetir los pasos documentados**, con las limitaciones y resultados medidos claramente identificados. La segunda observación exige además validez metodológica de las evaluaciones de IA y comparación con las referencias.
