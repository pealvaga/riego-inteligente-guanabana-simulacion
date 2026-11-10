# Instalación y ejecución — borrador pendiente de verificación

> **Importante:** todavía no están incorporados los programas originales, las dependencias ni las versiones verificadas. Esta guía **no** constituye un procedimiento ejecutable validado.

## Entorno de referencia pendiente de completar

| Componente | Versión exacta |
|---|---|
| Windows | Por verificar |
| Python | Por verificar |
| Librerías Python | Generar `requirements.txt` desde entorno funcional |
| CODESYS y controlador virtual | Por verificar |
| Factory I/O | Por verificar |
| Modbus TCP (IP, puerto, unit ID) | Por verificar |
| OPC UA (endpoint y variables) | Por verificar |

## Orden previsto de ejecución

1. Abrir y compilar el proyecto de CODESYS.
2. Iniciar el controlador virtual y configurar las comunicaciones.
3. Abrir la escena Factory I/O y comprobar el vínculo con CODESYS.
4. Ejecutar el simulador Python y comprobar Modbus TCP.
5. Verificar el control por histéresis y el registro histórico.
6. Cargar y comprobar los modelos de IA.

Este orden, los comandos concretos y las rutas deben probarse antes de dar por cerrada la documentación.

## Pruebas pendientes

- Condiciones y parámetros iniciales.
- Inicio, pausa, reinicio y pérdida de conexión.
- Tiempo simulado y frecuencia de registro.
- Ubicación y esquema del historial CSV.
- Scripts, datos, particiones y semillas para entrenamiento/evaluación.
- Resultados esperados y pruebas de reproducibilidad.
