# 🤖 AI SQL Assistant — Natural Language to Database Queries

Turn plain English questions into SQL queries and explore databases conversationally.

This project is an **AI-powered data assistant** that allows users to interact with a relational database using natural language. It converts questions into SQL queries using an LLM, executes them safely, and returns results along with visualizations.

Instead of writing SQL manually, users can simply ask questions in english like:

> “What are the top 10 most expensive tracks?”

and instantly receive answers.

---

# 🚀 Features

### 💬 Conversational AI Interface

A ChatGPT-style interface where users can ask database questions naturally.

### 🧠 LLM-powered SQL Generation

Uses **Gemini Flash 3.1 Flash Lite** to translate natural language questions into SQL queries.

### 🛡️ Query Safety Validation

A validation layer ensures:

- Only **SELECT queries** are allowed
- No destructive operations (`DROP`, `DELETE`, etc.)
- Tables referenced actually exist

### 📊 Automatic Data Visualization

Query results automatically generate charts when possible.

### 🗂️ Interactive Schema Explorer

Users can explore the database schema directly from the sidebar.

### ⚡ Fast API Backend

A lightweight API serves the LLM pipeline and executes queries securely.

---

# 🖥️ Demo

Example interaction:

User asks:

> "Top 10 most expensive tracks"

AI generates SQL:

```sql
SELECT Name, UnitPrice
FROM Track
ORDER BY UnitPrice DESC
LIMIT 10
```

Result:

| Name    | UnitPrice |
| ------- | --------- |
| Track A | 1.99      |
| Track B | 1.99      |

Visualization:

📊 Auto-generated bar chart of track prices.

---

# 🏗️ Architecture

```
User
 ↓
Streamlit Chat UI
 ↓
LLM SQL Generation (Gemini)
 ↓
SQL Validation Layer
 ↓
SQLite Database (Chinook)
 ↓
LLM Summary Generation (Gemini)
 ↓
Results + Charts
```

The system ensures safe query generation while providing a smooth conversational interface.

---

# 🧰 Tech Stack

**Frontend**

- Streamlit

**Backend**

- FastAPI / Flask

**LLM**

- Google Gemini Flash

**Database**

- SQLite (Chinook sample database)

**Libraries**

- pandas
- requests
- python-dotenv
- regex

---

# 📂 Project Structure

```
text-to-sql-ai/
│
├── frontend_chat.py        # Streamlit conversational UI
├── app.py                  # API server
│
├── pipeline.py             # LLM + SQL pipeline
├── llm_utils.py            # Gemini interaction
├── non_llm_utils.py        # SQL execution & validation
│
├── Chinook_Sqlite.sqlite   # Sample database
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/ai-sql-assistant.git
cd ai-sql-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Running the Project

Start the backend:

```bash
python app.py
```

Run the frontend:

```bash
streamlit run frontend_chat.py
```

Open the app:

```
http://localhost:8501
```

---

# 🧪 Example Questions

Try asking:

- List all artists
- Top 10 most expensive tracks
- Which genres have the most tracks?
- Which albums contain the most songs?

---

# 🔐 SQL Safety Layer

To prevent malicious queries, the system includes a validator that:

- restricts queries to `SELECT`
- blocks destructive operations
- checks referenced tables

This ensures the AI assistant **cannot modify or damage the database**.

---

# 💡 Why This Project Matters

Many companies struggle to give **non-technical users access to data**.

This project demonstrates how **Generative AI can bridge that gap**, allowing anyone to explore databases using natural language.

It combines:

- LLMs
- backend APIs
- database systems
- data visualization

into a practical AI application.

---

# 👨‍💻 Author

**Shubham**

IT Student | AI & Backend Systems Enthusiast

Interested in building practical AI tools that simplify complex workflows.

---

# ⭐ If you found this project interesting

Consider giving the repository a star!
