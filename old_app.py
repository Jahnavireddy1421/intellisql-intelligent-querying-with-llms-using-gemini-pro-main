import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (your API key)
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from Gemini Pro
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    # We pass both the prompt (instructions) and the user question
    response = model.generate_content([prompt[0], question])
    return response.text

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database is named STUDENT and has the following columns - NAME, CLASS, 
    SECTION, and MARKS.
    
    Example 1 - How many records are there?, 
    the SQL command will be: SELECT COUNT(*) FROM STUDENT;
    
    Example 2 - Tell me all the students in Data Science?, 
    the SQL command will be: SELECT * FROM STUDENT WHERE CLASS='Data Science';
    
    Your output must be a raw SQL query. Do not include '```' or the word 'sql' in the output.
    """
]
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# --- Updated Streamlit UI with Form ---
st.set_page_config(page_title="IntelliSQL - Text to SQL")
st.header("IntelliSQL: Query your DB with Gemini Pro")

# Wrap everything in a form
with st.form("query_form"):
    question = st.text_input("Input: ", key="input", placeholder="e.g., How many students are in Data Science?")
    
    # This button now handles both clicks AND the "Enter" key
    submit = st.form_submit_button("Generate & Run Query")

if submit:
    if question:
        response_sql = get_gemini_response(question, prompt)
        st.code(response_sql, language='sql')
        
        data = read_sql_query(response_sql, "data.db")
        
        st.subheader("The Result is:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.info("No records found.")
    else:
        st.warning("Please enter a question first!")