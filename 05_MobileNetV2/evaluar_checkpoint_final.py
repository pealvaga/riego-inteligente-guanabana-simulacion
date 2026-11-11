#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Evaluacion del checkpoint MobileNetV2 sobre imagenes de prueba no entrenadas.

Lee: CARPETA_PRUEBA/Sanas/** y CARPETA_PRUEBA/Nutrientes/**.
0 = Sana; 1 = Deficiencia (etiquetado binario del proyecto).
No reentrena, no edita imagenes ni modifica el modelo original.

Ejemplo:
 python evaluar_checkpoint_final.py \
   --prueba /content/drive/MyDrive/IA_prueba_independiente \
   --modelo /content/mejor_modelo_hojas_finetuning.keras \
   --salida /content/drive/MyDrive/IA_evaluacion_final \
   --inventario-entrenamiento /content/drive/MyDrive/IA_documentacion/inventario_imagenes.csv
"""
import argparse
import csv
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score
)

EXTENSIONES = {".jpg", ".jpeg", ".png", ".bmp"}
CLASES = {"Sanas": 0, "Nutrientes": 1}
COLUMNAS_MANIFIESTO = [
    "archivo", "fuente", "especie", "clase_original",
    "grupo_original", "criterio_reclasificacion", "licencia_o_referencia"
]


def sha256(ruta):
    h = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def recopilar(prueba):
    registros = []
    for carpeta, etiqueta in CLASES.items():
        origen = prueba / carpeta
        if not origen.is_dir():
            raise FileNotFoundError(
                f"Falta {origen}. Deben existir Sanas/ y Nutrientes/ "
                "con imagenes que NO se hayan utilizado para entrenar."
            )
        for ruta in sorted(origen.rglob("*"), key=lambda p: p.as_posix().lower()):
            if not ruta.is_file() or ruta.suffix.lower() not in EXTENSIONES:
                continue
            registros.append({
                "archivo": ruta.relative_to(prueba).as_posix(),
                "ruta": str(ruta),
                "etiqueta_real": etiqueta,
                "clase_real": "Sana" if etiqueta == 0 else "Deficiencia",
                "sha256": sha256(ruta),
            })
    if not registros:
        raise ValueError("Carpeta de prueba vacia.")
    df = pd.DataFrame(registros)
    if df["etiqueta_real"].nunique() < 2:
        raise ValueError("Se necesitan ejemplos de ambas clases en la prueba.")
    return df


def completar_manifiesto(df, prueba):
    ruta = prueba / "manifest_prueba.csv"
    for columna in COLUMNAS_MANIFIESTO[1:]:
        df[columna] = ""
    if ruta.exists():
        m = pd.read_csv(
            ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig"
        )
        if "archivo" not in m.columns:
            raise ValueError("manifest_prueba.csv requiere columna archivo.")
        m["archivo"] = m["archivo"].str.replace("\\", "/", regex=False)
        if m["archivo"].duplicated().any():
            raise ValueError("manifest_prueba.csv contiene archivos duplicados.")
        m = m.set_index("archivo")
        for col in COLUMNAS_MANIFIESTO[1:]:
            if col in m.columns:
                df[col] = df["archivo"].map(m[col]).fillna("")
    return df


def muestras_por_lote(rutas, tamano=16):
    for i in range(0, len(rutas), tamano):
        bloque = []
        for path in rutas[i:i+tamano]:
            datos = tf.io.read_file(str(path))
            img = tf.io.decode_image(
                datos, channels=3, expand_animations=False
            )
            img.set_shape([None, None, 3])
            img = tf.image.resize(img, [224, 224])
            bloque.append(tf.cast(img, tf.float32).numpy())
        yield np.stack(bloque, axis=0)


def guardar_matriz(y, y_pred, umbral, salida):
    c = confusion_matrix(y, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.8, 5.0))
    im = ax.imshow(c, cmap="Blues")
    ax.set_xticks([0, 1], ["Sana", "Deficiencia"])
    ax.set_yticks([0, 1], ["Sana", "Deficiencia"])
    ax.set_xlabel("Prediccion")
    ax.set_ylabel("Clase real")
    ax.set_title(f"Checkpoint MobileNetV2 - umbral {umbral:.2f}")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(int(c[i, j])), ha="center", va="center",
                    color="white" if c[i, j] > c.max() / 2 else "black",
                    fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.045)
    fig.tight_layout()
    destino = salida / f"matriz_confusion_{str(umbral).replace('.', '')}.png"
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prueba", type=Path, required=True)
    parser.add_argument("--modelo", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--inventario-entrenamiento", type=Path, default=None)
    parser.add_argument(
        "--confirma-no-usadas", action="store_true",
        help="Declaracion: las imagenes del test no se usaron en train/val."
    )
    args = parser.parse_args()
    prueba = args.prueba.expanduser().resolve()
    salida = args.salida.expanduser().resolve()
    modelo = args.modelo.expanduser().resolve()

    if not modelo.is_file():
        raise FileNotFoundError(f"No existe el .keras: {modelo}")
    if not prueba.is_dir():
        raise FileNotFoundError(
            f"No existe {prueba}; crea Sanas/ y Nutrientes/ con "
            "imagenes independientes NUEVAS, no copiadas del entrenamiento."
        )
    if salida == prueba or prueba in salida.parents:
        raise ValueError("La salida debe quedar FUERA de la carpeta de prueba.")
    salida.mkdir(parents=True, exist_ok=True)

    df = recopilar(prueba)
    df = completar_manifiesto(df, prueba)
    hashes_test = df[df["sha256"].duplicated(keep=False)].copy()
    hashes_test.to_csv(salida / "duplicados_en_prueba.csv", index=False,
                       encoding="utf-8-sig")

    sha_entrenamiento = set()
    inventario_disponible = False
    if args.inventario_entrenamiento is not None:
        indice = args.inventario_entrenamiento.expanduser().resolve()
        if indice.is_file():
            m = pd.read_csv(indice, usecols=["sha256"], dtype=str)
            sha_entrenamiento = set(m["sha256"].dropna().str.lower())
            inventario_disponible = bool(sha_entrenamiento)
        else:
            print("AVISO: no se encontro inventario de entrenamiento:", indice)

    df["coincide_hash_entrenamiento"] = (
        df["sha256"].str.lower().isin(sha_entrenamiento)
    )
    solapes = df[df["coincide_hash_entrenamiento"]].copy()
    solapes.to_csv(salida / "solapes_con_entrenamiento.csv", index=False,
                  encoding="utf-8-sig")

    if not args.confirma_no_usadas:
        print("AVISO: no se ha declarado independencia del conjunto de prueba.")
    if not inventario_disponible:
        print("AVISO: no se pudo contrastar SHA-256 con el inventario de entrenamiento.")
    if len(hashes_test):
        print("AVISO: hay imagenes exactamente repetidas dentro de la prueba:", len(hashes_test))
    if len(solapes):
        print("AVISO: hay imagenes IDENTICAS a las usadas en el conjunto original:", len(solapes))

    print("Cargando checkpoint final sin reentrenar:", modelo.name)
    red = tf.keras.models.load_model(str(modelo), compile=False)
    if red.output_shape[-1] != 1:
        raise ValueError("Se esperaba una salida sigmoide de dimension 1.")

    probabilidades = []
    for lote in muestras_por_lote(df["ruta"].tolist()):
        result = np.asarray(red.predict(lote, verbose=0)).reshape(-1)
        probabilidades.extend(result.tolist())
    probs = np.asarray(probabilidades, dtype=float)
    if len(probs) != len(df) or not np.isfinite(probs).all():
        raise ValueError("No se obtuvieron probabilidades validas para todas las imagenes.")
    if (probs < 0).any() or (probs > 1).any():
        raise ValueError("La salida del modelo no esta en escala [0, 1].")

    df["probabilidad_deficiencia"] = probs
    y_true = df["etiqueta_real"].to_numpy(dtype=int)
    detalle = {}
    filas_metricas = []
    for umbral in [0.50, 0.90]:
        clave = f"{umbral:.2f}"
        pred = (probs >= umbral).astype(int)
        df[f"prediccion_{clave}"] = pred
        df[f"acierto_{clave}"] = pred == y_true
        matriz = guardar_matriz(y_true, pred, umbral, salida)
        report = classification_report(
            y_true, pred, labels=[0, 1],
            target_names=["Sana", "Deficiencia"],
            zero_division=0, output_dict=True
        )
        info = {
            "umbral": umbral, "n": len(df),
            "accuracy": float(accuracy_score(y_true, pred)),
            "precision_deficiencia": float(precision_score(y_true, pred, zero_division=0)),
            "recall_deficiencia": float(recall_score(y_true, pred, zero_division=0)),
            "f1_deficiencia": float(f1_score(y_true, pred, zero_division=0)),
            "matriz": matriz.astype(int).tolist(),
            "reporte_por_clase": report,
        }
        detalle[clave] = info
        filas_metricas.append({
            k: v for k, v in info.items()
            if k not in ("matriz", "reporte_por_clase")
        })
        print(
            f"Umbral {clave}: accuracy={info['accuracy']:.4f}, "
            f"precision={info['precision_deficiencia']:.4f}, "
            f"recall={info['recall_deficiencia']:.4f}, "
            f"F1={info['f1_deficiencia']:.4f}"
        )

    df["particion"] = "prueba_independiente_declarada"
    df = df.drop(columns=["ruta"])
    df.to_csv(salida / "predicciones_mobilenetv2.csv", index=False,
              encoding="utf-8-sig")
    pd.DataFrame(filas_metricas).to_csv(
        salida / "metricas_resumen.csv", index=False, encoding="utf-8-sig"
    )

    por_fuente = []
    for fuente, grp in df[df["fuente"].ne("")].groupby("fuente"):
        for umbral in [0.50, 0.90]:
            y_grp = grp["etiqueta_real"].to_numpy(dtype=int)
            p_grp = grp[f"prediccion_{umbral:.2f}"].to_numpy(dtype=int)
            por_fuente.append({
                "fuente": fuente, "umbral": umbral, "imagenes": len(grp),
                "accuracy": float(accuracy_score(y_grp, p_grp))
            })
    pd.DataFrame(por_fuente, columns=[
        "fuente", "umbral", "imagenes", "accuracy"
    ]).to_csv(salida / "resultados_por_fuente.csv", index=False,
              encoding="utf-8-sig")

    verificacion = {
        "declarado_no_usadas_entrenamiento_validacion": bool(args.confirma_no_usadas),
        "inventario_entrenamiento_disponible": inventario_disponible,
        "duplicados_exactos_en_prueba": int(len(hashes_test)),
        "solapes_hash_con_entrenamiento": int(len(solapes)),
        "imagenes_con_fuente": int(df["fuente"].ne("").sum()),
        "imagenes_con_especie": int(df["especie"].ne("").sum()),
        "imagenes_con_clase_original": int(df["clase_original"].ne("").sum()),
        "imagenes_con_grupo_original": int(df["grupo_original"].ne("").sum()),
        "nota": (
            "SHA-256 solo detecta copias exactas. Un hash distinto NO prueba "
            "que no existan recortes, aumentos, hojas o plantas compartidas."
        ),
    }
    apto = (
        args.confirma_no_usadas and inventario_disponible
        and len(hashes_test) == 0 and len(solapes) == 0
    )
    estado = (
        "PRUEBA_INDEPENDIENTE_DECLARADA_CON_COMPROBACION_SHA_EXACTA"
        if apto else "EVALUACION_PRELIMINAR_INDEPENDENCIA_NO_ACREDITADA"
    )
    completo_manifest = all(
        df[col].ne("").all()
        for col in ("fuente", "especie", "clase_original", "grupo_original")
    )
    informe = {
        "estado": estado,
        "nota_estado": (
            "La independencia por imagen original/planta y el diagnostico "
            "real requieren evidencia de procedencia; la declaracion y SHA "
            "no bastan para certificar independencia semantica."
        ),
        "manifest_de_origen_completo": bool(completo_manifest),
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "modelo_archivo": modelo.name,
        "modelo_sha256": sha256(modelo),
        "n_prueba": int(len(df)),
        "distribucion": {
            "sana": int((y_true == 0).sum()),
            "deficiencia": int((y_true == 1).sum()),
        },
        "definiciones": {
            "clase_0": "Sana", "clase_1": "Deficiencia",
            "umbral_clasificacion": 0.50,
            "umbral_fertirriego": 0.90,
            "entrada": "RGB 224x224 float32 en 0..255; preprocesamiento interno",
        },
        "verificacion": verificacion,
        "versiones": {
            "python": sys.version.split()[0],
            "tensorflow": tf.__version__,
            "sklearn": sklearn.__version__,
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
        "resultados": detalle,
        "limitacion_agronomica": (
            "La etiqueta binaria Deficiencia agrupa fuentes heterogeneas "
            "y no acredita por si sola deficiencia nutricional de guanabana."
        )
    }
    (salida / "metricas_mobilenetv2.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    zippath = salida / "evaluacion_mobilenetv2_checkpoint.zip"
    with zipfile.ZipFile(zippath, "w", compression=zipfile.ZIP_DEFLATED) as paquete:
        for ruta in sorted(salida.iterdir()):
            if ruta.is_file() and ruta != zippath:
                paquete.write(ruta, arcname=ruta.name)

    print("\nEstado:", estado)
    print("Imagenes evaluadas:", len(df), "| Sana:",
          int((y_true == 0).sum()), "| Deficiencia:", int((y_true == 1).sum()))
    print("Archivos guardados en:", salida)
    print("ZIP para GitHub:", zippath)
    if not apto:
        print("ATENCION: NO presentar estas metricas como prueba independiente definitiva.")


if __name__ == "__main__":
    main()
