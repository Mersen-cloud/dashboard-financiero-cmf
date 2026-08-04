"""
Extracción de indicadores macroeconómicos desde la API CMF Chile.
Documentación: https://api.cmfchile.cl
"""

import os
import json
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("CMF_API_KEY")
BASE_URL = "https://api.cmfchile.cl/api-sbifv3/recursos_api"

RAW_DIR   = Path(__file__).parent.parent / "data" / "raw"
CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean"


def _get(endpoint: str, reintentos: int = 3) -> dict:
    for intento in range(reintentos):
        try:
            r = requests.get(
                f"{BASE_URL}/{endpoint}",
                params={"apikey": API_KEY, "formato": "json"},
                timeout=30,
            )
            r.raise_for_status()
            return r.json()
        except (requests.ConnectionError, requests.Timeout) as e:
            if intento == reintentos - 1:
                raise
            time.sleep(2 ** intento)  # backoff: 1s, 2s, 4s


def _a_float(valor: str) -> float | None:
    """
    Convierte a float una serie con formato chileno: punto de miles y coma
    decimal (ej. '40.844,79'). Para estos valores (UF, dólar, euro, UTM) el
    punto es siempre separador de miles.
    """
    try:
        return float(str(valor).replace(".", "").replace(",", "."))
    except (ValueError, AttributeError):
        return None


def _a_float_tasa(valor: str) -> float | None:
    """
    Convierte a float las tasas TIP/TMC, cuyo endpoint entrega el valor con
    PUNTO decimal (ej. '42.82' = 42,82%). No hay separador de miles porque
    las tasas anuales no superan las tres cifras.
    """
    try:
        return float(str(valor).strip())
    except (ValueError, AttributeError):
        return None


def extraer_serie_anual(recurso: str, clave: str, anios: list[int]) -> pd.DataFrame:
    """
    Descarga una serie histórica anual y la devuelve como DataFrame limpio.
    recurso: nombre del endpoint (ej. 'uf', 'dolar', 'ipc')
    clave:   clave JSON de la respuesta (ej. 'UFs', 'Dolares', 'IPCs')
    """
    frames = []
    for anio in anios:
        data = _get(f"{recurso}/{anio}")
        registros = data.get(clave, [])
        df = pd.DataFrame(registros)
        df["anio"] = anio
        frames.append(df)
        # Guardar raw
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        (RAW_DIR / f"{recurso}_{anio}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    resultado = pd.concat(frames, ignore_index=True)
    resultado["Fecha"] = pd.to_datetime(resultado["Fecha"])
    resultado["valor"] = resultado["Valor"].apply(_a_float)
    return resultado[["Fecha", "valor"]].rename(columns={"Fecha": "fecha"})


def extraer_tip_tmc(recurso: str, clave: str, anios: list[int]) -> pd.DataFrame:
    """
    Descarga TIP o TMC por mes/año. Devuelve DataFrame con una fila por
    categoría de operación y período.
    """
    frames = []
    for anio in anios:
        for mes in range(1, 13):
            try:
                data = _get(f"{recurso}/{anio}/{mes:02d}")
                time.sleep(0.3)
            except requests.HTTPError:
                continue
            registros = data.get(clave, [])
            RAW_DIR.mkdir(parents=True, exist_ok=True)
            (RAW_DIR / f"{recurso}_{anio}_{mes:02d}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            for reg in registros:
                reg["anio"] = anio
                reg["mes"]  = mes
                reg["fecha"] = pd.Timestamp(anio, mes, 1)
            frames.extend(registros)
    df = pd.DataFrame(frames)
    if df.empty:
        return df
    df["valor"] = df["Valor"].apply(_a_float_tasa)
    cols = ["fecha", "Titulo", "SubTitulo", "valor"]
    return df[[c for c in cols if c in df.columns]]


def guardar_clean(df: pd.DataFrame, nombre: str) -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    ruta = CLEAN_DIR / f"{nombre}.csv"
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"  Guardado: {ruta.name}  ({len(df)} filas)")


if __name__ == "__main__":
    ANIOS = list(range(2020, 2027))

    print("Extrayendo UF...")
    df_uf = extraer_serie_anual("uf", "UFs", ANIOS)
    guardar_clean(df_uf, "uf")

    print("Extrayendo Dólar...")
    df_dolar = extraer_serie_anual("dolar", "Dolares", ANIOS)
    guardar_clean(df_dolar, "dolar")

    print("Extrayendo Euro...")
    df_euro = extraer_serie_anual("euro", "Euros", ANIOS)
    guardar_clean(df_euro, "euro")

    print("Extrayendo IPC...")
    df_ipc = extraer_serie_anual("ipc", "IPCs", ANIOS)
    guardar_clean(df_ipc, "ipc")

    print("Extrayendo UTM...")
    df_utm = extraer_serie_anual("utm", "UTMs", ANIOS)
    guardar_clean(df_utm, "utm")

    print("Extrayendo TIP (tasas de interés promedio)...")
    df_tip = extraer_tip_tmc("tip", "TIPs", list(range(2020, 2027)))
    guardar_clean(df_tip, "tip")

    print("Extrayendo TMC (tasas máximas convencionales)...")
    df_tmc = extraer_tip_tmc("tmc", "TMCs", list(range(2020, 2027)))
    guardar_clean(df_tmc, "tmc")

    print("\nExtracción completada.")
