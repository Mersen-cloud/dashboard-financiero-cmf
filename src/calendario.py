"""
Genera la tabla calendario (dimensión de fechas) para el modelo de datos
de Power BI. Cubre el mismo rango que los indicadores extraídos.
"""

import pandas as pd
from pathlib import Path

CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean"

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def generar_calendario(inicio: str = "2020-01-01", fin: str = "2026-12-31") -> pd.DataFrame:
    fechas = pd.date_range(inicio, fin, freq="D")
    df = pd.DataFrame({"fecha": fechas})
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["nombre_mes"] = df["mes"].apply(lambda m: MESES[m - 1])
    df["trimestre"] = "T" + df["fecha"].dt.quarter.astype(str)
    df["anio_mes"] = df["fecha"].dt.strftime("%Y-%m")
    return df


if __name__ == "__main__":
    df = generar_calendario()
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    ruta = CLEAN_DIR / "calendario.csv"
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Guardado: {ruta}  ({len(df)} filas)")
