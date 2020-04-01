import os
import json
import flask
from app import database, geneset, drugset

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__, static_url_path=ROOT_PATH + 'static')
app.before_first_request(database.init)


@app.route(ROOT_PATH, methods=['GET'])
def route_index():
    return flask.render_template('index.html')


@app.route(ROOT_PATH + 'genesets', methods=['GET', 'POST'])
def route_genesets():
    if flask.request.method == 'GET':
        reviewed = flask.request.args.get('reviewed', 1)
        return geneset.get_genesets(reviewed)
    elif flask.request.method == 'POST':
        return geneset.add_geneset(flask.request.form)


@app.route(ROOT_PATH + 'drugsets', methods=['GET', 'POST'])
def route_drugs():
    if flask.request.method == 'GET':
        reviewed = flask.request.args.get('reviewed', 1)
        return drugset.get_drugsets(reviewed)
    elif flask.request.method == 'POST':
        return drugset.add_drugset(flask.request.form)


@app.route(ROOT_PATH + 'review', methods=['GET', 'POST'])
def route_review():
    if flask.request.method == 'GET':
        return flask.render_template('review.html')
    elif flask.request.method == 'POST':
        return geneset.approve_geneset(flask.request.form)


@app.route(ROOT_PATH + 'genesets/<geneset_id>', methods=['GET'])
def route_geneset(geneset_id):
    return flask.render_template('geneset.html', geneset=json.loads(geneset.get_geneset(geneset_id)[0]))


@app.route(ROOT_PATH + 'drugsets/<drugset_id>', methods=['GET'])
def route_drugset(drugset_id):
    return flask.render_template('drugset.html', drugset=json.loads(drugset.get_drugset(drugset_id)[0]))
