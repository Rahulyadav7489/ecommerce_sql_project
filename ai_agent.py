import os
from google import genai
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv("API")
client = genai.Client(api_key=api_key)

def nlp_to_sql(question, schema):
    prompt = f"""
You are an expert data analyst.
Given the database schema below, convert the question into a valid PostgreSQL SQL query.

Schema:
{schema}

Question:
{question}

Return ONLY the SQL query, no explanations.
"""
    response = client.generate_content(
        model="gemini-2.0-flash",
        prompt=prompt
    )
    sql_query = response.text.strip().replace("sql:", "").strip("` ")
    return sql_query

def summarize_results(question, df):
    if isinstance(df, str):
        # error case
        return df
    table_md = df.to_markdown(index=False)
    prompt = f"""
You are a helpful business data assistant.
The user asked: {question}

Here are the query results in markdown table format:
{table_md}

Write a clear, professional summary in simple English highlighting key findings, trends, or totals.
Avoid SQL jargon.
"""
    response = client.generate_content(
        model="gemini-2.0-flash",
        prompt=prompt
    )
    return response.text.strip()
