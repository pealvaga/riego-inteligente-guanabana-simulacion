# Proyecto CODESYS: controlador virtual y SCADA

El archivo [Codesys.zip](Codesys.zip) reúne el material de CODESYS aportado para el sistema de riego inteligente de guanábana.

## Función en el sistema

De acuerdo con el documento de grado, CODESYS desempeña las funciones de control automático por histéresis, intercambio de señales con la aplicación Python mediante Modbus TCP, visualización SCADA/HMI, vinculación con Factory I/O y registro de la operación.

El controlador utiliza los límites operativos de **60 %** y **75 %** de agua disponible, expresados en la escala de simulación. El estado del riego se devuelve a Python para actualizar el balance hídrico.

## Archivo del proyecto

| Recurso | Ruta | Descripción |
|---|---|---|
| Archivo comprimido CODESYS | `02_CODESYS/Codesys.zip` | Paquete facilitado por el autor para conservar los recursos del proyecto |

Para reproducir el entorno, descargar y extraer el ZIP. Abrir el archivo de proyecto correspondiente desde CODESYS y comprobar los dispositivos y bibliotecas instaladas.

## Integración y comprobaciones

- **Modbus TCP:** revisar el servidor CODESYS y las direcciones HR0–HR7/IR0 descritas en el [mapa de comunicación](../08_Documentacion/MAPA_MODBUS.md). La existencia de esos registros está confirmada en el código Python; su correspondencia con el PLC requiere comprobar el proyecto abierto en CODESYS.
- **Control:** contrastar el comportamiento de histéresis, mandos de inicio/parada y estado de las señales.
- **Supervisión:** comprobar la interfaz de niveles de tanques, humedad, temperatura, precipitación, estado del riego y reloj simulado.
- **Histórico:** el trabajo escrito describe un registro `HistorialCultivo.csv` mediante la biblioteca CAA File a intervalos de diez minutos simulados. La ruta, el formato y el funcionamiento deben verificarse con el programa incluido en el ZIP.
- **Factory I/O:** comprobar los símbolos y el enlace OPC UA con la escena virtual.

## Recomendación para reproducción

Conservar dentro del paquete exportable o en el repositorio el proyecto fuente, las versiones exactas de CODESYS y sus bibliotecas, las configuraciones de comunicación y una captura del árbol de dispositivos. Esta documentación ayuda a reconstruir el entorno en un equipo diferente.
