# Pre-entrega 6 — Análisis meteorológico de Chile con DuckDB

> **Curso:** Data Science II — Machine Learning  
> **Módulo:** 6 — SQL y motores analíticos modernos  
> **Autor:** Dennys Parra  
> **Consigna:** [`consigna-pre-entrega6.md`](./consigna-pre-entrega6.md)

Análisis de temperaturas históricas de tres estaciones meteorológicas chilenas utilizando **DuckDB** y consultas SQL directamente sobre archivos CSV. El objetivo es comparar estaciones del norte, centro y sur de Chile sin crear una base de datos persistente.

## Resultado

El proyecto cumple los requisitos de la consigna:

- Utiliza DuckDB desde Python.
- Consulta directamente archivos CSV mediante una vista virtual.
- Maneja valores nulos de temperatura.
- Ejecuta cuatro consultas analíticas diferentes.
- Mide el tiempo de ejecución de cada consulta.
- No genera ni incluye archivos binarios de base de datos.

## Estructura

```text
pre-entrega6/
├── data/
│   ├── CI000085406.csv       # Arica
│   ├── CIM00085574.csv       # Santiago - Arturo Merino Benítez
│   └── CI000085934.csv       # Punta Arenas
├── outputs/                  # resultados CSV generados por main.py
├── src/
│   ├── __init__.py
│   └── analisis.py           # vista DuckDB y consultas SQL
├── main.py
├── requirements.txt
├── consigna-pre-entrega6.md
├── explicacion_general_modulo6.md
├── .gitignore
└── README.md
```

## Fuente de datos

Los archivos pertenecen al conjunto oficial **NOAA Global Historical Climatology Network Daily**:

- [Arica — CI000085406](https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/CI000085406.csv)
- [Santiago — CIM00085574](https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/CIM00085574.csv)
- [Punta Arenas — CI000085934](https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/CI000085934.csv)
- [Documentación general de NOAA](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily)

`TMAX` y `TMIN` están expresadas en décimas de grado Celsius. Por ejemplo, `300` representa `30,0 °C`; el script realiza la conversión dividiendo por 10.

## Instalación

Se requiere Python 3.10 o superior.

Desde la raíz `CODERHOUSE`:

```powershell
.\.venv\Scripts\activate
pip install -r "Data Science II/Modulo 6/pre-entrega6/requirements.txt"
```

También puede instalarse desde la carpeta de la entrega:

```powershell
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta `pre-entrega6`:

```powershell
python main.py
```

O desde la raíz `CODERHOUSE`:

```powershell
python "Data Science II/Modulo 6/pre-entrega6/main.py"
```

El script crea cuatro archivos CSV en `outputs/`:

| Archivo | Análisis |
|---|---|
| `01_calidad_datos.csv` | Registros, nulos y rango temporal por estación |
| `02_promedio_mensual.csv` | Promedio mensual de temperatura máxima |
| `03_maximos_historicos.csv` | Máximo histórico por estación y fecha |
| `04_dias_calidos.csv` | Días con temperatura máxima de 35 °C o más |

## Corrida de referencia

La ejecución local de referencia analizó **58.487 registros** de las tres estaciones en aproximadamente **0,64 segundos**. El tiempo puede variar según el equipo.

Hallazgos principales:

- Santiago registró el máximo histórico más alto: **39,3 °C**, el 27 de enero de 2019.
- Arica presentó un máximo histórico de **34,0 °C**.
- Punta Arenas presentó un máximo histórico de **27,0 °C**.
- Santiago fue la única estación del conjunto con registros de **35 °C o más**: 56 días.
- Los valores nulos se conservaron como faltantes y no se reemplazaron por cero.

Los resultados completos quedan disponibles en los cuatro archivos CSV de `outputs/`.

## Consultas implementadas

### 1. Calidad de datos

Cuenta los registros, identifica valores válidos y nulos de `TMAX` y `TMIN`, y obtiene el período disponible para cada estación.

### 2. Promedios mensuales

Agrupa por estación y mes para calcular el promedio de temperatura máxima. Los nulos se excluyen del promedio mediante el filtro `WHERE tmax_c IS NOT NULL`.

### 3. Máximos históricos

Obtiene el día con mayor temperatura máxima registrada en cada estación mediante `ROW_NUMBER()` y `QUALIFY`.

### 4. Días cálidos

Filtra registros con `TMAX >= 35 °C` y calcula la cantidad, el promedio y el máximo de esos días por estación.

## Decisiones de diseño

| Decisión | Motivo |
|---|---|
| DuckDB en memoria | Permite analizar los archivos sin crear una base persistente. |
| CSV locales | Facilitan la entrega y la reproducibilidad sin depender de una API. |
| `union_by_name = true` | Las estaciones no tienen exactamente las mismas columnas. |
| `TRY_CAST` | Evita que un valor vacío o inválido detenga todo el análisis. |
| Resultados en CSV | Permiten revisar los resultados sin agregar archivos binarios. |

## Checklist de la consigna

| Requisito | Cumplimiento |
|---|---|
| Script funcional con DuckDB | `main.py` y `src/analisis.py` |
| Al menos tres consultas analíticas | Cuatro consultas en `QUERY_DEFINITIONS` |
| README con instrucciones | Este archivo |
| Consulta directa sobre CSV/Parquet | Vista `weather_raw` con `read_csv_auto` |
| Sin base de datos binaria | Conexión `duckdb.connect(":memory:")` |
| Manejo de nulos en temperaturas | `TRY_CAST` y filtros `IS NOT NULL` |
| Promedios mensuales | `02_promedio_mensual.csv` |
| Máximos históricos por estación | `03_maximos_historicos.csv` |
