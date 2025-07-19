import subprocess
from flask import Flask, render_template, request
from text_processor import polish_text

app = Flask(__name__)

def strip_latex(raw: str) -> str:
    """
    Uses pandoc to convert LaTeX input to plain text, removing LaTeX syntax.
    Requires pandoc to be installed and available on the system PATH.
    """
    try:
        result = subprocess.run(
            ['pandoc', '--from=latex', '--to=plain'],
            input=raw,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Pandoc error: {e}")
        # Return raw input if pandoc fails
        return raw.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    original = ''
    polished = ''
    issues = []

    if request.method == 'POST':
        raw_input = request.form.get('sentence', '').strip()

        if raw_input:
            try:
                # Optional: Strip LaTeX formatting (comment out if not needed)
                stripped_text = strip_latex(raw_input)

                # Polish the text: returns original, corrected text, and issues list
                original, polished, issues = polish_text(stripped_text)

            except Exception as e:
                print(f"Error processing input: {e}")
                polished = "An error occurred while processing the text."

    return render_template(
        'index.html',
        original=original,
        polished=polished,
        issues=issues
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
