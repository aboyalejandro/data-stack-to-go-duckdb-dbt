# Intro

A portable data-stack with:
- Custom Python ETL
- DuckDB for OLAP
- dbt for transformations
- Google Sheets for Warehouse
- Data Studio for Visualization

# Draft 
- requisites
    - cuenta demo de piwikpro
    - crear conectar service account
    - crear un sheets vacío, darle acceso al mail del service account
    - crear un data studio y conectarlo al sheets (hablar de caveats si se pierde la hoja)
    - duckdb / Docker Desktop

## Steps
- make build
- make run (generate data, save to duckdb, run dbt and export to sheets) -> container will keep running
- connect data studio to sheets
- make duckdb-files (if you want to query data)
- make duckdb (query duckdb)

```sql
 show tables; 
 select * from attribution limit 5;
````

- make clean (removes all generated files)

- To run in Github Actions, create secrets