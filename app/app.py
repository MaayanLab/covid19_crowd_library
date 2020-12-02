import os
import json
import flask
import datetime
from app import database, geneset, drugset, download, statistics, collection

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')
BASE_PATH = os.environ.get('BASE_PATH', 'maayanlab.cloud')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__, static_url_path=ROOT_PATH + 'static')
app.before_first_request(database.init)


@app.route(ROOT_PATH, methods=['GET'])
def route_index():
    return flask.render_template('index.html', stats=statistics.stats(), base_path=BASE_PATH)


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
        return flask.render_template('review.html', base_path=BASE_PATH)
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
    return flask.render_template('geneset.html', geneset=json_geneset, base_path=BASE_PATH)


@app.route(ROOT_PATH + 'drugsets/<drugset_id>', methods=['GET'])
def route_drugset(drugset_id):
    json_drugset = json.loads(drugset.get_drugset(drugset_id)[0])
    return flask.render_template('drugset.html', drugset=json_drugset, base_path=BASE_PATH)


@app.route(ROOT_PATH + 'genes/<gene_name>', methods=['GET'])
def route_gene(gene_name):
    json_geneset = json.loads(geneset.get_gene(gene_name)[0])
    return flask.render_template('gene.html', gene=json_geneset, base_path=BASE_PATH)


@app.route(ROOT_PATH + 'drugs/<drug_name>', methods=['GET'])
def route_drug(drug_name):
    json_drugset = json.loads(drugset.get_drug(drug_name)[0])
    # If it's 404, set 'name' anyway
    json_drugset['name'] = drug_name
    twitter = drugset.twitter_drug_submission(drug_name)
    if (twitter[1] == 200) and (twitter[0] != '[]'):
        json_drugset['twitter'] = twitter[0]
        start = json.loads(twitter[0])[0]['date']
        y, m, d = start.split('-')
        s = datetime.datetime(int(y), int(m), int(d))
        start = s.strftime("%b %d")
        json_drugset['start'] = start
    return flask.render_template('drug.html', drug=json_drugset, base_path=BASE_PATH)


@app.route(ROOT_PATH + 'stats/drugs/<drug_name>/twitter', methods=['GET'])
def route_drug_twitter_submissions(drug_name):
    return drugset.twitter_drug_submission(drug_name)[0]


@app.route(ROOT_PATH + 'stats')
def route_stats():
    return flask.render_template('stats.html', stats=statistics.stats(), base_path=BASE_PATH)


@app.route(ROOT_PATH + 'top_genes', methods=['GET', 'POST'])
def route_top_genes():
    if flask.request.method == 'GET':
        return json.dumps({'success': True, 'data': statistics.bar_genes()}), 200, {'ContentType': 'application/json'}
    elif flask.request.method == 'POST':
        POST = json.loads(flask.request.values.get('body'))
        return statistics.top_genes(**POST)


@app.route(ROOT_PATH + 'top_drugs', methods=['GET', 'POST'])
@app.route(ROOT_PATH + 'top_drugs/<categories>', methods=['GET', 'POST'])
def route_top_drugs(categories=None):
    if flask.request.method == 'GET':
        if not categories or categories == 0:
            return json.dumps({'success': True, 'data': statistics.bar_drugs()}), 200, {
                'ContentType': 'application/json'}
        else:
            return json.dumps({'success': True, 'data': statistics.bar_drugs(categories)}), 200, {
                'ContentType': 'application/json'}
    elif flask.request.method == 'POST':
        POST = json.loads(flask.request.values.get('body'))
        if not categories or categories == 0:
            return statistics.top_drugs(**POST)
        else:
            return statistics.top_drugs_categories(categories, POST)


@app.route(ROOT_PATH + 'genesets.gmt')
def download_genesets():
    return flask.Response(download.genesets(), mimetype='text/gmt')


@app.route(ROOT_PATH + 'drugsets.gmt')
def download_drugsets():
    return flask.Response(download.drugsets(), mimetype='text/gmt')


@app.route(ROOT_PATH + 'experimantal_drugsets.gmt')
def download_experimental():
    return flask.Response(download.drugsets(2), mimetype='text/gmt')


@app.route(ROOT_PATH + 'computational_drugsets.gmt')
def download_computational():
    return flask.Response(download.drugsets(3), mimetype='text/gmt')


@app.route(ROOT_PATH + 'twitter_drugsets.gmt')
def download_twitter():
    return flask.Response(download.drugsets(4), mimetype='text/gmt')


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
                                     website="https://maayanlab.cloud/Harmonizome/gene/",
                                     className="enriched-gene-link",
                                     ids={ids},
                                     base_path=BASE_PATH)
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
                                     ids={ids},
                                     base_path=BASE_PATH)
    else:
        ids = flask.request.values.getlist("id")
        return flask.jsonify(drugset.get_intersection(ids))


@app.route(ROOT_PATH + 'genesets/submissions', methods=['GET'])
def route_genesets_submissions():
    return json.dumps({'success': True, 'data': statistics.genesets_submissions()}), 200, {
        'ContentType': 'application/json'}


@app.route(ROOT_PATH + 'drugsets/submissions', methods=['GET'])
def route_drugsets_submissions():
    return json.dumps({'success': True, 'data': statistics.drugsets_submissions()}), 200, {
        'ContentType': 'application/json'}


@app.route(ROOT_PATH + 'collection/<collection_id>', methods=['GET'])
def route_collection(collection_id):
    collections = collection.get_collection(int(collection_id))
    if collections[1] == 200:
        return flask.render_template('collection.html', collection=json.loads(collections[0]), base_path=BASE_PATH)
    else:
        return flask.render_template('404.html', error=collections[2])
