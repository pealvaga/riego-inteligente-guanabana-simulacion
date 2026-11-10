import math
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from collections import deque

import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from pymodbus.client import ModbusTcpClient


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
UPDATE_MS = 1000
REAL_SECONDS_PER_SIM_HOUR = 60.0
MAX_REAL_TICK_SECONDS = 5.0  # Evita saltos excesivos por suspensión del PC.

# ============================================================
# MODELOS DE INTELIGENCIA ARTIFICIAL
# ============================================================
PREDICTION_MODEL_PATH = BASE_DIR / "modelo_prediccion_humedad.pkl"
IMAGE_MODEL_PATH = BASE_DIR / "mejor_modelo_hojas_finetuning.keras"
IMAGE_SIZE = 224
IMAGE_AI_THRESHOLD = 0.90

# Versión del balance hídrico utilizado para el entrenamiento.
SOIL_MODEL_VERSION = "balance_hidrico_temperatura_v2"
AI_STEP_MINUTES = 10
HUMIDITY_MIN = 60.0
FORECAST_RECURSIVE_STEPS = 12
FORECAST_TREND_WINDOW = 4
MAX_FORECAST_HOURS = 72
MAX_FORECAST_STEPS = int(MAX_FORECAST_HOURS * 60 / AI_STEP_MINUTES)
MIN_DROP_PER_STEP = 0.01

EXPECTED_MODEL_VARIABLES = [
    "Temperatura", "Precipitacion", "HumedadSuelo", "RiegoActivo",
    "HumedadSuelo_lag1", "HumedadSuelo_lag2",
    "Temperatura_lag1", "Temperatura_lag2",
    "Precipitacion_lag1", "Precipitacion_lag2",
    "RiegoActivo_lag1", "RiegoActivo_lag2",
]

# ============================================================
# BALANCE HÍDRICO DEL SUELO: ÁRBOL ADULTO
# ============================================================
# theta en fracción volumétrica; Zr en metros.
FIELD_CAPACITY = 0.28
WILTING_POINT = 0.13
ROOT_DEPTH_M = 0.60
TOTAL_AVAILABLE_WATER_MM = (
    1000.0 * (FIELD_CAPACITY - WILTING_POINT) * ROOT_DEPTH_M
)  # 90 mm

# Supuestos de configuración: NO mediciones meteorológicas locales.
# Hargreaves-Samani: ET0 = 0.0023*(Tmedia+17.8)*sqrt(Tmax-Tmin)*0.408*Ra
# Se supone una amplitud térmica diaria constante y radiación de referencia;
# la temperatura indicada en la interfaz se interpreta como media diaria.
TEMPERATURE_REFERENCE_C = 28.0
DIURNAL_TEMPERATURE_RANGE_C = 8.0
EXTRATERRESTRIAL_RADIATION_MJ_M2_DAY = 33.0
CROP_COEFFICIENT_KC = 0.85
IRRIGATION_FLOW_L_H = 32.0
IRRIGATION_EFFICIENCY = 0.85
IRRIGATED_AREA_M2 = 20.0
IRRIGATION_INPUT_MM_H = (
    IRRIGATION_FLOW_L_H * IRRIGATION_EFFICIENCY / IRRIGATED_AREA_M2
)  # 1.36 mm/h

# ============================================================
# MAPA MODBUS: NO SE CAMBIA
# ============================================================
REG_TEMPERATURA = 0
REG_LLUVIA = 1
REG_HUMEDAD = 2
REG_HEARTBEAT = 3
REG_DECISION_IA = 4
REG_DIA_SIM = 5
REG_HORA_SIM = 6
REG_MINUTO_SIM = 7
REG_RIEGO_ACTIVO = 0  # Input register leído desde CODESYS.


def calculate_et0_from_temperature(temperature_c: float) -> float:
    """Estima ET0 [mm/día] por Hargreaves-Samani con ΔT y Ra supuestos.

    Fórmula de referencia: FAO-56 / Hargreaves-Samani; valores locales de
    oscilación diaria y radiación requieren calibración si se usa en campo.
    """
    temperature = float(temperature_c)
    if not math.isfinite(temperature):
        raise ValueError("La temperatura debe ser un número finito.")
    return max(
        0.0,
        0.0023
        * (temperature + 17.8)
        * math.sqrt(DIURNAL_TEMPERATURE_RANGE_C)
        * 0.408
        * EXTRATERRESTRIAL_RADIATION_MJ_M2_DAY,
    )


def calculate_water_balance_step(
    storage_mm: float,
    rain_mm_h: float,
    irrigation_on: bool,
    et0_mm_day: float,
    delta_sim_hours: float,
) -> tuple[float, float]:
    """Devuelve (almacenamiento_nuevo_mm, drenaje_profundo_mm).

    Aproximación en un único depósito de la zona radicular. No representa
    escorrentía, ascenso capilar, variaciones espaciales o estrés hídrico.
    Las magnitudes de lluvia y ET0 deben ser no negativas.
    """
    if not all(math.isfinite(float(x)) for x in (
        storage_mm, rain_mm_h, et0_mm_day, delta_sim_hours
    )):
        raise ValueError("Los valores del balance hídrico deben ser finitos.")

    dt = max(0.0, float(delta_sim_hours))
    rain = max(0.0, float(rain_mm_h)) * dt
    irrigation = IRRIGATION_INPUT_MM_H * dt if irrigation_on else 0.0
    crop_evapotranspiration = (
        max(0.0, float(et0_mm_day)) * CROP_COEFFICIENT_KC / 24.0 * dt
    )
    unbounded = (
        float(storage_mm) + rain + irrigation - crop_evapotranspiration
    )
    drainage_mm = max(0.0, unbounded - TOTAL_AVAILABLE_WATER_MM)
    new_storage = max(0.0, min(TOTAL_AVAILABLE_WATER_MM, unbounded))
    return new_storage, drainage_mm


