# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from main import main  # Importing the main function from main.py

app = Flask(__name__)
app.secret_key = 'xyz'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        codeforces_username = request.form['codeforces_username']
        codechef_username = request.form['codechef_username']
        atcoder_username = request.form['atcoder_username']
        access_token = request.form['access_token']
        repo_name = request.form['repo_name']

        if codeforces_username or codechef_username or atcoder_username:
            if not access_token:
                flash('Please enter GitHub access token.', 'error')
            else:
                main()
                flash('Scraping and uploading completed successfully!', 'success')
        else:
            flash('Please enter at least one username.', 'warning')

        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
