import os

from github import Github
from flask import Flask, redirect, render_template, url_for
from flask_dance.contrib.github import github, make_github_blueprint

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersekrit')
app.config['GITHUB_OAUTH_CLIENT_ID'] = os.environ.get('GITHUB_OAUTH_CLIENT_ID')
app.config['GITHUB_OAUTH_CLIENT_SECRET'] = os.environ.get('GITHUB_OAUTH_CLIENT_SECRET')
github_bp = make_github_blueprint(scope='repo')
app.register_blueprint(github_bp, url_prefix='/login')


@app.route('/')
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))
    token = github.token['access_token']
    g = Github(token)
    user = g.get_user()
    repos = list(user.get_repos())
    return render_template('main.html', user=user, repos=repos, count=len(repos))
