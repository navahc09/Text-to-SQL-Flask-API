from llm_utils import generate_query, summarize_result
from non_llm_utils import extract_sql, execute_query, validate_sql_query

# this is the schema for Chinook DB, which contains all the tables, keys, and relationships
schema = {
  "Tables": [
    {
      "name": "Artist",
      "columns": ["ArtistId (PK) (INTEGER)", "Name (NVARCHAR)"],
      "relationships": []
    },
    {
      "name": "Album",
      "columns": ["AlbumId (PK) (INTEGER)", "Title (NVARCHAR)", "ArtistId (FK) (INTEGER)"],
      "relationships": ["ArtistId references Artist(ArtistId)"]
    },
    {
      "name": "Genre",
      "columns": ["GenreId (PK) (INTEGER)", "Name (NVARCHAR)"],
      "relationships": []
    },
    {
      "name": "MediaType",
      "columns": ["MediaTypeId (PK) (INTEGER)", "Name (NVARCHAR)"],
      "relationships": []
    },
    {
      "name": "Track",
      "columns": ["TrackId (PK) (INTEGER)", "Name (NVARCHAR)", "AlbumId (FK) (INTEGER)", "MediaTypeId (FK) (INTEGER)", "GenreId (FK) (INTEGER)", "Composer (NVARCHAR)", "Milliseconds (INTEGER)", "Bytes (INTEGER)", "UnitPrice (NUMERIC)"],
      "relationships": [
        "AlbumId references Album(AlbumId)",
        "MediaTypeId references MediaType(MediaTypeId)",
        "GenreId references Genre(GenreId)"
      ]
    },
    {
      "name": "Employee",
      "columns": ["EmployeeId (PK) (INTEGER)", "LastName (NVARCHAR)", "FirstName (NVARCHAR)", "Title (NVARCHAR)", "ReportsTo (FK) (INTEGER)", "BirthDate (DATETIME)", "HireDate (DATETIME)", "Address (NVARCHAR)", "City (NVARCHAR)", "State (NVARCHAR)", "Country (NVARCHAR)", "PostalCode (NVARCHAR)", "Phone (NVARCHAR)", "Fax (NVARCHAR)", "Email (NVARCHAR)"],
      "relationships": ["ReportsTo references Employee(EmployeeId)"]
    },
    {
      "name": "Customer",
      "columns": ["CustomerId (PK) (INTEGER)", "FirstName (NVARCHAR)", "LastName (NVARCHAR)", "Company (NVARCHAR)", "Address (NVARCHAR)", "City (NVARCHAR)", "State (NVARCHAR)", "Country (NVARCHAR)", "PostalCode (NVARCHAR)", "Phone (NVARCHAR)", "Fax (NVARCHAR)", "Email (NVARCHAR)", "SupportRepId (FK) (INTEGER)"],
      "relationships": ["SupportRepId references Employee(EmployeeId)"]
    },
    {
      "name": "Invoice",
      "columns": ["InvoiceId (PK) (INTEGER)", "CustomerId (FK) (INTEGER)", "InvoiceDate (DATETIME)", "BillingAddress (NVARCHAR)", "BillingCity (NVARCHAR)", "BillingState (NVARCHAR)", "BillingCountry (NVARCHAR)", "BillingPostalCode (NVARCHAR)", "Total (NUMERIC)"],
      "relationships": ["CustomerId references Customer(CustomerId)"]
    },
    {
      "name": "InvoiceLine",
      "columns": ["InvoiceLineId (PK) (INTEGER)", "InvoiceId (FK) (INTEGER)", "TrackId (FK) (INTEGER)", "UnitPrice (NUMERIC)", "Quantity (INTEGER)"],
      "relationships": [
        "InvoiceId references Invoice(InvoiceId)",
        "TrackId references Track(TrackId)"
      ]
    },
    {
      "name": "Playlist",
      "columns": ["PlaylistId (PK) (INTEGER)", "Name (NVARCHAR)"],
      "relationships": []
    },
    {
      "name": "PlaylistTrack",
      "columns": ["PlaylistId (PK, FK) (INTEGER)", "TrackId (PK, FK) (INTEGER)"],
      "relationships": [
        "PlaylistId references Playlist(PlaylistId)",
        "TrackId references Track(TrackId)"
      ]
    }
  ]
}

# primary function being called in app.py
def text_to_sql_summary(question: str):
    # generate query here
    raw = generate_query(question, schema)
    if (raw=="error"):
        return {"error": "SQL Query generation failed"}

    # extract sql statement only from the generated text
    sql_query = extract_sql(raw)
    print(sql_query)
    table_map = {}  

    for table in schema["Tables"]:
        table_map[table["name"].lower()] = [
            col.split()[0] for col in table["columns"]
        ]
    #validate sql query here
    (is_valid, statement) = validate_sql_query(sql_query, table_map)
    if (is_valid==False):
        return {"error": f"SQL Query validation failed: {statement}"}
    
    DB_PATH = 'Chinook_Sqlite.sqlite'
    result = execute_query(DB_PATH, sql_query)

    if result["error"]:
        return {"error": f"SQL Execution failed: {result['error']}", "generated_sql": sql_query}

    summary = summarize_result(result, question, schema)

    return {
        "summary": summary,
        "database_query_result": result["data"],
        "columns": result["columns"],
        "generated_sql": sql_query
    }
    
