from flask import Flask, render_template, request
from load_more import extract_clean_emails

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    emails = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        post_url = request.form['post_url']
        emails = extract_clean_emails(username, password, post_url)
        return render_template('results.html', emails=emails)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