class SimuladorCultivo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de guanábana - Balance hídrico + Modbus TCP + IA")
        self.geometry("1060x800")
        self.minsize(980, 740)

        # Estado de la simulación: S (mm) es el estado primario.
        self.running = False
        self.sim_seconds = 0.0
        self.water_storage_mm = TOTAL_AVAILABLE_WATER_MM * 0.55
        self.humidity = 55.0  # % de AGUA DISPONIBLE, no % volumétrico.
        self.total_drainage_mm = 0.0
        self.irrigation_on = False
        self.last_tick_monotonic = time.monotonic()

        # Riego normal/fertirriego, determinado por IA de imágenes.
        self.ia_decision = 0

        # Modbus TCP
        self.client = None
        self.modbus_connected = False
        self.heartbeat = 0

        # Random Forest
        self.ai_model = None
        self.ai_variables = []
        self.ai_model_loaded = False
        self.ai_model_error = ""
        self.ai_history = deque(maxlen=3)
        self.last_ai_sample_total_minute = None
        self.last_predicted_humidity = None
        self.last_next_irrigation = None

        # IA de hojas
        self.image_ai_model = None
        self.image_ai_loaded = False
        self.image_ai_error = ""
        self.selected_image_path = None
        self.image_preview_photo = None

        # Entradas Tkinter
        self.temperature_var = tk.DoubleVar(value=28.0)
        self.rain_var = tk.DoubleVar(value=0.0)
        self.initial_humidity_var = tk.DoubleVar(value=55.0)
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.IntVar(value=502)
        self.device_id_var = tk.IntVar(value=1)

        # Monitorización
        self.time_text = tk.StringVar(value="Día 1 - 00:00")
        self.humidity_text = tk.StringVar(value="55.0 %")
        self.irrigation_text = tk.StringVar(value="INACTIVO")
        self.sim_status_text = tk.StringVar(value="PAUSADO")
        self.modbus_status_text = tk.StringVar(value="DESCONECTADO")
        self.day_modbus_text = tk.StringVar(value="Día: 1")
        self.hour_modbus_text = tk.StringVar(value="Hora: 0")
        self.minute_modbus_text = tk.StringVar(value="Minuto: 0")
        self.ia_status_text = tk.StringVar(value="SIN DECISIÓN")
        self.ia_register_text = tk.StringVar(value="HR4 = 0")
        self.ai_prediction_text = tk.StringVar(value="IA predictiva: verificando modelo...")
        self.image_model_status_text = tk.StringVar(value="Modelo de imágenes: cargando...")
        self.image_path_text = tk.StringVar(value="Ninguna imagen seleccionada")
        self.image_result_text = tk.StringVar(value="Seleccione una imagen para analizar.")
        self.image_sana_text = tk.StringVar(value="Sana: --")
        self.image_deficiencia_text = tk.StringVar(value="Deficiencia: --")
        self.image_confianza_text = tk.StringVar(value="Confianza: --")

        self._load_prediction_model()
        self._load_image_model()
        self._build_ui()
        self._refresh_labels()
        self._refresh_ai_text()
        self._update_ia_decision_display()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(UPDATE_MS, self._tick)

    @staticmethod
    def _get_float(variable, default: float) -> float:
        try:
            result = float(variable.get())
            return result if math.isfinite(result) else default
        except (ValueError, TypeError, tk.TclError):
            return default

    # ========================================================
    # CARGA DE MODELOS
    # ========================================================
    def _load_prediction_model(self):
        """Carga automáticamente el paquete .pkl de esta carpeta."""
        try:
            ruta = PREDICTION_MODEL_PATH
            if not ruta.exists():
                raise FileNotFoundError(
                    f"No se encontró '{ruta.name}'. "
                    "La simulación ambiental y Modbus siguen operativos."
                )

            import joblib
            package = joblib.load(ruta)
            if not isinstance(package, dict) or not {"modelo", "variables"}.issubset(package):
                raise ValueError("El .pkl no contiene 'modelo' y 'variables'.")

            # No aceptar un Random Forest entrenado con otra dinámica de suelo.
            if package.get("simulador_modelo_version") != SOIL_MODEL_VERSION:
                raise ValueError(
                    "MODELO ANTERIOR / SIN VERIFICACIÓN DE COMPATIBILIDAD. "
                    "Se requiere reentrenar Random Forest con datos del balance hídrico "
                    f"y guardar 'simulador_modelo_version'='{SOIL_MODEL_VERSION}' "
                    "dentro del paquete .pkl."
                )

            variables = list(package["variables"])
            if variables != EXPECTED_MODEL_VARIABLES:
                raise ValueError("Las variables del modelo no corresponden al entrenamiento.")
            if int(package.get("paso_minutos", AI_STEP_MINUTES)) != AI_STEP_MINUTES:
                raise ValueError("El modelo no está entrenado a intervalos de 10 minutos.")

            self.ai_model = package["modelo"]
            self.ai_variables = variables
            if hasattr(self.ai_model, "n_jobs"):
                self.ai_model.n_jobs = 1
            self.ai_model_loaded = True
            self.ai_model_error = ""
        except Exception as exc:
            self.ai_model = None
            self.ai_variables = []
            self.ai_model_loaded = False
            self.ai_model_error = str(exc)

    def _load_image_model(self):
        try:
            if not IMAGE_MODEL_PATH.exists():
                raise FileNotFoundError(f"No se encontró '{IMAGE_MODEL_PATH.name}'.")
            from tensorflow.keras.models import load_model
            self.image_ai_model = load_model(str(IMAGE_MODEL_PATH), compile=False)
            self.image_ai_loaded = True
            self.image_ai_error = ""
            self.image_model_status_text.set("Modelo de imágenes: CARGADO")
        except Exception as exc:
            self.image_ai_model = None
            self.image_ai_loaded = False
            self.image_ai_error = str(exc)
            self.image_model_status_text.set(f"Modelo de imágenes: ERROR ({exc})")

    # ========================================================
    # INTERFAZ
    # ========================================================
    def _build_ui(self):
        header = ttk.Frame(self, padding=(15, 15, 15, 5))
        header.pack(fill="x")
        ttk.Label(
            header, text="Simulador ambiental del cultivo de guanábana",
            font=("Segoe UI", 19, "bold")
        ).pack()
        ttk.Label(header, text="Árbol adulto | Balance hídrico | 1 min real = 1 h simulada").pack(pady=(4, 6))
        connection_bar = ttk.Frame(header)
        connection_bar.pack(fill="x", pady=(6, 0))
        ttk.Label(connection_bar, text="Modbus:").pack(side="left")
        ttk.Label(
            connection_bar, textvariable=self.modbus_status_text,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(6, 20))
        ttk.Label(connection_bar, text="Tipo de riego:").pack(side="left")
        ttk.Label(
            connection_bar, textvariable=self.ia_status_text,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=6)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)
        self.tab_sim = ttk.Frame(notebook, padding=15)
        self.tab_ia = ttk.Frame(notebook, padding=15)
        self.tab_modbus = ttk.Frame(notebook, padding=15)
        notebook.add(self.tab_sim, text="Simulación ambiental")
        notebook.add(self.tab_ia, text="IA - tipo de riego")
        notebook.add(self.tab_modbus, text="Comunicación Modbus")
        self._build_simulation_tab()
        self._build_ia_tab()
        self._build_modbus_tab()

    def _build_simulation_tab(self):
        variables = ttk.LabelFrame(self.tab_sim, text="Variables ambientales", padding=15)
        variables.pack(fill="x", pady=(0, 12))

        ttk.Label(variables, text="Temperatura (°C):").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        ttk.Spinbox(
            variables, from_=10, to=45, increment=0.5,
            textvariable=self.temperature_var, width=12
        ).grid(row=0, column=1, padx=8)
        ttk.Label(variables, text="Precipitación (mm/h):").grid(
            row=0, column=2, sticky="w", padx=(25, 8), pady=8
        )
        ttk.Spinbox(
            variables, from_=0, to=100, increment=0.5,
            textvariable=self.rain_var, width=12
        ).grid(row=0, column=3, padx=8)
        ttk.Label(variables, text="Humedad inicial (% agua disponible):").grid(
            row=1, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Spinbox(
            variables, from_=0, to=100, increment=1,
            textvariable=self.initial_humidity_var, width=12
        ).grid(row=1, column=1, padx=8)
        controls = ttk.Frame(self.tab_sim)
        controls.pack(fill="x", pady=(0, 12))
        ttk.Button(controls, text="Iniciar simulación", command=self.start_simulation).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(controls, text="Pausar", command=self.pause_simulation).pack(
            side="left", padx=8
        )
        ttk.Button(controls, text="Reiniciar", command=self.reset_simulation).pack(
            side="left", padx=8
        )

        # Predicción en pantalla, sin botones de carga ni de exportación.
        forecast_frame = ttk.LabelFrame(
            self.tab_sim, text="IA predictiva - Próximo riego", padding=12
        )
        forecast_frame.pack(fill="x", pady=(0, 12))
        ttk.Label(
            forecast_frame,
            textvariable=self.ai_prediction_text,
            wraplength=890,
            justify="left",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=3, pady=3)

        monitor = ttk.LabelFrame(self.tab_sim, text="Estado del cultivo", padding=15)
        monitor.pack(fill="both", expand=True)
        monitor.columnconfigure(1, weight=1)
        monitor_items = [
            ("Tiempo simulado:", self.time_text, 14),
            ("Humedad (% agua disponible):", self.humidity_text, 22),
            ("Riego recibido desde CODESYS:", self.irrigation_text, 12),
            ("Estado simulación:", self.sim_status_text, 11),
        ]
        for row_num, (label, value, size) in enumerate(monitor_items):
            ttk.Label(monitor, text=label).grid(row=row_num, column=0, sticky="w", pady=6)
            ttk.Label(
                monitor, textvariable=value,
                font=("Segoe UI", size, "bold" if size >= 12 else "normal")
            ).grid(row=row_num, column=1, sticky="w", padx=25, pady=6)

        self.humidity_bar = ttk.Progressbar(
            monitor, orient="horizontal", mode="determinate", maximum=100
        )
        self.humidity_bar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 16))

    def _build_ia_tab(self):
        info = ttk.LabelFrame(
            self.tab_ia, text="IA de visión artificial - Selección del tipo de riego",
            padding=15
        )
        info.pack(fill="x", pady=(0, 12))
        ttk.Label(
            info,
            text=(
                "Seleccione una imagen de una hoja. La IA determina la probabilidad "
                "de hoja sana o de síntomas compatibles con deficiencia nutricional. "
                "El fertirriego solo se autoriza si la probabilidad de deficiencia "
                "es igual o superior al 90 %."
            ),
            wraplength=900, justify="left"
        ).pack(anchor="w")
        ttk.Label(
            info, textvariable=self.image_model_status_text,
            font=("Segoe UI", 10, "bold"), wraplength=890
        ).pack(anchor="w", pady=(10, 0))

        main_frame = ttk.Frame(self.tab_ia)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        image_frame = ttk.LabelFrame(main_frame, text="Imagen de la hoja", padding=15)
        image_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.image_preview_label = tk.Label(
            image_frame, text="Sin imagen", width=48, height=18,
            relief="sunken", bg="white", anchor="center"
        )
        self.image_preview_label.pack(fill="both", expand=True, pady=(0, 10))
        ttk.Label(
            image_frame, textvariable=self.image_path_text,
            wraplength=410, justify="center"
        ).pack(pady=(0, 10))
        buttons = ttk.Frame(image_frame)
        buttons.pack(pady=8)
        ttk.Button(buttons, text="Cargar imagen", command=self.select_leaf_image).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Analizar imagen", command=self.analyze_leaf_image).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Limpiar", command=self.clear_leaf_analysis).pack(
            side="left", padx=5
        )

        result_frame = ttk.LabelFrame(main_frame, text="Resultado de la IA", padding=20)
        result_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(result_frame, text="Clasificación:").pack(anchor="w", pady=(5, 5))
        ttk.Label(
            result_frame, textvariable=self.image_result_text,
            font=("Segoe UI", 15, "bold"), wraplength=400, justify="left"
        ).pack(anchor="w", pady=(0, 20))
        ttk.Separator(result_frame).pack(fill="x", pady=10)
        for variable, bold in (
            (self.image_sana_text, False),
            (self.image_deficiencia_text, False),
            (self.image_confianza_text, True),
        ):
            ttk.Label(
                result_frame, textvariable=variable,
                font=("Segoe UI", 13, "bold" if bold else "normal")
            ).pack(anchor="w", pady=6)
        ttk.Separator(result_frame).pack(fill="x", pady=10)
        ttk.Label(result_frame, text="Tipo de riego enviado a CODESYS:").pack(
            anchor="w", pady=(10, 5)
        )
        ttk.Label(
            result_frame, textvariable=self.ia_status_text,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 10))
        ttk.Label(
            result_frame, textvariable=self.ia_register_text,
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", pady=5)
        ttk.Label(
            result_frame,
            text="HR4 = 0 → Sin decisión\nHR4 = 1 → Riego normal\nHR4 = 2 → Fertirriego",
            justify="left"
        ).pack(anchor="w", pady=(20, 0))

    def _build_modbus_tab(self):
        comm = ttk.LabelFrame(self.tab_modbus, text="Configuración Modbus TCP", padding=20)
        comm.pack(fill="x", pady=(0, 15))
        for idx, (label, var, width) in enumerate((
            ("IP CODESYS:", self.ip_var, 18),
            ("Puerto:", self.port_var, 10),
            ("Device ID:", self.device_id_var, 8),
        )):
            ttk.Label(comm, text=label).grid(row=0, column=idx * 2, padx=8, pady=10)
            ttk.Entry(comm, textvariable=var, width=width).grid(
                row=0, column=idx * 2 + 1, padx=8
            )
        ttk.Button(comm, text="Conectar", command=self.connect_modbus).grid(
            row=1, column=0, padx=8, pady=12
        )
        ttk.Button(comm, text="Desconectar", command=self.disconnect_modbus).grid(
            row=1, column=1, padx=8, pady=12
        )
        ttk.Label(comm, text="Estado:").grid(row=2, column=0, padx=8, pady=8)
        ttk.Label(
            comm, textvariable=self.modbus_status_text,
            font=("Segoe UI", 11, "bold")
        ).grid(row=2, column=1, columnspan=5, sticky="w", padx=8)

        time_frame = ttk.LabelFrame(
            self.tab_modbus, text="Tiempo simulado enviado a CODESYS", padding=15
        )
        time_frame.pack(fill="x", pady=(0, 15))
        for var in (self.day_modbus_text, self.hour_modbus_text, self.minute_modbus_text):
            ttk.Label(
                time_frame, textvariable=var, font=("Segoe UI", 10, "bold")
            ).pack(side="left", padx=15)

        mapping = ttk.LabelFrame(self.tab_modbus, text="Mapa de registros", padding=20)
        mapping.pack(fill="both", expand=True)
        map_text = (
            "PYTHON → CODESYS\n\n"
            "HR0 / 40001   Temperatura ×10\n"
            "HR1 / 40002   Precipitación ×10\n"
            "HR2 / 40003   Humedad disponible ×10\n"
            "HR3 / 40004   Heartbeat\n"
            "HR4 / 40005   Tipo de riego (0, 1, 2)\n"
            "HR5 / 40006   Día simulado\n"
            "HR6 / 40007   Hora simulada\n"
            "HR7 / 40008   Minuto simulado\n\n"
            "CODESYS → PYTHON\n\n"
            "IR0 / 30001   Estado del riego (0 o 1)\n\n"
            "No cambian direcciones ni el escalamiento Modbus."
        )
        ttk.Label(
            mapping, text=map_text, justify="left", font=("Consolas", 11)
        ).pack(anchor="w")

    # ========================================================
    # IA DE HOJAS: NO SE MODIFICA EL MODELO
    # ========================================================
    def select_leaf_image(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen de hoja",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if not ruta:
            return
        try:
            path = Path(ruta)
            with Image.open(path) as img:
                preview = img.convert("RGB")
            try:
                resampling = Image.Resampling.LANCZOS
            except AttributeError:
                resampling = Image.LANCZOS
            preview.thumbnail((420, 330), resampling)
            self.image_preview_photo = ImageTk.PhotoImage(preview)
            self.image_preview_label.config(image=self.image_preview_photo, text="")
            self.selected_image_path = path
            self.image_path_text.set(path.name)
            self.image_result_text.set("Imagen cargada.\nPulse 'Analizar imagen'.")
            self.image_sana_text.set("Sana: --")
            self.image_deficiencia_text.set("Deficiencia: --")
            self.image_confianza_text.set("Confianza: --")
        except Exception as exc:
            self.selected_image_path = None
            messagebox.showerror("Error", f"No fue posible cargar la imagen.\n\n{exc}")

    def analyze_leaf_image(self):
        if not self.image_ai_loaded:
            messagebox.showerror(
                "IA de imágenes", f"El modelo no está cargado.\n\n{self.image_ai_error}"
            )
            return
        if self.selected_image_path is None:
            messagebox.showwarning("IA de imágenes", "Primero debe seleccionar una imagen.")
            return
        try:
            with Image.open(self.selected_image_path) as img:
                image_array = np.asarray(
                    img.convert("RGB").resize((IMAGE_SIZE, IMAGE_SIZE)), dtype=np.float32
                )
            # Preprocess incluido en la red: NO dividir entre 255.
            image_array = np.expand_dims(image_array, axis=0)
            prediction = np.asarray(
                self.image_ai_model.predict(image_array, verbose=0)
            )
            if prediction.size != 1:
                raise ValueError("El modelo no tiene una salida binaria.")

            # Se mantiene la convención del código original:
            # la salida de la red representa la clase 'deficiencia'.
            probability_deficiency = float(prediction.reshape(-1)[0])
            if not math.isfinite(probability_deficiency):
                raise ValueError("El modelo devolvió una probabilidad no válida.")
            probability_deficiency = max(0.0, min(1.0, probability_deficiency))
            probability_healthy = 1.0 - probability_deficiency

            self.image_sana_text.set(f"Sana: {probability_healthy * 100:.2f} %")
            self.image_deficiencia_text.set(
                f"Deficiencia: {probability_deficiency * 100:.2f} %"
            )
            confidence = max(probability_healthy, probability_deficiency)
            if probability_deficiency >= IMAGE_AI_THRESHOLD:
                self.ia_decision = 2
                self.image_result_text.set(
                    "DEFICIENCIA NUTRICIONAL DETECTADA\n\nRecomendación:\nFERTIRRIEGO"
                )
            elif probability_healthy >= IMAGE_AI_THRESHOLD:
                self.ia_decision = 1
                self.image_result_text.set("HOJA SANA\n\nRecomendación:\nRIEGO NORMAL")
            else:
                self.ia_decision = 1
                self.image_result_text.set(
                    "RESULTADO CON BAJA CONFIANZA\n\n"
                    "No se autoriza fertirriego.\n\nRecomendación:\nRIEGO NORMAL"
                )
            self.image_confianza_text.set(
                f"Confianza de clasificación: {confidence * 100:.2f} %"
            )
            self._update_ia_decision_display()
            if self.modbus_connected:
                self.write_all_to_codesys()
        except Exception as exc:
            messagebox.showerror("Error de IA", f"No fue posible analizar la imagen.\n\n{exc}")

    def clear_leaf_analysis(self):
        self.selected_image_path = None
        self.image_preview_photo = None
        self.image_preview_label.config(image="", text="Sin imagen")
        self.image_path_text.set("Ninguna imagen seleccionada")
        self.image_result_text.set("Seleccione una imagen para analizar.")
        self.image_sana_text.set("Sana: --")
        self.image_deficiencia_text.set("Deficiencia: --")
        self.image_confianza_text.set("Confianza: --")
        self.ia_decision = 0
        self._update_ia_decision_display()
        if self.modbus_connected:
            self.write_all_to_codesys()

    def _update_ia_decision_display(self):
        self.ia_status_text.set({
            0: "SIN DECISIÓN", 1: "RIEGO NORMAL", 2: "FERTIRRIEGO"
        }.get(self.ia_decision, "SIN DECISIÓN"))
        self.ia_register_text.set(f"HR4 = {self.ia_decision}")

    # ========================================================
    # MODBUS (MISMAS DIRECCIONES)
    # ========================================================
    def _write_registers(self, address, values):
        device_id = int(self.device_id_var.get())
        try:
            return self.client.write_registers(
                address=address, values=values, device_id=device_id
            )
        except TypeError:
            return self.client.write_registers(
                address=address, values=values, slave=device_id
            )

    def _read_input_registers(self, address, count):
        device_id = int(self.device_id_var.get())
        try:
            return self.client.read_input_registers(
                address=address, count=count, device_id=device_id
            )
        except TypeError:
            return self.client.read_input_registers(
                address=address, count=count, slave=device_id
            )

    def connect_modbus(self):
        self.disconnect_modbus()
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get())
            self.client = ModbusTcpClient(host=ip, port=port, timeout=1)
            self.modbus_connected = bool(self.client.connect())
            if self.modbus_connected:
                self.modbus_status_text.set(f"CONECTADO A {ip}:{port}")
                self.read_irrigation_from_codesys()
                self.write_all_to_codesys()
            else:
                self.modbus_status_text.set("NO SE PUDO CONECTAR")
                self.disconnect_modbus(keep_status=True)
        except Exception as exc:
            self.modbus_status_text.set(f"ERROR: {exc}")
            self.disconnect_modbus(keep_status=True)

    def disconnect_modbus(self, keep_status=False):
        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                pass
        self.client = None
        self.modbus_connected = False
        self.irrigation_on = False
        if not keep_status:
            self.modbus_status_text.set("DESCONECTADO")

    def read_irrigation_from_codesys(self):
        if not self.modbus_connected or self.client is None:
            return
        try:
            response = self._read_input_registers(address=REG_RIEGO_ACTIVO, count=1)
            if response.isError():
                self.modbus_status_text.set("ERROR LEYENDO RIEGO")
                self.irrigation_on = False  # Estado seguro ante error de lectura.
                return
            self.irrigation_on = response.registers[0] != 0
        except Exception as exc:
            self.irrigation_on = False
            self.modbus_status_text.set(f"ERROR LEYENDO MODBUS: {exc}")

    def write_all_to_codesys(self):
        if not self.modbus_connected or self.client is None:
            return
        try:
            temperature = self._get_float(self.temperature_var, 28.0)
            rain = max(0.0, self._get_float(self.rain_var, 0.0))
            day, hour, minute = self.get_simulated_time()
            self.heartbeat = (self.heartbeat + 1) % 65536
            values = [
                self._to_u16(round(temperature * 10)),
                self._to_u16(round(rain * 10)),
                self._to_u16(round(self.humidity * 10)),
                self._to_u16(self.heartbeat),
                self._to_u16(self.ia_decision),
                self._to_u16(day),
                self._to_u16(hour),
                self._to_u16(minute),
            ]
            response = self._write_registers(address=0, values=values)
            if response.isError():
                self.modbus_status_text.set("ERROR ESCRIBIENDO HR0-HR7")
                return
            self.modbus_status_text.set("COMUNICACIÓN OK")
        except Exception as exc:
            self.modbus_status_text.set(f"ERROR ESCRIBIENDO MODBUS: {exc}")

    @staticmethod
    def _to_u16(value):
        return max(0, min(65535, int(value)))

    # ========================================================
    # TIEMPO Y CONTROLES DE SIMULACIÓN
    # ========================================================
    def get_simulated_time(self):
        total_hours = int(self.sim_seconds // 3600)
        day = total_hours // 24 + 1
        hour = total_hours % 24
        minute = int((self.sim_seconds % 3600) // 60)
        return day, hour, minute

    @staticmethod
    def add_simulated_minutes(day, hour, minute, extra_minutes):
        total = (day - 1) * 1440 + hour * 60 + minute + int(extra_minutes)
        new_day = total // 1440 + 1
        rest = total % 1440
        return int(new_day), int(rest // 60), int(rest % 60)

    def start_simulation(self):
        if self.modbus_connected:
            self.read_irrigation_from_codesys()
        if self.last_ai_sample_total_minute is None:
            self._capture_ai_sample(force=True)
        self.running = True
        self.last_tick_monotonic = time.monotonic()
        self.sim_status_text.set("EN EJECUCIÓN")

    def pause_simulation(self):
        self.running = False
        self.sim_status_text.set("PAUSADO")

    def reset_simulation(self):
        self.running = False
        self.sim_seconds = 0.0
        initial = self._get_float(self.initial_humidity_var, 55.0)
        self.humidity = max(0.0, min(100.0, initial))
        self.water_storage_mm = TOTAL_AVAILABLE_WATER_MM * self.humidity / 100.0
        self.total_drainage_mm = 0.0

        # Reinicia las tres muestras temporales del predictor.
        self.ai_history.clear()
        self.last_ai_sample_total_minute = None
        self.last_predicted_humidity = None
        self.last_next_irrigation = None
        self.last_tick_monotonic = time.monotonic()
        self.sim_status_text.set("PAUSADO")
        self._refresh_labels()
        self._refresh_ai_text()
        if self.modbus_connected:
            self.write_all_to_codesys()

    # ========================================================
    # NUEVO MODELO AMBIENTAL: ECUACIONES (3) Y (12)
    # ========================================================
    def update_environmental_model(self, real_seconds):
        rain = max(0.0, self._get_float(self.rain_var, 0.0))
        temperature = self._get_float(self.temperature_var, TEMPERATURE_REFERENCE_C)
        et0 = calculate_et0_from_temperature(temperature)
        simulated_hours = max(0.0, real_seconds) / REAL_SECONDS_PER_SIM_HOUR
        self.sim_seconds += simulated_hours * 3600.0

        self.water_storage_mm, drainage = calculate_water_balance_step(
            storage_mm=self.water_storage_mm,
            rain_mm_h=rain,
            irrigation_on=self.irrigation_on,
            et0_mm_day=et0,
            delta_sim_hours=simulated_hours,
        )
        self.total_drainage_mm += drainage
        self.humidity = (
            self.water_storage_mm / TOTAL_AVAILABLE_WATER_MM * 100.0
        )

    # ========================================================
    # AVANCE CONTINUO HASTA LOS LÍMITES DE 10 MINUTOS
    # ========================================================
    def _advance_with_ai_samples(self, real_elapsed_seconds):
        """Toma una muestra exacta cada 10 minutos simulados."""
        restante = max(0.0, real_elapsed_seconds) * 3600.0 / REAL_SECONDS_PER_SIM_HOUR
        intervalo_seg = AI_STEP_MINUTES * 60.0
        while restante > 1e-7:
            limite = (math.floor((self.sim_seconds + 1e-6) / intervalo_seg) + 1) * intervalo_seg
            paso_seg = min(restante, max(0.0, limite - self.sim_seconds))
            if paso_seg <= 1e-7:
                self.sim_seconds = limite
                self._capture_ai_sample(force=True)
                continue
            self.update_environmental_model(
                paso_seg * REAL_SECONDS_PER_SIM_HOUR / 3600.0
            )
            restante -= paso_seg
            if self.sim_seconds >= limite - 1e-5:
                self.sim_seconds = limite
                self._capture_ai_sample(force=True)

    # ========================================================
    # RANDOM FOREST PREDICTIVO
    # ========================================================
    def _capture_ai_sample(self, force=False):
        if not self.ai_model_loaded:
            return
        # Una muestra exactamente cada diez minutos simulados.
        total_minute = int(round(self.sim_seconds / 60.0))
        if not force and total_minute % AI_STEP_MINUTES != 0:
            return
        if self.last_ai_sample_total_minute == total_minute:
            return
        day, hour, minute = self.get_simulated_time()
        sample = {
            "Dia": day,
            "Hora": hour,
            "Minuto": minute,
            "Temperatura": self._get_float(self.temperature_var, 28.0),
            "Precipitacion": max(0.0, self._get_float(self.rain_var, 0.0)),
            "HumedadSuelo": float(self.humidity),
            "RiegoActivo": int(self.irrigation_on),
        }

        self.ai_history.append(sample)
        self.last_ai_sample_total_minute = total_minute
        if len(self.ai_history) >= 3:
            self._run_ai_prediction()
        else:
            self._refresh_ai_text()

    @staticmethod
    def _build_feature_map(current, lag1, lag2):
        return {
            "Temperatura": current["Temperatura"],
            "Precipitacion": current["Precipitacion"],
            "HumedadSuelo": current["HumedadSuelo"],
            "RiegoActivo": current["RiegoActivo"],
            "HumedadSuelo_lag1": lag1["HumedadSuelo"],
            "HumedadSuelo_lag2": lag2["HumedadSuelo"],
            "Temperatura_lag1": lag1["Temperatura"],
            "Temperatura_lag2": lag2["Temperatura"],
            "Precipitacion_lag1": lag1["Precipitacion"],
            "Precipitacion_lag2": lag2["Precipitacion"],
            "RiegoActivo_lag1": lag1["RiegoActivo"],
            "RiegoActivo_lag2": lag2["RiegoActivo"],
        }

    def _predict_feature_map(self, feature_map):
        row = {name: float(feature_map[name]) for name in self.ai_variables}
        X = pd.DataFrame([row], columns=self.ai_variables)
        prediction = float(self.ai_model.predict(X)[0])
        return max(0.0, min(100.0, prediction))

    def _run_ai_prediction(self):
        try:
            current = dict(self.ai_history[-1])
            lag1 = dict(self.ai_history[-2])
            lag2 = dict(self.ai_history[-3])
            self.last_predicted_humidity = self._predict_feature_map(
                self._build_feature_map(current, lag1, lag2)
            )
            self.last_next_irrigation = self._estimate_next_irrigation(current, lag1, lag2)
            self._refresh_ai_text()
        except Exception as exc:
            self.last_predicted_humidity = None
            self.last_next_irrigation = None
            self.ai_prediction_text.set(
                "IA predictiva: ERROR DE PREDICCIÓN\n"
                "Humedad estimada en +10 min: --\n"
                f"Detalle: {exc}"
            )

    def _estimate_next_irrigation(self, current, lag1, lag2):
        time_tuple = (current["Dia"], current["Hora"], current["Minuto"])
        if self.irrigation_on:
            return {"status": "active", "minutes": 0, "time": time_tuple}
        if current["HumedadSuelo"] <= HUMIDITY_MIN:
            return {"status": "threshold", "minutes": 0, "time": time_tuple}

        future_current = dict(current)
        future_lag1 = dict(lag1)
        future_lag2 = dict(lag2)
        future_current["RiegoActivo"] = 0
        trajectory = [float(current["HumedadSuelo"])]

        for step in range(1, FORECAST_RECURSIVE_STEPS + 1):
            feature_map = self._build_feature_map(
                future_current, future_lag1, future_lag2
            )
            next_humidity = self._predict_feature_map(feature_map)
            trajectory.append(next_humidity)
            if next_humidity <= HUMIDITY_MIN:
                minutes_ahead = step * AI_STEP_MINUTES
                return {
                    "status": "estimated", "minutes": minutes_ahead,
                    "time": self.add_simulated_minutes(*time_tuple, minutes_ahead),
                }
            future_lag2 = dict(future_lag1)
            future_lag1 = dict(future_current)
            future_current = dict(future_current)
            future_current["HumedadSuelo"] = next_humidity
            future_current["RiegoActivo"] = 0

        window_size = min(FORECAST_TREND_WINDOW + 1, len(trajectory))
        recent = trajectory[-window_size:]
        drops = [recent[i] - recent[i + 1] for i in range(len(recent) - 1)]
        average_drop = sum(drops) / len(drops) if drops else 0.0
        if average_drop <= MIN_DROP_PER_STEP:
            return {"status": "not_found", "minutes": None, "time": None}
        remaining_humidity = max(0.0, trajectory[-1] - HUMIDITY_MIN)
        additional_steps = math.ceil(remaining_humidity / average_drop)
        total_steps = FORECAST_RECURSIVE_STEPS + additional_steps
        if total_steps > MAX_FORECAST_STEPS:
            return {"status": "not_found", "minutes": None, "time": None}
        minutes_ahead = total_steps * AI_STEP_MINUTES
        return {
            "status": "estimated", "minutes": minutes_ahead,
            "time": self.add_simulated_minutes(*time_tuple, minutes_ahead),
        }

    def _refresh_ai_text(self):
        if not self.ai_model_loaded:
            self.ai_prediction_text.set(
                "IA predictiva: MODELO NO CARGADO O INCOMPATIBLE\n"
                "Humedad estimada en +10 min: --\n"
                "Próximo riego previsto por IA: --\n"
                f"Motivo: {self.ai_model_error}"
            )
            return
        if len(self.ai_history) < 3 or self.last_predicted_humidity is None:
            self.ai_prediction_text.set(
                "IA predictiva: MODELO NUEVO CARGADO\n"
                "Humedad estimada en +10 min: ESPERANDO DATOS\n"
                "Próximo riego: ESPERANDO DATOS"
            )
            return

        next_irrigation = self.last_next_irrigation
        if next_irrigation is None:
            next_text = "RECALCULANDO"
        elif next_irrigation["status"] == "active":
            next_text = "RIEGO ACTIVO"
        elif next_irrigation["status"] == "threshold":
            next_text = "UMBRAL DE 60 % ALCANZADO"
        elif next_irrigation["status"] == "estimated":
            day, hour, minute = next_irrigation["time"]
            next_text = f"Día {day} - {hour:02d}:{minute:02d}"
        else:
            next_text = "NO ESTIMADO CON LAS CONDICIONES ACTUALES"
        self.ai_prediction_text.set(
            "IA predictiva: MODELO NUEVO CARGADO\n"
            f"Humedad estimada en +10 min: {self.last_predicted_humidity:.2f} %\n"
            f"Próximo riego: {next_text}"
        )

    # ========================================================
    # INTERFAZ Y BUCLE PRINCIPAL
    # ========================================================
    def _refresh_labels(self):
        day, hour, minute = self.get_simulated_time()
        self.time_text.set(f"Día {day} - {hour:02d}:{minute:02d}")
        self.humidity_text.set(f"{self.humidity:.2f} %")
        self.humidity_bar["value"] = self.humidity
        self.irrigation_text.set("ACTIVO" if self.irrigation_on else "INACTIVO")
        self.day_modbus_text.set(f"Día: {day}")
        self.hour_modbus_text.set(f"Hora: {hour}")
        self.minute_modbus_text.set(f"Minuto: {minute}")

    def _tick(self):
        now = time.monotonic()
        real_elapsed_seconds = min(
            MAX_REAL_TICK_SECONDS, max(0.0, now - self.last_tick_monotonic)
        )
        self.last_tick_monotonic = now

        # 1) Leer estado de riego desde CODESYS.
        if self.modbus_connected:
            self.read_irrigation_from_codesys()

        # 2) Calcular balance hídrico en tiempo simulado.
        if self.running:
            self._advance_with_ai_samples(real_elapsed_seconds)

        # 3) Comunicar con CODESYS.
        if self.modbus_connected:
            self.write_all_to_codesys()

        # 4) Actualizar interfaz.
        self._refresh_labels()
        self.after(UPDATE_MS, self._tick)

    def on_close(self):
        self.running = False
        self.disconnect_modbus()
        self.destroy()

if __name__ == "__main__":
    app = SimuladorCultivo()
    app.mainloop()
