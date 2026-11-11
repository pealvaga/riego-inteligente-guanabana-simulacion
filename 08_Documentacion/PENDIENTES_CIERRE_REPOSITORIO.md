# Cierre del repositorio — estado verificado el 11/11/2026

Este documento identifica **qué ya está publicado en GitHub** y separa los controles de reproducibilidad técnica de las futuras validaciones metodológicas. Su objetivo es evitar repetir pruebas funcionales que ya se realizaron y no confundir la existencia de un archivo con una validación externa.

## Publicación completada

- Código Python de la simulación y comunicación Modbus TCP: `01_Python/Sensores.py`.
- Proyecto CODESYS comprimido: `02_CODESYS/Codesys.zip`, con `Grado.project`.
- Escena Factory I/O: `03_Factory_IO/Grado.factoryio` y enlaces OPC DA documentados.
- Modelo Random Forest `rf-v2`: [GitHub Release](https://github.com/pealvaga/riego-inteligente-guanabana-simulacion/releases/tag/rf-v2) con `modelo_prediccion_humedad.pkl` (53.111.758 bytes). SHA-256 de la copia local **idéntico** al anunciado por GitHub: `c3eba2fce1d49187249afef988d0848276eb4dd2e9e5f5e2bf33fa8446e09692`.
- Base original RF, base consolidada, cuaderno de Colab, CSV de **922 predicciones**, JSON de métricas y trazabilidad de origen. RMSE RF **0,114327** vs. persistencia **0,172037**, mejora de RMSE **33,55 %** en cuatro escenarios de prueba.
- Comparación operativa adicional de **21 pronósticos a +10 minutos simulados**: MAE **0,00429** y RMSE **0,00655** puntos porcentuales, con valores redondeados a dos decimales y en rango de humedad limitado.
- Modelo MobileNetV2 `.keras`, entrenamiento, herramientas de evaluación y **resultados preliminares** sobre 100 capturas seleccionadas como hojas de guanábana: **50/50** sanas reconocidas, **13/50** imágenes etiquetadas con deficiencia identificadas a umbral **0,90**. La procedencia de las fotos deficientes se declaró como Google Imágenes; las etiquetas nutricionales no fueron verificadas. El umbral 90 % es una condición de **autorización conservadora de fertirriego**, no un margen de error medido.
- **21 capturas PNG originales E1–E21** en [evidencias_integracion_guanabana/](../07_Resultados/evidencias_integracion_guanabana/). E21 muestra la aplicación operativa con humedad 69,61 %, pronóstico a +10 min 69,60 %, riego inactivo y estimación de próximo riego **Día 3 a las 23:30**. La imagen E21 publicada es idéntica a la original aportada (blob Git SHA-1 `1fc80448fbe235d34fd23dbf732926883e8efc86`). Su [informe](../07_Resultados/RF_EVIDENCIA_ESTIMACION_PROXIMO_RIEGO_20261111.md) distingue el pronóstico del evento real.
- Guías de instalación y ejecución, mapa Modbus, versiones declaradas, informes técnicos, README principal y lista de verificación.

## Controles prioritarios antes de declarar el repositorio listo para entrega

| Prioridad | Comprobación | Estado |
|---|---|---|
| **Alta** | Confirmar que el `Grado.project` de `Codesys.zip` es **la misma revisión final guardada** que se compiló y ejecutó; la captura anterior tenía `Grado.project*`, que puede indicar cambios sin guardar. Reemplazar ZIP solo si hubo cambios reales. | **Pendiente de confirmación** |
| **Alta** | Registrar las **versiones de dependencias del entorno de Python que ejecuta la simulación** (especialmente `scikit-learn`, `joblib`, `pymodbus`, `tensorflow`) y, si es posible, demostrar el arranque siguiendo la guía desde una copia limpia. | **Parcial** |
| **Media** | Confirmar que la captura de la aplicación mostrando `MODELO NUEVO CARGADO` corresponde específicamente al archivo `rf-v2` publicado, no a un `.pkl` anterior con el mismo nombre; el SHA-256 de la copia local sí está confirmado. | **Parcial** |
| **Media** | Revisar que README, guía integral y Anexo C **en el documento de grado** apunten a la carpeta E1–E21, a `rf-v2` y a los resultados actuales. El texto propuesto del anexo ya está en GitHub; su incorporación al documento es una tarea externa al repositorio. | **Parcial** |
| **Cierre** | Crear una **etiqueta de entrega o Release del proyecto completo** apuntando a un commit definitivo de `main`, tras los controles anteriores, para que el docente revise una versión estable. No modificar resultados después sin registrar el cambio. | **Opcional recomendable** |

## Validaciones adicionales que NO bloquean publicar el código y los archivos, pero sí limitan las conclusiones científicas

- **Próximo riego:** ya se comprobó que la interfaz puede mostrar fecha prevista (E21), pero **no se midió el error del instante estimado** frente al riego realmente activado por CODESYS. Mantener esta limitación en el trabajo.
- **Random Forest:** la evaluación de 922 muestras utilizó cuatro escenarios reservados de una misma sesión. Para afirmar generalización a otras condiciones conviene evaluar **otra sesión independiente** no empleada para ajustar el bosque.
- **MobileNetV2:** no se acreditó independencia completa de las fotos ni el diagnóstico nutricional real de cada captura. Conservar las métricas preliminares y presentar como **recomendación de trabajo futuro** una base de hojas de guanábana con deficiencias nutricionales verificadas.
- **START/STOP/OPC:** se reportaron **múltiples pruebas funcionales satisfactorias**. E1–E20 muestran diversos estados y cambios de emergencia, pero no todos los cambios están capturados en una única secuencia sincronizada. La carencia es **de evidencia detallada**, no prueba de un funcionamiento defectuoso. No exigir repetir todas las maniobras sin una razón concreta.
- **Histórico CODESYS:** si se afirma que `HistorialCultivo.csv` fue exportado como resultado reproducible, conviene publicar una muestra real o especificar dónde encontrarlo; no inventar un archivo que no se ha verificado.

## Criterio práctico de cierre

**Para la publicación del trabajo de grado**, los componentes y las 21 evidencias están disponibles. Priorizar **CODESYS final guardado**, **entorno Python reproducible** y **coherencia con el documento entregado**. No hace falta reentrenar Random Forest, recopilar cientos de fotografías nuevas ni repetir todas las pruebas de control para cerrar la *publicación* del repositorio. Los límites de validación deben conservarse transparentemente en las conclusiones del trabajo.
