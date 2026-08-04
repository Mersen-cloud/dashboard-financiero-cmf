# Medidas DAX del dashboard

Todas las medidas van en una tabla dedicada `_Medidas` (Inicio → Especificar datos → crear tabla vacía llamada `_Medidas`), para mantener el modelo ordenado.

**Prerequisito:** relaciones `calendario[fecha]` 1→* contra `fecha` de cada tabla de indicadores (uf, dolar, euro, ipc, utm, tip, tmc). Marcar `calendario` como tabla de fechas (Herramientas de tabla → Marcar como tabla de fechas).

---

## Tipo de cambio

```dax
Dólar Último =
VAR UltimaFecha = CALCULATE ( MAX ( dolar[fecha] ) )
RETURN
    CALCULATE ( AVERAGE ( dolar[valor] ), dolar[fecha] = UltimaFecha )
```

```dax
Dólar Var% 12m =
VAR Actual = [Dólar Último]
VAR Previo =
    CALCULATE ( [Dólar Último], DATEADD ( calendario[fecha], -12, MONTH ) )
RETURN
    DIVIDE ( Actual - Previo, Previo )
```

```dax
Dólar Promedio Móvil 30d =
AVERAGEX (
    DATESINPERIOD ( calendario[fecha], LASTDATE ( calendario[fecha] ), -30, DAY ),
    CALCULATE ( AVERAGE ( dolar[valor] ) )
)
```

```dax
Dólar Depreciación desde 2020 =
VAR Base =
    CALCULATE (
        [Dólar Último],
        REMOVEFILTERS ( calendario ),
        calendario[anio_mes] = "2020-01"
    )
RETURN
    DIVIDE ( [Dólar Último] - Base, Base )
```

Para el euro, duplicar las cuatro medidas cambiando `dolar` → `euro`.

---

## Inflación

```dax
IPC Mensual =
SUM ( ipc[valor] )
```

```dax
IPC Acumulado Año =
TOTALYTD ( SUM ( ipc[valor] ), calendario[fecha] )
```

```dax
IPC 12m (compuesto) =
VAR Meses =
    CALCULATETABLE (
        VALUES ( calendario[anio_mes] ),
        DATESINPERIOD ( calendario[fecha], MAX ( calendario[fecha] ), -12, MONTH )
    )
RETURN
    PRODUCTX ( Meses, 1 + CALCULATE ( SUM ( ipc[valor] ) ) / 100 ) - 1
```

> **Nota metodológica:** la inflación anual correcta se compone multiplicativamente
> (`Π(1+m)−1`), no sumando los IPC mensuales. La diferencia es relevante en años de
> alta inflación como 2022. Este detalle es un buen punto a mencionar en entrevistas.

---

## UF

```dax
UF Última =
VAR UltimaFecha = CALCULATE ( MAX ( uf[fecha] ) )
RETURN
    CALCULATE ( AVERAGE ( uf[valor] ), uf[fecha] = UltimaFecha )
```

```dax
UF Var% 12m =
VAR Actual = [UF Última]
VAR Previo =
    CALCULATE ( [UF Última], DATEADD ( calendario[fecha], -12, MONTH ) )
RETURN
    DIVIDE ( Actual - Previo, Previo )
```

---

## Tasas de interés

```dax
TIP Promedio =
AVERAGE ( tip[valor] )
```

```dax
TMC Promedio =
AVERAGE ( tmc[valor] )
```

Estas dos se usan junto con el filtro de segmento (columna `Titulo`/`SubTitulo`) en segmentadores de página.

---

## Formatos recomendados

| Medida | Formato |
|--------|---------|
| Dólar/Euro/UF valores | `#,##0` (sin decimales) o `#,##0.00` |
| Variaciones % | Porcentaje, 1 decimal |
| IPC | Porcentaje o número con 1 decimal según visual |
