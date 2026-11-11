# Versiones confirmadas del entorno de simulación

Registro a partir de capturas de las ventanas de información de software capturadas durante el desarrollo del proyecto (10/11/2026, hora local de Colombia). Se documentan las versiones **instaladas/mostradas**; no constituye una prueba de compilación, ejecución o comunicación.

| Componente | Versión observada | Evidencia |
|---|---|---|
| CODESYS IDE | **V3.5 SP9 Patch 1** | Captura previa de «Acerca de» e «Información de versión» |
| CODESYS Control Win V3 | **3.5.9.10** | Pantalla de inicio del runtime «CODESYS Control Win V3 Version 3.5.9.10» |
| OPCConfig | **3.5.9.0** | Cuadro «Info about OPCConfig» |
| Factory I/O | **2.5.10** | Pantalla «Update Checker»: «Currently installed version is v2.5.10» |
| Python | **CPython 3.12.9** | [Captura de dependencias](ENTORNO_EJECUTADO.json) |
| Device Modbus TCP Slave (componente IDE) | **3.5.9.10** | Captura previa del catálogo de componentes de CODESYS |

## Comprobaciones de correspondencia

- **CODESYS:** el runtime anunciado como `Control Win V3 3.5.9.10` y el IDE `V3.5 SP9 Patch 1` se alinean con las versiones 3.5.9.0/3.5.9.10 que figuran en el paquete publicado `02_CODESYS/Codesys.zip`. No se ha comprobado que `Grado.project` compile y entre en RUN sin errores.
- **Factory I/O:** la aplicación declara versión 2.5.10, la misma que aparece en los metadatos de `03_Factory_IO/Grado.factoryio`.
- **OPCConfig:** la herramienta de configuración es 3.5.9.0. **No equivale a una comprobación de versión del servidor `CoDeSys.OPC.DA` ni a una conexión OPC DA activa**.
- **Python:** las dependencias registradas en la captura están instaladas, pero queda confirmar que se trate del intérprete con el que se ejecuta realmente `01_Python/Sensores.py`.

## Pruebas pendientes

1. Abrir y compilar `Grado.project` sin errores; registrar dependencias de bibliotecas y comprobar Control Win en estado **RUN**.
2. Probar la conexión **Python → CODESYS (Modbus TCP)**, verificando HR0–HR7 e IR0 con datos cambiantes.
3. Probar la conexión **Factory I/O ↔ CODESYS (OPC DA)**, verificando el servidor `CoDeSys.OPC.DA` y las 14 señales `PLC1.Application.GVL.FO_*`.
4. Capturar una ejecución completa con SCADA, riego, niveles de tanques y registro del histórico.
5. Verificar carga y compatibilidad efectiva del modelo de imágenes y, cuando exista validación, el `.pkl` final de Random Forest.

## Tratamiento de evidencias

Los valores transcritos proceden de las capturas de las ventanas de información de cada programa. **Aún no se han guardado los PNG en el repositorio**. Para conservar evidencias visuales de entrega se pueden subir los tres PNG a `07_Resultados/evidencias_versiones/` con nombres descriptivos y referencias a este archivo.

La [lista de verificación del primer punto](CHECKLIST_PRIMER_PUNTO.md) distingue los componentes documentados de las pruebas funcionales todavía por realizar.
