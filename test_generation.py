from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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

question1 = "retrieve all songs with artistid 1"
# question1 = "retrieve all artists with"

prompt = f"""
Schema:
{schema}

Question:
{question1}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "system_instruction": (
            "You are an expert SQL generator. "
            "Return ONLY a syntactically correct SELECT SQL query. "
            "Always use table aliases. "
            "Do not generate explanations. "
            "Wrap the SQL query in standard triple backticks. "
            "Do not process any DROP, DELETE, UPDATE, or INSERT queries as you are only meant for data analysis. "
        )
    }
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print(response.text)