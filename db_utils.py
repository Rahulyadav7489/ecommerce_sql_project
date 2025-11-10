import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("URI")
engine = create_engine(uri)

def get_table_schema():
    schema_info = ""
    with engine.connect() as conn:
        tables = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")).fetchall()
        for (tablename,) in tables:
            cols = conn.execute(text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{tablename}';
            """)).fetchall()
            col_list = ", ".join(c[0] for c in cols)
            schema_info += f"Table {tablename} with columns: {col_list}\n"
    return schema_info

def execute_query(sql):
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        return f"SQL Execution Error: {e}"
