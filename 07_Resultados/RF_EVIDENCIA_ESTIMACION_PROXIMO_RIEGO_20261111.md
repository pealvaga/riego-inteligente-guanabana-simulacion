# Evidencia de estimación del próximo riego — Random Forest (11/11/2026)

## Registro de la pantalla de la aplicación

Se recibió una captura de la pestaña **«Simulación ambiental»** del **«Simulador ambiental del cultivo de guanábana»**. El escenario se inició con humedad configurada de **70 %**, temperatura de **28 °C** y precipitación de **0 mm/h**. En el instante fotografiado se muestran:

| Elemento de la interfaz | Valor visible |
|---|---|
| Comunicación Modbus | **COMUNICACIÓN OK** |
| IA predictiva | **MODELO NUEVO CARGADO** |
| Temperatura configurada | **28,0 °C** |
| Precipitación configurada | **0,0 mm/h** |
| Humedad inicial configurada | **70 %** |
| Tiempo simulado mostrado | **Día 1, 03:38** |
| Humedad actual mostrada | **69,61 % de agua disponible** |
| Humedad predicha a +10 minutos | **69,60 %** |
| Próximo riego estimado por la aplicación | **Día 3, 23:30** |
| Riego recibido desde CODESYS | **INACTIVO** |
| Estado de simulación | **EN EJECUCIÓN** |
| Tipo de riego (IA de imagen) | **SIN DECISIÓN** |

**Interpretación:** a diferencia de ensayos anteriores donde la pantalla mostraba «NO ESTIMADO CON LAS CONDICIONES ACTUALES», esta ejecución exhibe una **fecha y hora de próximo riego**, mientras la humedad desciende y el riego está inactivo. Es evidencia de que el cálculo de estimación **puede producir una salida** bajo estas condiciones; no demuestra todavía la exactitud temporal de esa salida.

### Archivo de imagen

- Nombre del archivo publicado: [`21_rf_v2_pronostico_proximo_riego.png`](evidencias_integracion_guanabana/21_rf_v2_pronostico_proximo_riego.png).
- Ubicación verificada: `07_Resultados/evidencias_integracion_guanabana/21_rf_v2_pronostico_proximo_riego.png`.
- Formato de la imagen recibida: **PNG**, **1195 × 895** píxeles.
- Huella SHA-256 de la captura **recibida**: `004ee0330a8b9a85ba39a93e97c235ddbf08c6e5b8a3ffab2b9344b8990ad54d`.
- **Estado verificado:** el PNG **sí está publicado en GitHub**. El objeto Git de la rama `main` tiene SHA-1 de blob `1fc80448fbe235d34fd23dbf732926883e8efc86` (144.776 bytes), **coincidente con el blob calculado a partir de la captura original recibida**. El SHA-256 original es `004ee0330a8b9a85ba39a93e97c235ddbf08c6e5b8a3ffab2b9344b8990ad54d`. Esto acredita identidad de la imagen publicada.

## Alcance y limitaciones

1. La captura muestra un modelo cargado, pero **no prueba por sí sola** qué SHA-256 del archivo `.pkl` está activo dentro de esa ejecución. El archivo local de `rf-v2` sí coincidió por hash con el de GitHub Release en una comprobación separada.
2. La humedad proyectada `69,60 %` **no debe compararse directamente** con el valor visible de `69,61 %` como si fuera una medición futura: la IA se actualiza en intervalos de diez minutos simulados y el reloj mostrado está en `03:38`; por ello los dos valores visibles pueden corresponder a instantes diferentes.
3. La fecha del próximo riego **es una estimación**; la imagen no demuestra que CODESYS haya iniciado el riego efectivamente el **día 3 a las 23:30**.
4. Para medir el error del momento de próximo riego, registrar la **fecha/hora de activación real** cuando la humedad cruce el umbral del PLC (**menor que 60 %**, según el extracto del código) y compararla con la fecha prevista; si las condiciones climáticas o el riego cambian, consignarlo.
5. La señal de estado `Riego recibido desde CODESYS: INACTIVO` respalda que el programa no estaba regando en el momento de la captura. No acredita por sí sola una evaluación futura completa de la lógica del PLC.

## Resultado

**Comprobada visualmente la capacidad de presentar una estimación concreta de próximo riego en el programa ejecutándose.** La captura original **ya está publicada y se verificó su integridad**. Permanece pendiente la validación del **error temporal** de esa fecha estimada frente a la activación real de riego.

Ver también el [diagnóstico del mensaje «NO ESTIMADO»](RF_DIAGNOSTICO_PROXIMO_RIEGO_NO_ESTIMADO.md) y la [comparación de 21 pronósticos a diez minutos simulados](RF_COMPROBACION_OPERATIVA_21_PREDICCIONES_20261111.md). No se modificaron archivos de Python, CODESYS, Factory I/O ni los modelos.
