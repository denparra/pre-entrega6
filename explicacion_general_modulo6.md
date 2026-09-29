# Explicación general — Pre-entrega 6

## ¿Qué se hizo?

Se construyó un análisis de temperaturas históricas de Chile utilizando DuckDB como motor de consultas. Se trabajó con tres estaciones meteorológicas:

- Arica, ubicada en el norte.
- Santiago, ubicada en la zona central.
- Punta Arenas, ubicada en el extremo sur.

La selección permite comparar comportamientos térmicos de distintas zonas del país sobre una serie temporal real.

## ¿Por qué se utilizó DuckDB?

En los módulos anteriores se utilizaron herramientas de Python para adquirir, limpiar y transformar datos. En esta entrega el objetivo cambia: se busca consultar archivos directamente con SQL, sin crear una base de datos tradicional.

DuckDB es apropiado porque funciona dentro del proceso de Python, lee archivos CSV directamente, permite crear vistas virtuales y resuelve agregaciones y filtros con SQL.

## Relación con los módulos anteriores

### Módulo 2: adquisición y normalización

Se mantiene el trabajo con fuentes externas y datos reales, pero la lectura y la normalización se realizan dentro de DuckDB.

### Módulo 5: pipeline y organización

Se conserva la separación entre ejecución y lógica:

- `main.py` coordina la ejecución.
- `src/analisis.py` contiene la lógica de DuckDB y las consultas.
- `data/` contiene las fuentes.
- `outputs/` contiene resultados tabulares.

## ¿Cómo se prepara el dataset?

Los CSV de NOAA tienen columnas como `STATION`, `DATE`, `NAME`, `TMAX` y `TMIN`. Antes de analizar:

1. Se leen los tres archivos con `read_csv_auto`.
2. Se unifican las columnas con `union_by_name = true`.
3. Se convierten las fechas mediante `TRY_CAST`.
4. Se convierten `TMAX` y `TMIN` de décimas de grado a grados Celsius.
5. Los valores nulos se conservan y se excluyen únicamente de los cálculos que necesitan una temperatura válida.

No reemplazar un dato faltante por cero es importante: cero grados representa una temperatura real, mientras que un valor nulo significa que la estación no informó esa medición.

## ¿Qué preguntas responde el análisis?

### Calidad de datos

¿Cuántos registros tiene cada estación? ¿Qué período cubre? ¿Cuántas temperaturas faltan?

### Comportamiento mensual

¿Cuál es la temperatura máxima promedio de cada mes en cada estación?

### Extremos históricos

¿Cuál fue la mayor temperatura máxima registrada en cada estación y en qué fecha ocurrió?

### Días cálidos

¿Qué estación acumuló más días con temperaturas máximas iguales o superiores a 35 °C?

## Decisiones importantes

### No se creó una base de datos persistente

La consigna solicita aprovechar DuckDB como motor embebido y consultar los archivos directamente. Por eso se utiliza una conexión en memoria:

```python
duckdb.connect(":memory:")
```

Esto evita agregar archivos `.db` o `.duckdb` al proyecto.

### Se generan resultados CSV

Los resultados se guardan como CSV porque son fáciles de inspeccionar, compartir y versionar. No son una base de datos ni reemplazan a los archivos fuente.

## Procedencia y referencias

Los datos meteorológicos provienen de NOAA Global Historical Climatology Network Daily. La fuente, las estaciones utilizadas y sus enlaces oficiales están documentados en el `README.md`.

La referencia a NOAA es necesaria para reconocer el origen de los datos; no se presenta como autoría del proyecto.

## Conclusión

La entrega demuestra el flujo completo del módulo: fuente meteorológica pública, lectura directa de archivos, limpieza básica, consultas SQL analíticas, medición del tiempo de ejecución y documentación reproducible.
