"""Pre-entrega 6 — análisis meteorológico con DuckDB.

Ejecuta las consultas analíticas definidas en ``src/analisis.py`` sobre los
archivos CSV de NOAA almacenados en ``data/``.
"""

from pathlib import Path

from src.analisis import ejecutar_analisis


BASE = Path(__file__).resolve().parent


def main() -> None:
    """Ejecuta el análisis completo y muestra un resumen en consola."""

    resumen = ejecutar_analisis(BASE)

    print("\n" + "=" * 72)
    print(" PRE-ENTREGA 6 — ANÁLISIS METEOROLÓGICO CON DUCKDB")
    print("=" * 72)
    print(f"Archivos consultados: {resumen['archivos']}")
    print(f"Registros analizados: {resumen['registros']:,}")
    print(f"Estaciones: {', '.join(resumen['estaciones'])}")
    print(f"Tiempo total: {resumen['tiempo_total']:.4f} segundos")
    print(f"Resultados: {BASE / 'outputs'}")
    print("ANÁLISIS COMPLETADO [OK]\n")


if __name__ == "__main__":
    main()
