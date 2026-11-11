# Simulación de un sistema de riego inteligente para cultivos de guanábana

**Actualización más reciente (11/11/2026).** [Random Forest `rf-v2`](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2) está publicado como Release de 53 MB, con [base consolidada, CSV y métricas de prueba](07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md). La última evaluación obtuvo **RMSE 0,114327**, mejor que persistencia **0,172037**, con **4.552 ejemplos de entrenamiento y 922 de prueba**. Los resultados inferiores de versiones anteriores se conservan como *históricos* y no describen el modelo actual. **La huella SHA-256 de la copia local del `.pkl` coincide con la del adjunto de Release.** Queda pendiente verificar su carga e inferencia en Python.


Proyecto de grado de Ingeniería Mecatrónica (Universitaria Agustiniana, 2026) orientado a la simulación de un sistema de riego para guanábana (*Annona muricata* L.) a cielo abierto. Integra un modelo ambiental, control automático, supervisión SCADA y dos componentes de inteligencia artificial.

## Arquitectura del sistema

| Componente | Función |
|---|---|
| **Python** | Simulación ambiental y balance hídrico, interfaz gráfica y comunicación Modbus TCP |
| **CODESYS** | Controlador virtual, control por histéresis, HMI SCADA y registro histórico |
| **Factory I/O** | Escena virtual de tanques, actuadores y señales del proceso; archivo con enlace OPC DA a CODESYS |
| **Random Forest** | Pronóstico de humedad del suelo y estimación del próximo riego |
| **MobileNetV2** | Clasificación visual foliar como apoyo a la elección entre riego normal y fertirriego |

Las condiciones de operación utilizadas en la simulación incluyen umbrales de 60 % (inicio) y 75 % (fin) de agua disponible, así como una escala de tiempo acelerada de **1 minuto real por 1 hora simulada**. Los intervalos de predicción del modelo de humedad son de 10 minutos simulados.

La arquitectura no equivale a una validación agronómica en campo. En particular, las clasificaciones visuales no sustituyen un análisis nutricional del cultivo.

## Contenido

| Ruta | Descripción |
|---|---|
| [01_Python](01_Python/) | Aplicación de simulación, interfaz y comunicación |
| [02_CODESYS](02_CODESYS/) | [Paquete CODESYS](02_CODESYS/Simulaci%C3%B3n%20guanabana%20codesys%20%282%29.zip), controlador, automatización y SCADA |
| [03_Factory_IO](03_Factory_IO/) | [Escena Grado.factoryio](03_Factory_IO/Grado.factoryio) y sus 14 señales OPC DA |
| [04_Random_Forest](04_Random_Forest/) | [Simulador de registro](04_Random_Forest/simulador_guanabana_grado_registro_RF.py), [notebook actual](04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb), [modelo rf-v2 en Releases](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2) y [evaluación nueva](07_Resultados/RF_INFORME_EVALUACION_V2_20261111.md) |
| [05_MobileNetV2](05_MobileNetV2/) | [Script de entrenamiento](05_MobileNetV2/ia_imagen.py), [modelo fine-tuned](05_MobileNetV2/mejor_modelo_hojas_finetuning.keras) y [guía de evaluación](05_MobileNetV2/GUIA_EVALUACION_FINAL.md) |
| [06_Datos](06_Datos/) | Datos, procedencia y particiones |
| [07_Resultados](07_Resultados/) | Resultados, métricas y evidencias |
| [08_Documentacion](08_Documentacion/) | Configuración, reproducibilidad y mapa Modbus |

## Instalación y ejecución

