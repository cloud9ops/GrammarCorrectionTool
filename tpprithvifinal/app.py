from flask import Flask, render_template, request
from text_polish import polish_full_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form.get('user_text', '')
        try:
            result = polish_full_text(user_input)
        except ValueError as e:
            result = {"error": str(e)}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
