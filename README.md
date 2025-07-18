# Text-to-SQL Flask API

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-blue)

This project is a functional prototype that converts natural language questions into SQL queries. It uses a pre-trained model from Hugging Face and exposes the functionality through a minimal REST API built with Flask.

## Features
* **Natural Language to SQL**: Translates plain English questions into executable SQL queries.
* **Hugging Face Integration**: Leverages a pre-trained `transformers` model for the core translation task.
* **Database Execution**: Connects to a local SQLite database (Chinook) to execute the generated queries.
* **REST API**: Exposes a single `POST /query` endpoint to make the service available over the network.

## Tech Stack
* **Backend**: Python, Flask
* **AI/ML**: Hugging Face Transformers, PyTorch
* **Database**: SQLite

---

## Setup and Installation

Follow these steps to get the project running locally.

### 1. Prerequisites
* Python 3.10 or higher
* `pip` and `venv` for package management

### 2. Installation
Clone the repository and set up the virtual environment.

```bash
# Clone the repository
git clone [https://github.com/your-username/Text-to-SQL-Flask-API.git](https://github.com/your-username/Text-to-SQL-Flask-API.git)
cd Text-to-SQL-Flask-API

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt
```

---

## Usage

The project can be run as a web server. Make sure you are in the project's root directory with the virtual environment activated.

### 1. Run the API Server
Start the Flask application by running `app.py`:

```bash
python app.py
```
The server will start, load the model into memory, and will be available at `http://127.0.0.1:5000`.

### 2. Test the Endpoint
You can test the live API endpoint using the provided `test_api.py` (by simply clicking the 'run' button) script or a cURL command.

**Using the Python Test Script:**
```bash
python test_api.py
```

**Using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "How many albums are there for the artist Aerosmith?"}' \
  [http://127.0.0.1:5000/query]
```
A successful response will be a JSON object containing the generated SQL and the results from the database.

---

## Alternative: Google Colab
For a cloud-based demonstration without a local setup, you can use the provided Google Colab notebook.

[**Link to Google Colab Notebook**](https://colab.research.google.com/drive/1l3dYjwANz42MGJVvpzhexZ3PirHo_Qor?usp=sharing)
