import os
import json
import flask
from app import database, geneset, drugset, download, statistics

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__, static_url_path=ROOT_PATH + 'static')
app.before_first_request(database.init)


@app.route(ROOT_PATH, methods=['GET'])
def route_index():
    return flask.render_template('index.html', stats=statistics.stats())


@app.route(ROOT_PATH + 'genesets_table', methods=['POST'])
def route_genesets_table():
    return geneset.serve_geneset_datatable(int(flask.request.values.get('reviewed')))(
        **json.loads(flask.request.values.get('body')))


@app.route(ROOT_PATH + 'genesets', methods=['GET', 'POST'])
def route_genesets():
    if flask.request.method == 'GET':
        reviewed = flask.request.args.get('reviewed', 1)
        return geneset.get_genesets(reviewed)
    elif flask.request.method == 'POST':
        return geneset.add_geneset(flask.request.form)


@app.route(ROOT_PATH + 'drugsets_table', methods=['POST'])
def route_drugsets_table():
    category = int(flask.request.values.get('category', default=0))
    if category:
        return drugset.serve_drugset_filtered_datatable(int(flask.request.values.get('reviewed')), category)(
            **json.loads(flask.request.values.get('body')))
    else:
        return drugset.serve_drugset_datatable(int(flask.request.values.get('reviewed')))(
            **json.loads(flask.request.values.get('body')))



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
        form = flask.request.form
        if form['set_type'] == 'geneset':
            return geneset.approve_geneset(form)
        elif form['set_type'] == 'drugset':
            if 'category' in form:
                return drugset.change_category(form)
            else:
                return drugset.approve_drugset(form)


@app.route(ROOT_PATH + 'genesets/<geneset_id>', methods=['GET'])
def route_geneset(geneset_id):
    json_geneset = json.loads(geneset.get_geneset(geneset_id)[0])
    return flask.render_template('geneset.html', geneset=json_geneset)


@app.route(ROOT_PATH + 'drugsets/<drugset_id>', methods=['GET'])
def route_drugset(drugset_id):
    json_drugset = json.loads(drugset.get_drugset(drugset_id)[0])
    return flask.render_template('drugset.html', drugset=json_drugset)


@app.route(ROOT_PATH + 'stats')
def route_stats():
    return flask.render_template('stats.html', stats=statistics.stats())


@app.route(ROOT_PATH + 'top_genes', methods=['GET', 'POST'])
def route_top_genes():
    if flask.request.method == 'GET':
        return json.dumps({'success': True, 'data': statistics.bar_genes()}), 200, {'ContentType': 'application/json'}
    elif flask.request.method == 'POST':
        POST = json.loads(flask.request.values.get('body'))
        return statistics.top_genes(**POST)


@app.route(ROOT_PATH + 'top_drugs', methods=['GET', 'POST'])
def route_top_drugs():
    if flask.request.method == 'GET':
        return json.dumps({'success': True, 'data': statistics.bar_drugs()}), 200, {'ContentType': 'application/json'}
    elif flask.request.method == 'POST':
        POST = json.loads(flask.request.values.get('body'))
        return statistics.top_drugs(**POST)


@app.route(ROOT_PATH + 'genesets.gmt')
def download_genesets():
    return flask.Response(download.genesets(), mimetype='text/gmt')


@app.route(ROOT_PATH + 'drugsets.gmt')
def download_drugsets():
    return flask.Response(download.drugsets(), mimetype='text/gmt')


@app.route(ROOT_PATH + 'genesets/overlap', methods=['GET', 'POST'])
@app.route(ROOT_PATH + 'genesets/overlap/<ids>')
def route_overlap_genesets(ids=None):
    if ids:
        print(len(ids.split(",")))
        # if len(ids.split(",")) > 5:
        #     return flask.render_template('venn.html', type="Gene set", maxError=True)
        # else:
        intersection = geneset.get_intersection(ids.split(","))
        return flask.render_template('venn.html',
                                     intersection=intersection["overlaps"],
                                     labels=intersection["labels"],
                                     type="Gene Set",
                                     elements="genes",
                                     website="https://amp.pharm.mssm.edu/Harmonizome/gene/",
                                     className="enriched-gene-link",
                                     ids={ids})
    else:
        ids = flask.request.values.getlist("id")
        return flask.jsonify(geneset.get_intersection(ids))


@app.route(ROOT_PATH + 'drugsets/overlap', methods=['GET', 'POST'])
@app.route(ROOT_PATH + 'drugsets/overlap/<ids>')
def route_overlap_drugsets(ids=None):
    if ids:
        # print(len(ids.split(",")))
        # if len(ids.split(",")) > 5:
        #     return flask.render_template('venn.html', type="Drug-set", maxError=True)
        # else:
        intersection = drugset.get_intersection(ids.split(","))
        return flask.render_template('venn.html',
                                     intersection=intersection["overlaps"],
                                     labels=intersection["labels"],
                                     type="Drug Set",
                                     elements="drugs",
                                     website="https://www.drugbank.ca/unearth/q?utf8=✓&searcher=drugs&query=",
                                     className="drug-link",
                                     ids={ids})
    else:
        ids = flask.request.values.getlist("id")
        return flask.jsonify(drugset.get_intersection(ids))
