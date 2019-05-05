import flask
from flask import request,jsonify
import json
import pymysql

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/plant/all', methods=['GET'])
def api_all():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='plant1')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM plant_data;')
    results=cur.fetchall()
    
    return jsonify(results)
    



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/plant', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id1 = query_parameters.get('id')
    query = "SELECT * FROM plant_data WHERE id = %s;"
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='plant1')
    cur = conn.cursor()
    cur.execute(query,[id1])
    row_headers=[x[0] for x in cur.description]
    print(row_headers)
    results=cur.fetchall()
    for result in results:
        list1=list(result)
        list1[3]=list(list1[3].split(";"))
        list1[8]=list(list1[8].split(";"))
        content =dict(zip(row_headers,list1))
             
    return jsonify(content)

app.run()