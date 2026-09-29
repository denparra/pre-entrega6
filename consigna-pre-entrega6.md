# Pre-entrega: Análisis de Datos Meteorológicos con DuckDB y SQL

> Pre-entrega: Análisis de Datos Meteorológicos con DuckDB e SQL

## Objetivo

El objetivo de este entregable es consolidar el uso de DuckDB como motor analítico de alto rendimiento para procesar datos externos de manera eficiente. Aprenderás a realizar consultas SQL directamente sobre archivos de datos sin necesidad de una base de datos tradicional pesada.

## Criterios de la entrega

Respondé las siguientes preguntas:

1. **El repositorio contiene un script funcional que utiliza la librería de DuckDB.**
2. **El código realiza al menos tres consultas analíticas diferentes** (promedios, conteos, filtrados complejos).
3. **Se incluye un archivo README.md** con instrucciones claras para replicar el análisis.
4. **La consulta de datos se realiza directamente sobre archivos** (CSV o Parquet) aprovechando las capacidades de DuckDB.
5. **No se incluyen archivos binarios de la base de datos**, priorizando el enfoque de motor embebido.

## Repositorio y entregable

Repositorio de GitHub que contenga el script de análisis en SQL/Python usando DuckDB y un README con los resultados del análisis.

## Entregable

## Propósito
Configurar un entorno analítico ligero y ejecutar consultas SQL complejas para extraer insights de un dataset de serie temporal (clima), demostrando la velocidad y simplicidad de DuckDB.

## Pasos sugeridos
### 1. Preparación del entorno

Preparación del Entorno: Crea un nuevo repositorio en GitHub para este proyecto.
### 2. Obtención de datos

Obtención de datos: Descarga o referencia via URL un dataset en formato CSV o Parquet (puedes usar datasets públicos de clima de NOAA o similares).
### 3. Implementación de scripts

Implementación de Scripts: Escribe un script de Python o un archivo SQL que realice lo siguiente mediante DuckDB:
Carga y registro del archivo como una tabla virtual.
Limpieza básica (manejo de nulos en temperaturas).
Análisis agregados (promedios mensuales, máximos históricos por estación).
### 4. Documentación

Documentación: Crea un archivo README.md que explique cómo ejecutar el análisis y cuáles fueron los tiempos de respuesta o hallazgos principales.
## Errores comunes
Intentar cargar el archivo en una base de datos SQL tradicional (como MySQL) en lugar de consultar directamente el archivo con DuckDB.
No documentar las dependencias necesarias en un archivo requirements.txt.
