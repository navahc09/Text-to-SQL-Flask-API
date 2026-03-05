# using flask to create api endpoint '/query' to access the model from the outside
from flask import Flask, request, jsonify
from pipeline import text_to_sql_summary

app = Flask(__name__)

# we have five functions:
# text_to_sql_summary()
# generate_query()
# validate_query()
# execute_query()
# summarize_result()
# process the query in json format from get_sql_from_english() function from english_to_sql script

@app.route('/query', methods=['POST'])
def process_query():
	data = request.get_json()
	
	if not data or 'question' not in data:
		return jsonify({"error": "Invalid Input, 'question' is required"})

	question = data['question']
	summary = text_to_sql_summary(question)

	if "error" in summary:
		return jsonify(summary), 500
	else:
		return jsonify(summary)

if __name__ == '__main__':
	app.run(debug=True, port=5000)
	app.run(host="0.0.0.0", port=5000)