from main import codeforces_uploader, codechef_uploader, atcoder_uploader
from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from gevent import monkey
from github import Github
from github.GithubException import UnknownObjectException
monkey.patch_all()


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        codeforces_username = request.form.get('codeforces_username')
        codechef_username = request.form.get('codechef_username')
        atcoder_username = request.form.get('atcoder_username')
        access_token = request.form.get('access_token')
        repo_name = request.form.get('repo_name')

        # Create a GitHub repo and call the respective uploader functions
        # You'll need to modify this part to work with the existing code
        g = Github(access_token)
        try:
            repo = g.get_user().get_repo(repo_name)
        except UnknownObjectException:
            repo = g.get_user().create_repo(repo_name, private=True)

        # Call the uploader functions with the repository object
        if codechef_username:
            codechef_uploader(codechef_username, repo)
        if codeforces_username:
            codeforces_uploader(codeforces_username, repo)
        if atcoder_username:
            atcoder_uploader(atcoder_username, repo)
        
        return 'Data submitted successfully!'

    return render_template('index.html')


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
