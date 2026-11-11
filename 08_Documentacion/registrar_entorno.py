#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registra versiones del entorno Python sin instalar dependencias ni abrir modelos.

Ejemplo (desde la raiz del repositorio):
    python 08_Documentacion/registrar_entorno.py --salida 08_Documentacion/ENTORNO_EJECUTADO.json

Solo registra version de Python, plataforma basica y versiones de paquetes.
No recoge rutas personales, nombres de usuario, IP, variables de entorno ni claves.
"""
import argparse
import importlib.metadata as metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGES = [
    "numpy", "pandas", "Pillow", "pymodbus", "joblib",
    "scikit-learn", "tensorflow", "openpyxl", "matplotlib",
    "ipykernel", "keras",
]


def package_version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida", type=Path, default=None,
        help="Ruta opcional a JSON; sin este argumento imprime solamente.",
    )
    args = parser.parse_args()
    data = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "plataforma": platform.system(),
        "arquitectura": platform.machine(),
        "paquetes": {name: package_version(name) for name in PACKAGES},
        "pendiente_registro_manual": {
            "codesys": "Registrar version de IDE/controlador y bibliotecas",
            "factory_io": "Registrar version, driver activo y conexion OPC DA",
            "modbus": "Registrar que los HR0-HR7/IR0 se verificaron en ejecucion",
            "modelos": "Registrar modelo y version con los que se comprobo inferencia",
        },
        "nota": "No implica que los componentes hayan sido ejecutados o validados.",
    }
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.salida is None:
        print(content, end="")
    else:
        ruta = args.salida
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(content, encoding="utf-8")
        print(f"Entorno registrado en: {ruta}")


if __name__ == "__main__":
    main()
