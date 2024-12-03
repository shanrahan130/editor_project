from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def count_vowels():
    # Add CORS headers to allow access from different origins
    response = jsonify(get_vowel_count_response())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def get_vowel_count_response():
    text = request.args.get('text', '')
    vowels = 'aeiouAEIOU'
    count = sum(1 for char in text if char in vowels)
    return {
        'error': False,
        'string': f'Contains {count} vowels',
        'answer': count
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
