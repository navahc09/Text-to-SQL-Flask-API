import streamlit as st
import requests
import pandas as pd

API_URL = "https://conversational-text-to-sql-agent.onrender.com/query"

st.set_page_config(page_title="Text-to-SQL Agent", page_icon="📊", layout="wide")

st.title("Conversational Text-to-SQL Agent")
st.markdown("""
**An LLM-powered orchestration pipeline that translates natural language into secure, executable SQL queries, and returns the results with a summary.** Ask questions about the sample music store database (Chinook). The agent will generate the SQL, pass it through a strict read-only sanitization layer, execute it, and visualize the results. 
(Note: The chat may get stuck at "Generating SQL" if the backend service has gone idle due to inactivity (Render's free-tier policy). If this happens, refresh the page and enter your question again.) 
""")
st.divider()

# Schema
schema = {
    "Artist": ["ArtistId", "Name"],
    "Album": ["AlbumId", "Title", "ArtistId"],
    "Track": ["TrackId", "Name", "AlbumId", "GenreId", "Milliseconds", "UnitPrice"],
    "Customer": ["CustomerId", "FirstName", "LastName", "Country"],
    "Invoice": ["InvoiceId", "CustomerId", "InvoiceDate", "Total"],
    "InvoiceLine": ["InvoiceLineId", "InvoiceId", "TrackId", "UnitPrice", "Quantity"],
    "Genre": ["GenreId", "Name"],
    "Playlist": ["PlaylistId", "Name"]
}

# Session State
# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "type": "text", 
            "content": "**Welcome!** I am your Text-to-SQL agent. \n\nYou can ask me questions about tracks, artists, invoices, and customers. Try clicking one of the **Example Questions** in the sidebar to see how the multi-stage pipeline works!"
        }
    ]

# Sidebar Schema Viewer
st.sidebar.title("Database Schema")

for table, cols in schema.items():
    with st.sidebar.expander(table):
        for c in cols:
            st.write(c)

# Example Questions
st.sidebar.markdown("---")
st.sidebar.markdown("### Try an Example")

examples = [
    "Top 10 most expensive tracks",
    "How many invoices are there in total?",
    "How many songs does artist with id 1 have?",
]

for q in examples:
    if st.sidebar.button(q, width='stretch'):
        st.session_state.pending_question = q

# Display Chat History
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["type"] == "text":
            st.write(msg["content"])

        elif msg["type"] == "sql":
            st.code(msg["content"], language="sql")

        elif msg["type"] == "table":

            df = msg["content"]

            st.dataframe(df, width='stretch')

            if isinstance(df, pd.DataFrame) and len(df.columns) == 2:

                if pd.api.types.is_numeric_dtype(df[df.columns[1]]):

                    st.subheader("Visualization")
                    st.bar_chart(df)

# Chat Input
question = st.chat_input("Ask a question about the database...")

# example question trigger
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question

# Query Execution
if question:

    # show user message
    st.chat_message("user").write(question)

    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": question
    })

    with st.spinner("Generating SQL and querying database..."):

        try:

            response = requests.post(
                API_URL,
                json={"question": question}
            )

            if response.status_code == 200:

                data = response.json()

                # SQL
                if "generated_sql" in data:

                    sql = data["generated_sql"]

                    with st.chat_message("assistant"):
                        st.code(sql, language="sql")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "sql",
                        "content": sql
                    })

                # summary
                summary = data.get("summary", "")

                with st.chat_message("assistant"):
                    st.write(summary)

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "text",
                    "content": summary
                })

                # dataframe
                df = pd.DataFrame(
                    data.get("database_query_result", []),
                    columns=data.get("columns")
                )

                with st.chat_message("assistant"):

                    st.dataframe(df, width='stretch')

                    if isinstance(df, pd.DataFrame) and len(df.columns) == 2:

                        if pd.api.types.is_numeric_dtype(df[df.columns[1]]):

                            st.subheader("Visualization")
                            st.bar_chart(df)

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "table",
                    "content": df
                })

                # debug viewer
                with st.expander("Raw API Response"):
                    st.json(data)

            else:

                try:
                    error_data = response.json()
                    st.error(error_data.get("error", "Unknown API error"))
                except:
                    st.error(f"Server returned error: {response.status_code}")
                    st.text(response.text)

        except requests.exceptions.RequestException as e:

            st.error("Could not connect to API.")
            st.text(str(e))
