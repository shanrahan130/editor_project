from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def count_palindromes():
    text = request.args.get("text", "")
    words = text.split(" ")
    count = sum(1 for word in words if word.lower() == word.lower()[::-1])
    
    response = {
        "error": False,
        "string": f"Contains {count} palindromes",
        "answer": count
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
