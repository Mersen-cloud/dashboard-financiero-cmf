# Dashboard de Indicadores Financieros — Sistema Bancario Chileno (CMF)

Dashboard interactivo en Power BI con datos oficiales de la Comisión para el Mercado Financiero (CMF) de Chile.
Proyecto de portafolio orientado a cargos de **Data Analyst** en banca y fintech.

---

## Preguntas de negocio que responde

| # | Pregunta | Indicador clave |
|---|----------|-----------------|
| 1 | ¿Qué bancos tienen mayor morosidad? | % cartera vencida / colocaciones |
| 2 | ¿Cómo se distribuye el mercado de créditos? | Participación por banco y segmento |
| 3 | ¿Qué tan rentables son los bancos? | ROE y ROA |
| 4 | ¿Cuánto crecieron las colocaciones en 12 meses? | Variación real anual por segmento |
| 5 | ¿Cómo comparan los bancos grandes vs. los de nicho? | Benchmarking multidimensional |

---

## Stack tecnológico

| Capa | Herramienta |
|------|-------------|
| Extracción y limpieza | Python (`requests`, `pandas`) |
| Almacenamiento | CSV en `data/clean/` |
| Visualización | Power BI Desktop |
| Métricas | Medidas DAX (morosidad %, ROE, ROA, crecimiento real) |

---

## Estructura del repositorio

```
dashboard-financiero-cmf/
├── data/
│   ├── raw/          # datos crudos de la API (no versionados)
│   └── clean/        # CSVs limpios que alimentan Power BI
├── notebooks/
│   └── 01_extraccion_cmf.ipynb   # extracción + limpieza documentada
├── src/
│   └── extraccion.py             # módulo reutilizable
├── dashboard/
│   └── dashboard.pbix            # entregable Power BI
├── .env.example                  # plantilla de variables de entorno
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar

### 1 · Clonar el repositorio

```bash
git clone https://github.com/Mersen-cloud/dashboard-financiero-cmf.git
cd dashboard-financiero-cmf
```

### 2 · Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 3 · Configurar la API Key

Obtén tu API Key gratuita en [api.cmfchile.cl](https://api.cmfchile.cl/), luego:

```bash
copy .env.example .env
# Edita .env y reemplaza tu_api_key_aqui con tu clave real
```

### 4 · Ejecutar la extracción

```bash
# Opción A: notebook documentado
jupyter notebook notebooks/01_extraccion_cmf.ipynb

# Opción B: script directo
python src/extraccion.py
```

Los archivos limpios quedarán en `data/clean/`.

### 5 · Abrir el dashboard

Abre `dashboard/dashboard.pbix` en Power BI Desktop. Si los datos no cargan automáticamente, actualiza la ruta de los CSV en la configuración de la fuente de datos.

---

## Hallazgos clave

> *Esta sección se completará con los hallazgos del análisis una vez procesados los datos.*

---

## Fuente de datos

- **API CMF Bancos**: [api.cmfchile.cl](https://api.cmfchile.cl/) — datos oficiales del sistema bancario chileno, acceso gratuito con registro.
- Los datos crudos (`data/raw/`) no se versionan; solo se versiona el código de extracción y los CSVs limpios.

---

*Autor: Diego León · [GitHub: Mersen-cloud](https://github.com/Mersen-cloud)*
