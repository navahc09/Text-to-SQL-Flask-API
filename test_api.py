# this script is the primary way to interact with the application
# a cURL command pasted in terminal could also perform the same job
# feel free to change questions in the questions_to_test list

import requests
# URL for the flask api endpoint
API_URL = 'http://127.0.0.1:5000/query'

questions_to_test = [
    "List all album titles by the artist AC/DC",
    "Count the total number of albums for every artist.",
    "Show all artists whose name starts with 'A'",
    "Retrieve the title of the album that has an identifier of 3.",
    "Identify the artist who recorded the album named 'Are You Experienced?'."
]

# enumerating over each question individually from the questions_to_test list
for i, question in enumerate(questions_to_test, 1):
    print(f"***** Question {i}: {question} *****")

    json_data = {
        'question': question
    }

    # basic try-except to catch exceptions
    try:
        # passing the question as a POST request in json format
        response = requests.post(API_URL, json=json_data)

        if response.status_code == 200:
            print("Server Response:")
        else:
            print(f"Error: Received status code {response.status_code}")

        print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"A connection error occurred: {e}")

    print("\n")
