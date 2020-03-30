import flask
from dotenv import load_dotenv
from .geneset import *
from .drugset import *

load_dotenv(verbose=True)

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__, static_url_path=ROOT_PATH + 'static')


@app.route(ROOT_PATH + 'static')
def staticfiles(path):
    return flask.send_from_directory('static', path)


@app.route(ROOT_PATH, methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route(ROOT_PATH + 'enrichr', methods=['GET', 'POST'])
def enrichr():
    if flask.request.method == 'GET':
        reviewed = flask.request.args.get('reviewed', 1)
        return get_genesets(reviewed)
    elif flask.request.method == 'POST':
        return add_geneset(flask.request.form)


@app.route(ROOT_PATH + 'drugs', methods=['GET', 'POST'])
def drugs():
    if flask.request.method == 'GET':
        reviewed = flask.request.args.get('reviewed', 1)
        return get_drugsets(reviewed)
    elif flask.request.method == 'POST':
        return add_drugset(flask.request.form)


@app.route(ROOT_PATH + 'review', methods=['GET', 'POST'])
def review():
    if flask.request.method == 'GET':
        return flask.render_template('review.html')
    elif flask.request.method == 'POST':
        return approve_geneset(flask.request.form)


@app.route(ROOT_PATH + 'geneset/<geneset_id>', methods=['GET'])
def geneset(geneset_id):
    print(geneset_id)
    return