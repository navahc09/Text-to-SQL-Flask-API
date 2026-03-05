import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# this function generates the sql query
def generate_query(question: str, schema):
    prompt = f"""
    Schema:
    {schema}

    Question:
    {question}
    """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
        config={
            "system_instruction": (
                "You are an expert SQL generator. "
                "Return ONLY a syntactically correct SELECT SQL query. "
                "Always use table aliases. "
                "Do not generate explanations. "
                "Wrap the SQL query in standard triple backticks. "
                "Do not process any DROP, DELETE, UPDATE, or INSERT queries as you are only meant for data analysis. "
                "If a valid SQL query cannot be generated for any reason, your response should only be 'error'"
            )
        }
    )

    if not response.text or "error" in response.text.lower():
        return "error"
    else:
        return response.text
    
# this function summarizes the SQL data recieved by executing the query
def summarize_result(result, question: str, schema):
    prompt = f"""
    Schema:
    {schema}

    Question:
    {question}
    
    Data:
    {result}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
        config={
            "system_instruction": (
                "You are an expert SQL data analyzer. "
                "You are given a question, and the SQL data responsible for answering it. "
                "You have to understand the question, analyze the data, and provide a summary for the resulting sql data. "
                "If a valid summary cannot be generated for any reason (like empty dataset), your response should only be 'error'"
            )
        }
    )

    if not response.text or "error" in response.text.lower():
        return "error"
    else:
        return response.text