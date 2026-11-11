# Verificación de librerías de Python mediante PowerShell — 11/11/2026

## Procedencia y alcance

Se recibió la salida de una sesión **Windows PowerShell 5.1** con los comandos `python --version`, `python -m pip --version` y `python -m pip show numpy pandas scikit-learn joblib pymodbus tensorflow keras pillow matplotlib openpyxl`. Se transcriben únicamente las versiones técnicas, **sin publicar el log íntegro, rutas personales ni textos extensos de licencias**.

La salida confirma que los paquetes enumerados están presentes en el Python global consultado, pero **no prueba por sí sola** que el archivo `Sensores.py` se haya ejecutado exactamente con ese intérprete ni que los modelos se hayan cargado en esta sesión de PowerShell.

## Versiones constatadas en la consulta

| Componente | Versión |
|---|---|
| Sistema de comandos | Windows PowerShell 5.1 |
| Python | **3.12.9** |
| pip | **24.3.1** |
| numpy | **2.5.3** |
| pandas | **3.0.5** |
| scikit-learn | **1.6.1** |
| joblib | **1.6.0** |
| pymodbus | **3.15.0** |
| tensorflow | **2.21.0** |
| keras | **3.15.1** |
| Pillow | **12.3.0** |
| matplotlib | **3.11.2** |
| openpyxl | **3.1.5** |

Estas versiones **coinciden con la instantánea publicada previamente** en [`ENTORNO_EJECUTADO.json`](ENTORNO_EJECUTADO.json) y el archivo de versiones directas [`requirements_entorno_reportado.txt`](requirements_entorno_reportado.txt). Este registro constituye una segunda comprobación documental de las versiones, **no un resultado de pruebas nuevas de las IA**.

## Incidencia al exportar `pip freeze`

El comando `python -m pip freeze > versiones_librerias_python.txt` se lanzó desde una carpeta protegida del sistema operativo y PowerShell devolvió **UnauthorizedAccessException / Acceso denegado** al escribir allí. **No es un error de instalación ni del cálculo de versiones**.

Para obtener la lista completa en una ruta de usuario, ejecutar:

```powershell
python -m pip freeze | Set-Content -Path "$env:USERPROFILE\versiones_librerias_python.txt" -Encoding UTF8
```

El archivo completo `pip freeze` **todavía no se ha recibido**. El resumen de paquetes directos sí está registrado; **no debe presentarse como bloqueo completo de todas las dependencias transitivas**.

Para relacionar este entorno con la ejecución efectiva, obtener `python -c "import sys; print(sys.executable)"` desde el mismo terminal con el que se abre la aplicación y confirmar que se trata de este intérprete. Si la aplicación se lanza con un entorno virtual o Python distinto, repetir allí el registro.

## Confirmación posterior del comando de exportación

Se aportó una segunda salida de PowerShell en la que el comando:

```powershell
python -m pip freeze | Set-Content -Path "$env:USERPROFILE\versiones_librerias_python.txt" -Encoding UTF8
```

terminó **sin mensajes de error**. Por ello, la exportación del inventario completo a la carpeta del usuario **parece haberse realizado correctamente**; todavía **no se ha recibido ni verificado el contenido del archivo generado**. Se confirmó además que `sys.executable` señala a la instalación normal de **Python 3.12** bajo `AppData/Local/Programs/Python/Python312/python.exe`. No se publica la ruta personal completa. Para acreditar que es el intérprete efectivo de la aplicación, falta comprobar cómo se lanza `Sensores.py`.

## Estado

- **Completado:** comprobación de Python, pip y diez librerías principales instaladas, con versiones coincidentes con la instantánea anterior.
- **Por completar (recomendado):** adjuntar y revisar el archivo `pip freeze` ya generado sin errores aparentes, y comprobar que la aplicación ejecuta el intérprete identificado en PowerShell.
- **Sin cambios** en las versiones instaladas, el código de Python ni los archivos `.pkl`/`.keras`.
