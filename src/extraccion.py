"""
Módulo de extracción de datos desde la API CMF Bancos.
Documentación oficial: https://api.cmfchile.cl/
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CMF_API_KEY")
BASE_URL = "https://api.cmfchile.cl/api-sbifv3/recursos_api"

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean"


def _get(endpoint: str, params: dict | None = None) -> dict:
    """Llama a la API CMF y devuelve el JSON de respuesta."""
    url = f"{BASE_URL}/{endpoint}"
    defaults = {"apikey": API_KEY, "formato": "json"}
    response = requests.get(url, params={**defaults, **(params or {})}, timeout=30)
    response.raise_for_status()
    return response.json()


def extraer_colocaciones(periodo: str) -> pd.DataFrame:
    """
    Extrae colocaciones por banco para un período dado.

    periodo: formato AAAAMM, por ejemplo '202312'
    """
    data = _get(f"colocaciones/{periodo}")
    registros = data.get("Colocaciones", [])
    df = pd.DataFrame(registros)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ruta_raw = RAW_DIR / f"colocaciones_{periodo}.json"
    ruta_raw.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return df


def extraer_morosidad(periodo: str) -> pd.DataFrame:
    """Extrae índices de morosidad por banco para un período dado."""
    data = _get(f"cartera_vencida/{periodo}")
    registros = data.get("CartVencida", [])
    df = pd.DataFrame(registros)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ruta_raw = RAW_DIR / f"morosidad_{periodo}.json"
    ruta_raw.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return df


def limpiar_numericos(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Convierte columnas de texto con formato chileno (puntos de miles, comas decimales)
    a float. Los valores no convertibles se dejan como NaN y se registran en consola.
    """
    for col in columnas:
        if col not in df.columns:
            continue
        original_nulos = df[col].isna().sum()
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .pipe(pd.to_numeric, errors="coerce")
        )
        nuevos_nulos = df[col].isna().sum() - original_nulos
        if nuevos_nulos > 0:
            print(f"  [{col}] {nuevos_nulos} valor(es) no convertibles → NaN")
    return df


def guardar_clean(df: pd.DataFrame, nombre: str) -> Path:
    """Guarda el DataFrame limpio en data/clean/ como CSV UTF-8."""
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    ruta = CLEAN_DIR / f"{nombre}.csv"
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Guardado: {ruta} ({len(df)} filas)")
    return ruta


if __name__ == "__main__":
    periodo = "202312"
    print(f"Extrayendo colocaciones para {periodo}...")
    df_col = extraer_colocaciones(periodo)
    print(f"  {len(df_col)} registros obtenidos")
    guardar_clean(df_col, f"colocaciones_{periodo}")

    print(f"Extrayendo morosidad para {periodo}...")
    df_mor = extraer_morosidad(periodo)
    print(f"  {len(df_mor)} registros obtenidos")
    guardar_clean(df_mor, f"morosidad_{periodo}")
