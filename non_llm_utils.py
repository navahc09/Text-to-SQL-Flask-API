import sqlite3
import regex as re

FORBIDDEN_KEYWORDS = {
    "drop", "delete", "update", "insert", "alter",
    "truncate", "create", "replace", "attach", "detach"
}

# this function is used to extract sql content from generated text usingt regex
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
            columns = [desc[0] for desc in cursor.description]
            return {"data": results, "columns": columns, "error": None}
    except sqlite3.Error as e:
        return {"data": None, "columns": None, "error": str(e)}
    
# this function is used to validate the query for any security issues
def validate_sql_query(sql_query: str, schema):
    """
    Returns: (is_valid: bool, message: str)
    """

    if not sql_query or not sql_query.strip():
        return False, "Empty SQL query"

    sql_clean = sql_query.strip().lower()

    # all queries must start with SELECT
    if not sql_clean.startswith("select"):
        return False, "Only SELECT queries are allowed"

    # block multiple statements
    if ";" in sql_clean[:-1]:
        return False, "Multiple SQL statements are not allowed"

    # forbidden keywords
    for word in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{word}\b", sql_clean):
            return False, f"Forbidden keyword detected: {word}"

    # extract table names (simple heuristic)
    table_pattern = r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)|\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    tables_found = re.findall(table_pattern, sql_clean)

    used_tables = set()
    for t1, t2 in tables_found:
        if t1:
            used_tables.add(t1.lower())
        if t2:
            used_tables.add(t2.lower())

    # verify tables exist
    for table in used_tables:
        if table not in schema:
            return False, f"Unknown table: {table}"

    # extract columns (heuristic)
    column_pattern = r"select\s+(.*?)\s+from"
    match = re.search(column_pattern, sql_clean, re.DOTALL)

    if match:
        cols_part = match.group(1)

        # skip SELECT *
        if "*" not in cols_part:
            columns = [c.strip().split()[-1] for c in cols_part.split(",")]

            allowed_columns = set()
            for table in used_tables:
                allowed_columns.update(schema[table])   

            for col in columns:
                if "." in col:
                    col = col.split(".")[-1]

                # remove parentheses and functions
                col = col.replace(")", "").replace("(", "")

                # remove aggregate functions like COUNT, SUM etc
                col = re.sub(r"^(count|sum|avg|min|max)", "", col, flags=re.IGNORECASE)

                col = col.strip()

                if col.lower() not in [c.lower() for c in allowed_columns]:
                    return False, f"Unknown column: {col}"

    return True, sql_query