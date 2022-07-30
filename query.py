import json
import os

QUERY_PATH = 'data/queries.json'


def create_query_file(fp: str) -> None:
    if not os.path.isfile(fp):
        open(fp, 'w').close()

def load_queries() -> dict:
    try:
        queries = get_queries_from_file(QUERY_PATH)
    except:
        create_query_file(QUERY_PATH)
        queries = {}
    return queries

def get_queries_from_file(fp) -> dict:
    with open(fp, 'r') as query_file:
        query_data =  json.load(query_file.read())

    return query_data

def save_queries(queries):
    with open(QUERY_PATH, 'w') as query_file:
        query_file.write(json.dump(queries, query_file))