# Simulación de un sistema de riego inteligente para cultivos de guanábana

> **Estado actual: documentación inicial.** Los programas, modelos de IA y conjuntos de datos originales todavía no se han incorporado ni verificado; el repositorio aún no es una reproducción ejecutable.

Trabajo de grado de Ingeniería Mecatrónica, modalidad diplomado, Universitaria Agustiniana (2026). Se presenta una simulación para cultivos de guanábana (*Annona muricata* L.) a cielo abierto.

## Arquitectura del proyecto

- **Python:** simulación ambiental y dinámica de humedad; interfaz y comunicación Modbus TCP.
- **CODESYS:** controlador virtual, lógica de riego, HMI SCADA y registro histórico.
- **Factory I/O:** escena virtual con tanques, actuadores e indicadores; comunicación OPC UA con CODESYS.
- **Random Forest:** predicción de humedad y estimación del siguiente riego.
- **MobileNetV2:** clasificación foliar para apoyar la selección entre riego normal y fertirriego; **no constituye un diagnóstico nutricional validado en campo**.

El informe utiliza límites de 60 % para iniciar y 75 % para detener el riego (escala simulada de agua disponible); 1 minuto real representa 1 hora simulada, y el registro periódico se describe cada 10 minutos simulados.

## Organización del repositorio

| Carpeta | Propósito |
|---|---|
| [01_Python](01_Python/) | Simulador ambiental y cliente Modbus |
| [02_CODESYS](02_CODESYS/) | PLC virtual, control e interfaz SCADA |
| [03_Factory_IO](03_Factory_IO/) | Planta virtual y comunicación |
| [04_Random_Forest](04_Random_Forest/) | Regresión y pronóstico de humedad |
| [05_MobileNetV2](05_MobileNetV2/) | Clasificación visual foliar |
| [06_Datos](06_Datos/) | Datos, procedencia y particiones |
| [07_Resultados](07_Resultados/) | Métricas y evidencias |
| [08_Documentacion](08_Documentacion/) | Instrucciones, trazabilidad y comunicaciones |

## Reproducción

Consultar la [guía de instalación y ejecución](08_Documentacion/INSTALACION_Y_EJECUCION.md), **todavía en preparación**. Las versiones de software, librerías, rutas, códigos originales y pasos validados se incorporarán al verificar el entorno de trabajo.

La [tabla de registros Modbus](08_Documentacion/MAPA_MODBUS.md) presenta las direcciones documentadas en el informe, pendientes de contrastar con el programa final.

## Procedencia de los datos y limitaciones

Las bases CoLeaf (hojas de café) y SoursopBD (hojas de guanábana con categorías fitosanitarias) no acreditan automáticamente diagnóstico de deficiencias nutricionales de guanábana. Se documentarán clases originales, reglas de reclasificación, particiones y licencias antes de publicar datos y resultados.

No se deben interpretar las métricas históricas como resultado de una evaluación independiente reproducida hasta publicar sus scripts, datos y configuración.

## Demostración

[Video de funcionamiento](https://youtu.be/djTeff68Glk)

## Licencia

Pendiente de definir. La disponibilidad pública del repositorio no equivale a una licencia que autorice la reutilización de código, imágenes, datasets o componentes de terceros.