- **[Guía integral de reproducción del sistema](08_Documentacion/GUIA_REPRODUCCION_INTEGRAL.md)**
- **[Lista de verificación de la primera corrección](08_Documentacion/CHECKLIST_PRIMER_PUNTO.md)**
- [Entorno Python registrado: CPython 3.12.9 y versiones de paquetes](08_Documentacion/ENTORNO_PYTHON_REGISTRADO.md)
- [Instantánea completa de Python 3.12.9: 53 paquetes de pip freeze](08_Documentacion/versiones_librerias_python_20261111.txt)
- [Entorno CODESYS registrado: V3.5 SP9 Patch 1 y componentes](08_Documentacion/ENTORNO_CODESYS_REGISTRADO.md)
- [Versiones de Control Win 3.5.9.10, OPCConfig 3.5.9.0 y Factory I/O 2.5.10](08_Documentacion/VERSIONES_SOFTWARE_CONFIRMADAS.md)
- [Texto propuesto para el Anexo C](08_Documentacion/TEXTO_PROPUESTO_ANEXO_C.md)
- [Evidencia de ejecución integrada: Python–CODESYS–Factory I/O](07_Resultados/EVIDENCIA_EJECUCION_INTEGRADA.md)
- [Plantilla de evidencia de pruebas funcionales](07_Resultados/PLANTILLA_EVIDENCIAS_FUNCIONALES.md)
- [Guía del entorno y secuencia de ejecución](08_Documentacion/INSTALACION_Y_EJECUCION.md)
- [Configuración de la aplicación Python](01_Python/README.md)
- [Mapa de registros Modbus TCP](08_Documentacion/MAPA_MODBUS.md)
- [Guía de verificación de resultados](08_Documentacion/ESTADO_REPRODUCIBILIDAD.md)

La ejecución integral requiere los proyectos y modelos correspondientes, además de las herramientas CODESYS y Factory I/O. La escena contiene configuración de **OPC DA** (`CoDeSys.OPC.DA`) para la conexión Factory I/O–CODESYS; Python se comunica con CODESYS mediante **Modbus TCP**. Los nombres y rutas de los modelos utilizados por Python están especificados en su documentación.

## Reentrenamiento desde el registro completo

Para corregir la selección de solo 813 muestras de la base histórica de Random Forest se creó un [cuaderno alternativo que reconstruye los datos desde todas las sesiones](04_Random_Forest/RF_Guanaba_todas_sesiones.ipynb). Actualmente descarga la versión **más reciente del Excel publicada en `06_Datos/` de la rama `main`**, incluso cuando mantiene el mismo nombre. Consulta las [instrucciones para Google Colab](04_Random_Forest/COMO_ENTRENAR_CON_TODAS_LAS_SESIONES.md). El cuaderno nuevo se ejecutó con la base actual y los resultados `rf-v2` están publicados; la identidad SHA-256 ya se comprobó y queda pendiente verificar su compatibilidad funcional en Python.

## Evaluación de MobileNetV2

Para evaluar el modelo fine-tuned sin modificar el entrenamiento existe un [cuaderno independiente de Google Colab](05_MobileNetV2/EVALUAR_MOBILENETV2.ipynb) y una [guía paso a paso](05_MobileNetV2/COMO_EVALUAR_CHECKPOINT_FINAL.md). La evaluación exploratoria del checkpoint ya se ejecutó con 100 fotografías, pero **aún no se acreditó la independencia de los datos ni las etiquetas nutricionales**.

**Primer resultado del checkpoint MobileNetV2:** se dispone de un [informe preliminar de 100 imágenes](07_Resultados/MobileNetV2/INFORME_PRELIMINAR_20261111.md) (accuracy 67 % al umbral 0,50 y 63 % al umbral operativo 0,90). **No es una validación independiente acreditada**, por falta de procedencia y grupos originales de las fotografías. El reporte detalla los falsos negativos y la necesidad de corroborar etiquetas.

**Antecedente histórico de Random Forest:** una ejecución anterior con 3.243 muestras obtuvo RMSE **1,7698** frente a **0,6304** de persistencia y quedó **NO VALIDADA**. Ver el [informe histórico](07_Resultados/RF_INFORME_EVALUACION_BASE_ACTUALIZADA_20261111.md). **El modelo actual es `rf-v2`, evaluado arriba con resultados mejores.**

**Comprobación funcional pendiente de RF `rf-v2`:** el nuevo modelo tiene SHA-256 coincidente con GitHub Release y métricas de prueba superiores a persistencia. El [protocolo de verificación de integración](07_Resultados/PROTOCOLO_VERIFICACION_RF_V2_EN_PYTHON.md) especifica las capturas mínimas para demostrar carga e inferencia en Python, sin modificar ni reentrenar el modelo.

