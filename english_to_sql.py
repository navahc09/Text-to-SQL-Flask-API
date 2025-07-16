import sqlite3
import regex as re
import torch
from transformers import pipeline

# using TinyLlama-1.1B-Chat-v1.0 model because of consistency and ability to put system prompts
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="cpu")


# this function is used to extract sql content from generated text
def extract_sql(text: str) -> str | None:
    match = re.search(r"```(?:sql)?\s*\n(.*?)\n\s*```", text, re.DOTALL)

    if match:
        return match.group(1).strip().replace('\n', ' ')
    else:
        if "SELECT" in text.upper():
            return text.strip().replace('\n', ' ')

    return None


# this function is used to execute the generated and extracted SQL query on Chinook DB
def execute_query(db_path, query):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return {"data": results, "error": None}
    except sqlite3.Error as e:
        return {"data": None, "error": str(e)}


# primary function being called in app.py
def get_sql_from_english(question: str):
    # feeding messages list into the model
    messages = [
        {
            "role": "system",
            "content": (

                "You are a SQL expert. Your job is write SQL queries to find answers for the plain English questions provided to you as input. "
                "Given dataset is that of a digital media store, which contains the tables Album(AlbumId, Title, ArtistId), and "
                "Artist(ArtistId, Name). Strictly use an Alias while generating each query. Write clear, unambigious SQL queries for each English statement. Do not answer in any other way "
                "Ignore irrelevant questions and ensure that your query is relevant, dont do anything thats more than whats asked. "
                "Your SQL query must be wrapped between standard triple backticks."
            )
        },

        {
            "role": "user",
            "content": question
        }
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.1, top_k=20, top_p=0.95)
    raw = outputs[0]["generated_text"]

    # check raw generated text for debugging purposes
    print(raw)
    # extract sql statement only from the generated text
    sql_query = extract_sql(raw)

    if not sql_query:
        return {"error": "Failed to generate SQL query from the model."}

    DB_PATH = 'Chinook_Sqlite.sqlite'
    result = execute_query(DB_PATH, sql_query)

    if result["error"]:
        return {"error": f"SQL Execution failed: {result['error']}", "generated_sql": sql_query}
    else:
        return {"generated_sql": sql_query, "database_query_result": result["data"]}
