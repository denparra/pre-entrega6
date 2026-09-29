"""Consultas DuckDB para el análisis de estaciones meteorológicas chilenas."""

from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Any

import duckdb


QUERY_DEFINITIONS = {
    "01_calidad_datos": """
        SELECT
            station,
            name,
            COUNT(*) AS total_registros,
            COUNT(tmax_c) AS tmax_validas,
            COUNT(*) - COUNT(tmax_c) AS tmax_nulas,
            COUNT(tmin_c) AS tmin_validas,
            COUNT(*) - COUNT(tmin_c) AS tmin_nulas,
            MIN(observation_date) AS fecha_inicio,
            MAX(observation_date) AS fecha_fin
        FROM weather_clean
        GROUP BY station, name
        ORDER BY station
    """,
    "02_promedio_mensual": """
        SELECT
            station,
            name,
            EXTRACT(MONTH FROM observation_date)::INTEGER AS mes,
            ROUND(AVG(tmax_c), 2) AS promedio_tmax_c,
            COUNT(*) AS dias_con_tmax
        FROM weather_clean
        WHERE tmax_c IS NOT NULL
        GROUP BY station, name, mes
        ORDER BY station, mes
    """,
    "03_maximos_historicos": """
        SELECT
            station,
            name,
            observation_date AS fecha_maxima,
            ROUND(tmax_c, 1) AS tmax_maxima_c
        FROM weather_clean
        WHERE tmax_c IS NOT NULL
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY station
            ORDER BY tmax_c DESC, observation_date
        ) = 1
        ORDER BY tmax_maxima_c DESC
    """,
    "04_dias_calidos": """
        SELECT
            station,
            name,
            COUNT(*) AS dias_con_35_grados_o_mas,
            ROUND(AVG(tmax_c), 2) AS promedio_dias_calidos_c,
            ROUND(MAX(tmax_c), 1) AS maximo_tmax_c
        FROM weather_clean
        WHERE tmax_c >= 35
        GROUP BY station, name
        ORDER BY dias_con_35_grados_o_mas DESC
    """,
}


def _sql_paths(paths: list[Path]) -> str:
    """Devuelve una lista de rutas segura para usar en una expresión SQL."""

    return ", ".join("'{}'".format(str(path).replace("'", "''")) for path in paths)


def _crear_vista_clima(connection: duckdb.DuckDBPyConnection, paths: list[Path]) -> None:
    """Registra los CSV como una vista virtual y normaliza temperaturas."""

    files = _sql_paths(paths)

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW weather_raw AS
        SELECT *
        FROM read_csv_auto(
            [{files}],
            union_by_name = true,
            filename = true
        )
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE VIEW weather_clean AS
        SELECT
            station,
            name,
            TRY_CAST(date AS DATE) AS observation_date,
            TRY_CAST(tmax AS DOUBLE) / 10.0 AS tmax_c,
            TRY_CAST(tmin AS DOUBLE) / 10.0 AS tmin_c
        FROM weather_raw
        WHERE TRY_CAST(date AS DATE) IS NOT NULL
        """
    )


def _guardar_csv(path: Path, columns: list[str], rows: list[tuple[Any, ...]]) -> None:
    """Guarda el resultado tabular sin crear una base de datos persistente."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(rows)


def _ejecutar_consulta(
    connection: duckdb.DuckDBPyConnection,
    nombre: str,
    sql: str,
    output_dir: Path,
) -> dict[str, Any]:
    """Ejecuta una consulta, mide su duración y exporta sus filas a CSV."""

    started_at = time.perf_counter()
    result = connection.execute(sql)
    columns = [column[0] for column in result.description]
    rows = result.fetchall()
    elapsed = time.perf_counter() - started_at

    _guardar_csv(output_dir / f"{nombre}.csv", columns, rows)

    return {
        "nombre": nombre,
        "columnas": columns,
        "filas": rows,
        "tiempo": elapsed,
    }


def ejecutar_analisis(base: Path) -> dict[str, Any]:
    """Ejecuta las consultas sobre los CSV y devuelve un resumen verificable."""

    data_dir = base / "data"
    output_dir = base / "outputs"
    paths = sorted(data_dir.glob("*.csv"))

    if not paths:
        raise FileNotFoundError(f"No se encontraron archivos CSV en {data_dir}")

    started_at = time.perf_counter()

    with duckdb.connect(":memory:") as connection:
        _crear_vista_clima(connection, paths)
        total_records = connection.execute("SELECT COUNT(*) FROM weather_clean").fetchone()[0]
        stations = [
            row[0]
            for row in connection.execute(
                "SELECT DISTINCT station FROM weather_clean ORDER BY station"
            ).fetchall()
        ]

        results = [
            _ejecutar_consulta(connection, name, query, output_dir)
            for name, query in QUERY_DEFINITIONS.items()
        ]

    return {
        "archivos": len(paths),
        "registros": total_records,
        "estaciones": stations,
        "tiempo_total": time.perf_counter() - started_at,
        "consultas": results,
    }