**Lectura del modelo foliar:** la [evaluación preliminar de MobileNetV2](07_Resultados/MobileNetV2/INFORME_PRELIMINAR_20261111.md) clasificó correctamente 50 de 50 hojas etiquetadas como sanas; al umbral conservador del 90 %, identificó 13 de 50 etiquetadas con deficiencia. Las imágenes de deficiencia se localizaron con Google Imágenes, sin diagnóstico nutricional independiente acreditado; se recomienda una base futura de guanábana con deficiencias confirmadas. **El 90 % es un umbral de autorización del fertirriego, no un margen de error estadístico.**

**Estado de publicación:** las **21 capturas E1–E21** ya están en [evidencias_integracion_guanabana/](07_Resultados/evidencias_integracion_guanabana/), incluida la [captura E21 de fecha estimada de próximo riego](07_Resultados/evidencias_integracion_guanabana/21_rf_v2_pronostico_proximo_riego.png). Para conocer las pocas comprobaciones pendientes antes de la entrega, ver el [resumen de cierre del repositorio](08_Documentacion/PENDIENTES_CIERRE_REPOSITORIO.md). No se requiere repetir el entrenamiento ni las pruebas funcionales realizadas para completar la publicación.

## Reproducibilidad y alcance de las IA

La evaluación de Random Forest debe preservar el orden temporal y separar las trayectorias destinadas a entrenamiento, validación y prueba. Sus resultados deben compararse con una referencia de persistencia y acompañarse de un error del momento estimado del próximo riego. **La ejecución histórica del cuaderno antiguo utilizó 813 muestras y no superó persistencia (RMSE 0,6144 frente a 0,1386)**. **La ejecución nueva v2 sí supera persistencia**; aún falta verificar huella y compatibilidad del `.pkl` antes de cargarlo en la aplicación.

Para MobileNetV2, el script de entrenamiento utiliza 70/15/15 y crea sus métricas iniciales con umbral 0,50 antes de la fase fine-tuning. La evaluación del checkpoint final se documenta por separado y debe comprobar la independencia por imagen original y la matriz de confusión con el umbral operativo de **probabilidad de deficiencia ≥ 0,90**.

El [inventario de imágenes](05_MobileNetV2/COMO_GENERAR_INVENTARIO.md) puede generarse desde Google Colab sin subir las fotografías al repositorio. Los datasets de referencia son [CoLeaf](https://doi.org/10.17632/brfgw46wzb.1) y [SoursopBD](https://doi.org/10.17632/hjrhrt5hs8.2). Las etiquetas originales requieren justificación explícita: síntomas fitosanitarios en guanábana o deficiencias en café no son automáticamente equivalentes a una deficiencia nutricional de guanábana.

El [inventario de imágenes verificado](06_Datos/ANALISIS_INVENTARIO_MOBILENETV2.md) contiene 2.247 archivos y detecta 74 pares de duplicados exactos. La trazabilidad de especies, fuentes y particiones todavía debe establecerse para determinar la independencia de las pruebas.

Las cifras de desempeño deben leerse junto con el conjunto de prueba, el script de evaluación y la configuración que las generó.

## Acceso a las imágenes de entrenamiento

La base de imágenes de MobileNetV2 se mantiene fuera del repositorio por su tamaño. La ubicación de los datos se documenta mediante el [enlace a la carpeta IA en Google Drive](https://drive.google.com/drive/folders/1dSFK86hFvjr4cZiNZvvqDZDGeydOIcys?usp=sharing). Consultar el [README de MobileNetV2](05_MobileNetV2/README.md) para la estructura, el inventario y las condiciones de trazabilidad. El acceso público y los derechos de redistribución deben comprobarse antes de utilizar o compartir fotografías de terceros.

## Demostración

[Video de funcionamiento del sistema](https://youtu.be/djTeff68Glk)

## Autoría y uso

Trabajo académico de elaboración propia. El código, los modelos, las escenas y los datos externos pueden tener condiciones de uso diferentes; consultar las licencias respectivas antes de redistribuir componentes de terceros. La publicación en GitHub no otorga por sí sola una licencia de reutilización.
