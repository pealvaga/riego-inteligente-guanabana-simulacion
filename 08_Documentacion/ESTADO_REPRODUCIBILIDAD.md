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

Mantener la separación por sesiones, respetar el orden temporal y asegurar que no se filtren observaciones futuras entre conjuntos. Comparar las predicciones con persistencia y evaluar el error del próximo momento de riego además del RMSE de humedad.

## Reproducción de MobileNetV2

Documentar procedencia y etiquetas, separar imágenes originales y versiones aumentadas, y reportar la matriz de confusión bajo el umbral operativo de 0,90 de probabilidad de deficiencia.

## Correspondencia académica

La documentación técnica debe acompañarse de evidencias de ejecución, configuración y resultados medidos con los mismos artefactos publicados. La comprobación de componentes a partir de archivos **no equivale** a una prueba funcional realizada en CODESYS/Factory I/O.

### Aspectos que requieren conciliación en el documento escrito

- La escena entregada configura `OPCClientDA` (`CoDeSys.OPC.DA`), mientras que el informe escrito describe el enlace con Factory I/O como OPC UA. Debe verificarse el protocolo utilizado en la ejecución final y corregirse el informe o la configuración para que coincidan.

- El proyecto de CODESYS incluye comparaciones estrictas `< 60` y `> 75`; el trabajo escrito utiliza límites inclusivos.
- La Tabla 1 del trabajo describe HR0–HR4 e IR0, mientras que Python utiliza HR0–HR7 para incluir día, hora y minuto.
- El CSV registra `RiegoActivo` a partir de `GVL.Riego`, mientras que Python lee un registro construido desde `GVL.Regando`: verificar que ambas variables representen efectivamente el mismo estado.
- El CSV no incluye identificador de sesión; documentar los cambios de trayectoria al preparar los datos para evaluación temporal independiente.
