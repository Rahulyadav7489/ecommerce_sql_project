import streamlit as st
from db_utils import get_table_schema, execute_query
from ai_agent import nlp_to_sql, summarize_results

st.title("Business Data NLP Query and Power BI Dashboard")

st.write("Enter your business question (e.g. 'What is the total revenue by gender?'):")

schema = get_table_schema()

user_question = st.text_input("Your Question")

if st.button("Run Query"):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        st.info("Generating SQL query...")
        sql = nlp_to_sql(user_question, schema)
        st.code(sql, language="sql")
        st.info("Executing SQL on the database...")
        result = execute_query(sql)

        if hasattr(result, "shape"):  # it's a dataframe
            st.dataframe(result)
            st.info("Generating summary...")
            summary = summarize_results(user_question, result)
            st.write("### Summary:")
            st.write(summary)
        else:
            st.error(result)

# Embed Power BI dashboard iframe (replace with your actual URL)
powerbi_embed_url = "https://app.powerbi.com/view?r=YOUR_EMBED_URL_HERE"

st.write("---")
st.write("## Power BI Dashboard View")
st.markdown(f'<iframe width="100%" height="600" src="{powerbi_embed_url}" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
