# Datos y trazabilidad

Esta sección organiza los conjuntos de datos asociados a la simulación hídrica y a la clasificación visual foliar.

## Registros de simulación

Cada trayectoria debe conservar su identificador de sesión, origen, condiciones iniciales y variables registradas. Para el pronóstico de humedad se utilizan temperatura, precipitación, humedad disponible y estado de riego, con intervalos de 10 minutos simulados. Es importante distinguir datos de entrenamiento y datos independientes de prueba.

## Bases de imágenes

Fuentes citadas en el documento académico:

- **CoLeaf:** https://doi.org/10.17632/brfgw46wzb.1
- **SoursopBD:** https://doi.org/10.17632/hjrhrt5hs8.2

La trazabilidad requiere registrar especie, clase original, clase agrupada, justificación, cantidad de imágenes originales y su distribución en entrenamiento, validación y prueba.

La división por grupos de imágenes originales debe realizarse antes del aumento de datos. No redistribuir imágenes de terceros sin comprobar su licencia.

## Esquema recomendado de particiones

Para Random Forest: separar trayectorias y mantener el orden temporal. Para MobileNetV2: dividir por imagen original o planta identificada y evitar versiones aumentadas del mismo original en conjuntos diferentes.

Conservar la manifestación de las particiones y sus semillas, para reconstruir exactamente la evaluación que se presente en el documento de grado.
