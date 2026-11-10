#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventario local de imagenes sin copiar ni subir el dataset.

Lee las carpetas Sanas/ y Nutrientes/ usadas por ia_imagen.py.
Genera CSV/JSON de metadatos y detecta duplicados identicos por SHA-256.
No modifica imagenes, no reconstruye particiones historicas y no entrena IA.

Uso en Colab (Google Drive ya montado):
  python generar_inventario_imagenes.py --raiz /content/drive/MyDrive/IA \
    --salida /content/drive/MyDrive/IA_documentacion
"""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXTENSIONES = {".jpg", ".jpeg", ".png", ".bmp"}  # Igual a ia_imagen.py
CLASES = {"Sanas": ("Sana", 0), "Nutrientes": ("Deficiencia", 1)}
CAMPOS = [
    "archivo", "fuente", "especie", "clase_original", "clase_final",
    "grupo_original", "particion", "criterio_reclasificacion",
    "licencia_o_referencia", "sha256", "tamano_bytes", "subcarpeta_origen",
]


def hash_archivo(ruta):
    resumen = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


def escribir_csv(ruta, cabeceras, filas):
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=cabeceras)
        writer.writeheader()
        writer.writerows(filas)


def main():
    parser = argparse.ArgumentParser(
        description="Genera un inventario ligero para el dataset de MobileNetV2."
    )
    parser.add_argument(
        "--raiz", type=Path, required=True,
        help="Carpeta IA con Sanas/ y Nutrientes/.",
    )
    parser.add_argument(
        "--salida", type=Path, required=True,
        help="Carpeta donde guardar CSV y resumen (no se suben imagenes).",
    )
    args = parser.parse_args()

    raiz = args.raiz.expanduser().resolve()
    salida = args.salida.expanduser().resolve()
    for clase in CLASES:
        if not (raiz / clase).is_dir():
            parser.error(f"No existe la carpeta requerida: {raiz / clase}")
    if salida in (raiz / "Sanas", raiz / "Nutrientes"):
        parser.error("La carpeta de salida no puede ser Sanas/ o Nutrientes/")

    salida.mkdir(parents=True, exist_ok=True)
    filas = []
    errores = []
    hash_a_archivos = defaultdict(list)
    por_clase = Counter()
    por_subcarpeta = Counter()

    for carpeta, (etiqueta, _) in CLASES.items():
        for ruta in sorted((raiz / carpeta).rglob("*")):
            if not ruta.is_file() or ruta.suffix.lower() not in EXTENSIONES:
                continue
            relativa = ruta.relative_to(raiz).as_posix()
            try:
                huella = hash_archivo(ruta)
                tamano = ruta.stat().st_size
            except OSError as exc:
                errores.append({"archivo": relativa, "error": str(exc)})
                continue

            subcarpeta = ruta.parent.relative_to(raiz).as_posix()
            filas.append({
                "archivo": relativa,
                "fuente": "",
                "especie": "",
                "clase_original": "",
                "clase_final": etiqueta,
                "grupo_original": "",
                "particion": "",
                "criterio_reclasificacion": "",
                "licencia_o_referencia": "",
                "sha256": huella,
                "tamano_bytes": tamano,
                "subcarpeta_origen": subcarpeta,
            })
            por_clase[etiqueta] += 1
            por_subcarpeta[subcarpeta] += 1
            hash_a_archivos[huella].append({"archivo": relativa, "clase": etiqueta})

    duplicados = []
    grupos_duplicados = 0
    grupos_en_clases_distintas = 0
    for sha, elementos in sorted(hash_a_archivos.items()):
        if len(elementos) < 2:
            continue
        grupos_duplicados += 1
        cruzado = len({e["clase"] for e in elementos}) > 1
        grupos_en_clases_distintas += int(cruzado)
        for elemento in elementos:
            duplicados.append({
                "sha256": sha,
                "archivo": elemento["archivo"],
                "clase_final": elemento["clase"],
                "duplicado_entre_clases": cruzado,
            })

    escribir_csv(salida / "inventario_imagenes.csv", CAMPOS, filas)
    escribir_csv(
        salida / "duplicados_exactos.csv",
        ["sha256", "archivo", "clase_final", "duplicado_entre_clases"],
        duplicados,
    )
    escribir_csv(salida / "errores_lectura.csv", ["archivo", "error"], errores)

    resumen = {
        "ruta_raiz_local": str(raiz),
        "total_imagenes_inventariadas": len(filas),
        "conteo_por_clase": dict(por_clase),
        "conteo_por_subcarpeta": dict(sorted(por_subcarpeta.items())),
        "grupos_de_duplicados_exactos": grupos_duplicados,
        "grupos_duplicados_entre_clases": grupos_en_clases_distintas,
        "archivos_con_error_de_lectura": len(errores),
        "observaciones": [
            "No se suben ni copian fotografias.",
            "Fuente, especie, clase original y criterios no pueden inferirse por defecto.",
            "Los duplicados detectados son solo identicos byte a byte.",
            "No se reconstruye el reparto historico entrenamiento/validacion/prueba.",
            "La semilla 42 no garantiza reconstruir particiones sin el orden original.",
        ],
    }
    (salida / "resumen_inventario.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nInventario generado en:", salida)
    print("Total de imagenes:", len(filas))
    print("Por clase:", dict(por_clase))
    print("Grupos de duplicados exactos:", grupos_duplicados)
    print("Duplicados entre clases:", grupos_en_clases_distintas)
    print("Errores:", len(errores))
    print("\nArchivos de salida: inventario_imagenes.csv,")
    print("duplicados_exactos.csv, errores_lectura.csv, resumen_inventario.json")


if __name__ == "__main__":
    main()
