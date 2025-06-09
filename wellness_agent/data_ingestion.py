from pyspark.sql import SparkSession
import pandas as pd

# Initialize Spark session (if not already running)
spark = SparkSession.builder.getOrCreate()

CATALOG = 'dais-hackathon-2025'
SCHEMA = 'bright_initiative'


def list_catalogs():
    print("\nAvailable catalogs:")
    catalogs = [row.catalog for row in spark.sql("SHOW CATALOGS").collect()]
    print(catalogs)
    return catalogs


def list_schemas(catalog):
    print(f"\nAvailable schemas in catalog '{catalog}':")
    try:
        schemas = [row.databaseName for row in spark.sql(f"SHOW SCHEMAS IN `{catalog}`").collect()]
        print(schemas)
        if not schemas:
            print("No schemas found. You may not have permission to view schemas in this catalog.")
        return schemas
    except Exception as e:
        print(f"Error listing schemas in catalog '{catalog}': {e}")
        print("If you see a permissions error, ask your Databricks admin for USE CATALOG privileges on this catalog.")
        return []


def list_tables(catalog, schema):
    print(f"\nTables in `{catalog}`.`{schema}`:")
    try:
        tables = [row.tableName for row in spark.sql(f"SHOW TABLES IN `{catalog}`.`{schema}`").collect()]
        print(tables)
        return tables
    except Exception as e:
        print(f"  Could not list tables in schema '{schema}': {e}")
        return []


def describe_table(catalog, schema, table_name):
    full_table = f'`{catalog}`.`{schema}`.`{table_name}`'
    print(f"\n--- Table: {full_table} ---")
    try:
        df = spark.read.table(full_table)
        print(f"Columns and types for {table_name}:")
        for field in df.schema.fields:
            print(f"  {field.name}: {field.dataType}")
        print(f"\nSample rows from {table_name}:")
        df.show(10)
    except Exception as e:
        print(f"  ERROR: Could not load table '{table_name}': {e}")


def main():
    list_catalogs()
    schemas = list_schemas(CATALOG)
    if SCHEMA not in schemas:
        print(f"Schema '{SCHEMA}' not found in catalog '{CATALOG}'. Please update SCHEMA variable.")
        return
    tables = list_tables(CATALOG, SCHEMA)
    for table in tables:
        describe_table(CATALOG, SCHEMA, table)


if __name__ == "__main__":
    main() 