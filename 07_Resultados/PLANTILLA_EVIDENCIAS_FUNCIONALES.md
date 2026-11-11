# Plantilla para registrar pruebas del sistema de riego

Este archivo es una **plantilla vacía de verificación**, no un resultado observado. Crear una copia por cada ejecución comprobada, y colocar sus capturas y datos derivados en `07_Resultados`.

## Identificación

- Fecha de prueba:
- Responsable:
- Commit de GitHub utilizado:
- Sistema operativo:
- Versión de Python y dependencias (enlace al reporte):
- Versión de CODESYS IDE y Control Win:
- Versión de Factory I/O:
- Configuración activa de OPC DA:
- Modelo Random Forest y versión/huella (si existe y está validado):
- Modelo MobileNetV2 y versión/huella:
- Archivo o sesión de datos utilizada:

## Registro de verificaciones

| Caso | Procedimiento de prueba | Resultado (pendiente / aprobado / no aprobado) | Evidencia |
|---|---|---|---|
| 01 | Abrir y compilar el proyecto CODESYS | Pendiente | |
| 02 | Verificar servicio virtual y variables HR0–HR7 e IR0 | Pendiente | |
| 03 | Abrir Factory I/O y comprobar 14 señales OPC DA | Pendiente | |
| 04 | Ejecutar Python y conectar Modbus TCP | Pendiente | |
| 05 | Cambiar temperatura y observar balance hídrico | Pendiente | |
| 06 | Cambiar precipitación y observar balance hídrico | Pendiente | |
| 07 | Comprobar condiciones de arranque/paro del riego y valores frontera | Pendiente | |
| 08 | Observar niveles y actuadores de los tanques | Pendiente | |
| 09 | Verificar indicadores de interfaz SCADA y señales de emergencia | Pendiente | |
| 10 | Generar y localizar `HistorialCultivo.csv` | Pendiente | |
| 11 | Cargar una imagen y verificar salida de MobileNetV2 y umbral 0,90 | Pendiente | |
| 12 | Si hay RF validado: cargar paquete y verificar predicción | Pendiente | |
| 13 | Generar Excel de sesiones para entrenamiento RF | Pendiente | |
| 14 | Ejecutar evaluación RF: comparativa de persistencia y error próximo riego | Pendiente | |
| 15 | Ejecutar evaluación MobileNetV2: métricas y matriz a 0,90 | Pendiente | |

## Observaciones e incidencias

- Comportamiento esperado:
- Comportamiento obtenido:
- Limitaciones:
- Errores, rutas o ajustes necesarios:
- Resultado de repetición de prueba:

## Archivos de evidencia recomendados

Ejemplos de nombres que se pueden utilizar una vez existan capturas reales:

```text
07_Resultados/
  prueba_YYYYMMDD/
    01_codesys_compilacion.png
    02_codesys_modbus.png
    03_factoryio_opc_da.png
    04_scada_variables.png
    05_python_conexion.png
    06_sensores_humedad.png
    07_evento_riego.png
    08_clasificacion_foliar.png
    09_historial_registro.csv
    entorno_python.json
    informe_pruebas.md
```

**No generar capturas ficticias ni rellenar como «aprobado» sin una prueba real.** Diferenciar evidencias de control simulado de una posible validación agronómica en campo.
