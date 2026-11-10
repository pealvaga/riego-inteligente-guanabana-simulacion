# Generación del inventario de imágenes sin subir el dataset

Este procedimiento trabaja **sobre la misma carpeta de Google Drive** empleada por `ia_imagen.py` y produce archivos CSV/JSON pequeños. No copia, modifica ni publica las fotografías y no vuelve a entrenar el modelo.

## 1. Abrir Google Colab y montar Drive

```python
from google.colab import drive
drive.mount("/content/drive")
```

La carpeta de datos del código original es `/content/drive/MyDrive/IA`. Debe contener `Sanas/` y `Nutrientes/` con sus subcarpetas.

## 2. Descargar el script desde el repositorio

Ejecutar en una nueva celda de Colab:

```python
!wget -q -O /content/generar_inventario_imagenes.py "https://raw.githubusercontent.com/pealvaga/riego-inteligente-guanabana-simulacion/main/05_MobileNetV2/generar_inventario_imagenes.py"
```

## 3. Generar inventario

```python
!python /content/generar_inventario_imagenes.py --raiz "/content/drive/MyDrive/IA" --salida "/content/drive/MyDrive/IA_documentacion"
```

El script lee `*.jpg`, `*.jpeg`, `*.png` y `*.bmp` de `Sanas/` y `Nutrientes/`, siguiendo las extensiones del entrenamiento.

Se generan estos recursos en `MyDrive/IA_documentacion/`:

| Archivo | Contenido |
|---|---|
| `inventario_imagenes.csv` | Ruta relativa, clase final, subcarpeta, tamaño, SHA-256 y campos por completar |
| `resumen_inventario.json` | Cantidades por clase y subcarpeta, duplicados y errores |
| `duplicados_exactos.csv` | Archivos con contenido idéntico (SHA-256) |
| `errores_lectura.csv` | Archivos que no se pudieron leer |

No genera una copia de las imágenes.

## 4. Revisar y completar la trazabilidad

Los campos `fuente`, `especie`, `clase_original`, `grupo_original`, `particion`, `criterio_reclasificacion` y `licencia_o_referencia` quedan **vacíos por diseño**, porque no pueden determinarse con certeza a partir de las carpetas binarias `Sanas` / `Nutrientes`.

- Documentar qué imágenes proceden de CoLeaf y cuáles de SoursopBD.
- Conservar la clase original (plaga, enfermedad, deficiencia, etc.) cuando exista.
- Revisar posibles variantes aumentadas y capturas de una misma planta: la coincidencia de SHA-256 **solo encuentra duplicados exactos**.
- No asumir que la semilla `random_state=42` reproduce la partición original; también debe conservarse el orden de entrada. Para el conjunto de prueba del modelo final hay que demostrar independencia de entrenamiento y validación.

## 5. Incorporar evidencia ligera a GitHub

Después de revisar rutas y metadatos, publicar en `06_Datos/` los archivos de inventario, resumen y, cuando proceda, particiones verificadas, sin incluir todas las fotografías. Se puede conservar la carpeta de imágenes en Drive y proporcionar a los revisores autorizados acceso de solo lectura, **si las licencias de los datasets lo permiten**. Otra alternativa es documentar los enlaces oficiales de descarga y los pasos de reconstrucción.

Para evaluación independiente de MobileNetV2, utilizar la [guía del checkpoint final](GUIA_EVALUACION_FINAL.md). Las estadísticas generadas aquí son de inventario, **no métricas de clasificación**.

> Antes de publicar los CSV, revisar que las rutas y nombres de archivo no incluyan datos privados o información que no deba difundirse.
