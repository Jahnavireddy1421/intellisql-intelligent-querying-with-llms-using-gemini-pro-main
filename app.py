import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Backend Logic ---
def get_response(question, prompt):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content([prompt, question])
    
    # Clean the response text to remove markdown formatting
    cleaned_sql = response.text.strip()
    cleaned_sql = cleaned_sql.replace("```sql", "").replace("```", "").replace("sql", "")
    
    # Handle the "undefined" error if Gemini adds it
    cleaned_sql = cleaned_sql.replace("undefined", "").strip()
    
    return cleaned_sql

def read_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# --- Page 1: Home ---
def page_home():
    st.markdown("""
        <style>
        body { background-color: #2E2E2E; }
        .main-title { text-align: center; color: #4CAF50; font-size: 2.5em; }
        .sub-title { text-align: center; color: #4CAF50; font-size: 1.5em; }
        .offerings { padding: 20px; color: white; }
        .offerings h2 { color: #4CAF50; }
        .offerings ul { list-style-type: none; padding: 0; }
        .offerings li { margin: 10px 0; font-size: 18px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-title'>Welcome to IntelliSQL!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Revolutionizing Database Querying with Advanced LLM Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Link from your instruction screenshot (image_1a3642.png)
        st.image("https://cdn1.iconfinder.com/data/icons/business-dual-color-glyph-set-3/128/Data_warehouse-1024.png", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class='offerings'>
            <h2>Wide Range of Offerings</h2>
            <ul>
                <li>💡 Intelligent Query Assistance</li>
                <li>🔍 Data Exploration and Insights</li>
                <li>📦 Efficient Data Retrieval</li>
                <li>🚀 Performance Optimization</li>
                <li>🔧 Syntax Suggestions</li>
                <li>📈 Trend Analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- Page 2: About ---
def page_about():
    st.markdown("<style>.content { color: white; }</style>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #4CAF50;'>About IntelliSQL</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.markdown("<h2>IntelliSQL is an innovative project aimed at revolutionizing database querying using advanced Language Model capabilities.</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Link from your instruction screenshot (image_1a3660.png)
    st.image("https://download.logo.wine/logo/Oracle_SQL_Developer/Oracle_SQL_Developer-Logo.wine.png", use_container_width=True)

# --- Page 3: Intelligent Query Assistance ---
def page_intelligent_query_assistance():
    st.markdown("""
        <style>
        .tool-input { margin-bottom: 20px; color: white; }
        .response { margin-top: 20px; color: white; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='color: #4CAF50;'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)
    st.write("IntelliSQL enhances the querying process by providing intelligent assistance to users.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = "You are an expert in converting English questions to SQL query! The database is STUDENT with columns: NAME, CLASS, SECTION, MARKS. Provide only the SQL code."
        
        st.markdown("<div class='tool-input'>", unsafe_allow_html=True)
        que = st.text_input("Enter Your Query:", key="sql_query")
        submit = st.button("Get Answer", key="submit_button", help="click to retrieve the SQL data")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit or que:
            try:
                response = get_response(que, prompt)
                st.write(f"**Generated SQL Query:** `{response}`")
                
                data = read_query(response, "data.db")
                st.markdown("<div class='response'>", unsafe_allow_html=True)
                st.subheader("The Response is:")
                st.table(data)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
    with col2:
        # Link from your instruction screenshot (image_1a3685.png)
        st.image("https://cdn-icons-png.flaticon.com/512/9850/9850877.png", use_container_width=True)

# --- Main Function ---
def main():
    st.set_page_config(page_title="IntelliSQL", page_icon="🌟", layout="wide")
    
    st.sidebar.title("Navigation")
    # Custom sidebar styling from image_1a36a5.png
    st.sidebar.markdown("<style>.sidebar .sidebar-content {background-color: #2E2E2E; color: white;}</style>", unsafe_allow_html=True)
    
    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()