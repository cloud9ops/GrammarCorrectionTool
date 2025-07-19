from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from text_polish import stream_polish_sentences
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream', methods=['POST'])
def stream():
    user_input = request.form.get('user_text', '')
    if not user_input.strip():
        return Response("No input text provided.", status=400)

    def generate():
        try:
            for detail in stream_polish_sentences(user_input):
                json_data = json.dumps(detail)
                yield f"data: {json_data}\n\n"
        except ValueError as e:
            yield f"data: error|{str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route('/auto-polish', methods=['POST'])
def auto_polish():
    try:
        data = request.get_json()
        sentence = data.get('sentence', '').strip()
        if not sentence:
            return jsonify({"error": "No sentence provided"}), 400

        # Use only the first polished result
        results = list(stream_polish_sentences(sentence))
        if not results:
            return jsonify({"error": "No polishing result returned"}), 500

        return jsonify(results[0])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)

