# Guía de construcción del dashboard

Pasos para construir `dashboard.pbix` en Power BI Desktop a partir de los CSV de `data/clean/`.

---

## 1 · Carga de datos

1. **Obtener datos → Texto/CSV** y cargar los 8 archivos de `data/clean/`:
   `uf.csv`, `dolar.csv`, `euro.csv`, `ipc.csv`, `utm.csv`, `tip.csv`, `tmc.csv`, `calendario.csv`
2. En Power Query, verificar por cada tabla:
   - `fecha` con tipo **Fecha** (no Fecha/Hora)
   - `valor` con tipo **Número decimal**
   - Los CSV usan punto decimal: si la configuración regional causa problemas,
     usar *Cambiar tipo → Usando configuración regional → Inglés (Estados Unidos)*
3. Cerrar y aplicar.

## 2 · Modelo de datos

1. Vista de modelo: crear relaciones **uno a varios** desde `calendario[fecha]` hacia
   `fecha` de cada tabla de indicadores.
2. Marcar `calendario` como **tabla de fechas**.
3. Ocultar de la vista de informe las columnas `fecha` de las tablas de hechos
   (se usa siempre la del calendario).
4. Crear la tabla `_Medidas` y agregar las medidas de [medidas_dax.md](medidas_dax.md).

## 3 · Páginas del dashboard

### Página 1 · Resumen Ejecutivo
- **4 tarjetas KPI** arriba: Dólar Último + Var% 12m, UF Última, IPC 12m (compuesto), TIP Promedio (consumo)
- **Gráfico de líneas** central: dólar diario 2020–2026 con promedio móvil 30d
- **Gráfico de columnas** pequeño: IPC mensual último año
- Segmentador de año en la esquina superior derecha

### Página 2 · Inflación
- **Columnas**: IPC mensual completo 2020–2026 (destacar visualmente el peak de 2022)
- **Línea**: IPC acumulado por año (una línea por año o con segmentador)
- **Línea**: evolución UF vs eje secundario con IPC 12m — muestra cómo la UF sigue a la inflación con rezago
- **Tarjetas**: IPC acumulado del año actual, IPC 12m, mes con mayor IPC histórico

### Página 3 · Tipo de Cambio
- **Líneas**: USD/CLP y EUR/CLP en el mismo gráfico
- **Tarjetas**: valor actual, máximo histórico, mínimo histórico, depreciación acumulada desde 2020
- **Columnas**: variación % anual del dólar por año

### Página 4 · Tasas de Interés
- **Líneas**: TIP promedio por segmento en el tiempo (segmentador por `Titulo`)
- **Líneas**: TMC por segmento
- **Tabla o matriz**: última TMC vigente por tipo de operación
- Nota informativa: la TMC es el techo legal de tasas — relevante para riesgo crediticio

## 4 · Diseño

- Tema: fondo claro, un color principal (azul corporativo `#1F4E79` sugerido) + gris
- Títulos de página consistentes, misma tipografía (Segoe UI)
- Formato español de Chile: separador de miles con punto (configurar en
  Archivo → Opciones → Configuración regional)

## 5 · Al terminar

1. Guardar como `dashboard/dashboard.pbix`
2. Exportar capturas de cada página (para el README)
3. Completar la sección **Hallazgos clave** del README con 3–4 números concretos, por ejemplo:
   - Inflación acumulada 2022 vs promedio histórico
   - Depreciación del CLP frente al dólar 2020–2026
   - Diferencia entre TMC de consumo vs comercial
4. Commit del `.pbix` (sí se versiona: es el entregable del portafolio)
