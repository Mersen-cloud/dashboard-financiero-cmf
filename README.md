# Dashboard de Indicadores Macroeconómicos Chile (CMF)

Dashboard interactivo en Power BI con datos oficiales de la Comisión para el Mercado Financiero (CMF) de Chile.
Proyecto de portafolio orientado a cargos de **Data Analyst** en banca y fintech.

---

## Preguntas de negocio que responde

| # | Pregunta | Indicador |
|---|----------|-----------|
| 1 | ¿Cómo evolucionó la inflación en Chile (2020–2026)? | IPC mensual y acumulado anual |
| 2 | ¿Qué tan volátil ha sido el tipo de cambio? | USD/CLP y EUR/CLP diarios |
| 3 | ¿Cómo se relacionan la UF y el IPC? | Correlación UF vs inflación |
| 4 | ¿Cómo han variado las tasas de crédito? | TIP y TMC por segmento |
| 5 | ¿Cuánto ha perdido el peso frente al dólar en 5 años? | Depreciación acumulada |

---

## Stack tecnológico

| Capa | Herramienta |
|------|-------------|
| Extracción y limpieza | Python (`requests`, `pandas`) |
| Almacenamiento | CSV en `data/clean/` |
| Visualización | Power BI Desktop |
| Fuente de datos | API CMF Chile (`api.cmfchile.cl`) |

---

## Datos extraídos

| Archivo | Descripción | Frecuencia | Filas |
|---------|-------------|-----------|-------|
| `uf.csv` | Unidad de Fomento | Diaria | ~2.400 |
| `dolar.csv` | Tipo de cambio USD/CLP | Hábil diaria | ~1.600 |
| `euro.csv` | Tipo de cambio EUR/CLP | Hábil diaria | ~1.600 |
| `ipc.csv` | Índice de Precios al Consumidor | Mensual | ~78 |
| `utm.csv` | Unidad Tributaria Mensual | Mensual | ~80 |
| `tip.csv` | Tasa de Interés Promedio por segmento | Mensual | ~960 |
| `tmc.csv` | Tasa Máxima Convencional por segmento | Mensual | ~950 |

Período cubierto: **enero 2020 – agosto 2026**

---

## Estructura del repositorio

```
dashboard-financiero-cmf/
├── data/
│   ├── raw/          # JSON crudos de la API (no versionados)
│   └── clean/        # CSVs limpios para Power BI
├── notebooks/
│   └── 01_extraccion_cmf.ipynb   # extracción + limpieza documentada
├── src/
│   └── extraccion.py             # módulo reutilizable de extracción
├── dashboard/
│   └── dashboard.pbix            # entregable Power BI
├── .env.example                  # plantilla de API Key
├── requirements.txt
└── README.md
```

---

## Cómo reproducir

### 1 · Clonar el repositorio

```bash
git clone https://github.com/Mersen-cloud/dashboard-financiero-cmf.git
cd dashboard-financiero-cmf
```

### 2 · Entorno virtual e instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3 · Configurar API Key

Obtén tu clave gratuita en [api.cmfchile.cl](https://api.cmfchile.cl/) y crea el archivo `.env`:

```bash
copy .env.example .env
# Edita .env y reemplaza tu_api_key_aqui
```

### 4 · Ejecutar la extracción

```bash
python src/extraccion.py
```

Los archivos limpios quedan en `data/clean/` listos para cargar en Power BI.

---

## Hallazgos clave

> *Sección por completar con los hallazgos del análisis una vez finalizado el dashboard.*

---

## Fuente de datos

- **API CMF Chile**: [api.cmfchile.cl](https://api.cmfchile.cl/) — datos oficiales, acceso gratuito con registro.
- Los JSON crudos (`data/raw/`) no se versionan; solo el código y los CSVs limpios.

---

*Autor: Diego León · [GitHub: Mersen-cloud](https://github.com/Mersen-cloud)*
