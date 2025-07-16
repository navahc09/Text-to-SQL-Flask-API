# using flask to create api endpoint '/query' to access the model from the outside
from flask import Flask, request, jsonify
from english_to_sql import get_sql_from_english

app = Flask(__name__)

# process the query in json format from get_sql_from_english() function from english_to_sql script
@app.route('/query', methods=['POST'])
def process_query():
	data = request.get_json()

	if not data or 'question' not in data:
		return jsonify({"error": "Invalid input. 'question' is required"})

	question = data['question']
	result = get_sql_from_english(question)

	if "error" in result:
		return jsonify(result), 500
	else:
		return jsonify(result)

if __name__ == '__main__':
	app.run(debug=True, port=5000)