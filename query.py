import json
import os

QUERY_PATH = 'data/queries.json'
URL_PATH = 'data/urls.json'

def recurse_tuple(iter):
    ret = []
    for elem in iter:
        if isinstance(elem, list):
            elem = tuple([tuple(recurse_tuple(x)) if isinstance(x, list) else x for x in elem])
        ret.append(elem)
    return ret

def create_data_file(fp: str):
    if not os.path.isfile(fp):
        open(fp, 'w').close()

def load_queries():
    try:
        queries = recurse_tuple([sorted(d) for d in get_data_from_file(QUERY_PATH)])
        urls = get_data_from_file(URL_PATH)
    except FileNotFoundError:
        create_data_file(QUERY_PATH)
        create_data_file(URL_PATH)
        queries = []
        urls = []

    return queries, urls

def get_data_from_file(fp):
    with open(fp, 'r') as f:
        data =  json.load(f)

    return data

def save_queries(queries, urls):
    with open(QUERY_PATH, 'w') as query_file:
        json.dump(queries, query_file)

    with open(URL_PATH, 'w') as url_file:
        json.dump(urls, url_file)