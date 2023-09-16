from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

GET_METHOD = 'GET'
POST_METHOD = 'POST'

in_memory_datastore = {
    "COBOL": {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL": {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL": {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
   "BASIC": {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"},
   "PL": {"name": "PL", "publication_year": 1966, "contribution": "constants, function overloading, pointers"},
   "SIMULA67": {"name": "SIMULA67", "publication_year": 1967,
                "contribution": "class/object split, subclassing, protected attributes"},
   "Pascal": {"name": "Pascal", "publication_year": 1970,
              "contribution": "modern unary, binary, and assignment operator syntax expectations"},
   "CLU": {"name": "CLU", "publication_year": 1975,
           "contribution": "iterators, abstract data types, generics, checked exceptions"},
}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/programming_languages', methods=[GET_METHOD, POST_METHOD])
def programming_languages_route():
    if request.method == GET_METHOD:
        return list_programming_languages()
    elif request.method == POST_METHOD:
        return create_programming_language(request.get_json(force=True))

def list_programming_languages():
    before_year = request.args.get('before_year') or '30000'
    after_year = request.args.get('after_year') or '0'
    qualifying_data = list(
        filter(
            lambda pl: int(before_year) > pl ['publication_year'] > int(after_year), in_memory_datastore.values()
        ))
    return {"programming_languages": qualifying_data}

def create_programming_language(new_lang):
    language_name = new_lang['name']
    in_memory_datastore[language_name] = new_lang
    return new_lang

@app.route('/programming_languages/<programming_language_name>')
def get_programming_language_name(programming_language_name):
    return in_memory_datastore[programming_language_name]
