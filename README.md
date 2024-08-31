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
    - crear conectar service account. Add your service_account.json file in /reporting path
    - crear un sheets vacío, darle acceso al mail del service account
    - crear un data studio y conectarlo al sheets (hablar de caveats si se pierde la hoja)
    - duckdb / Docker Desktop
    - rename .env.example to .env and fill in your values

## Steps
- make build
- make run (generate data, save to duckdb, run dbt and export to sheets) -> container will keep running
- connect data studio to sheets

# if you want to query data

Uncomment line 45, 46, 47 and replace the command value with:

 ```sh
sh -c "python model_export.py && tail -f /dev/null
```
This will leave the container open so you can copy the files to query.

- make duckdb-files (if you want to query data)
- make duckdb (query duckdb)

```sql
 show tables; 
 select * from attribution limit 5;
````

- make clean (removes all generated files)

- To run in Github Actions, create your secrets for the .env file