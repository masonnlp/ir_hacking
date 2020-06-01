import json
import pandas as pd
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser

def load_squad():
    with open('train-v2.0.json') as f:
        data = json.load(f)
    d = data['data']
    titles = []
    contexts = []
    context_ids = []
    for i in d:
        title = i['title']
        paragraphs = i['paragraphs']
        for p in paragraphs:
            qas = p['qas']
            context = p['context']
            titles.append(title)
            contexts.append(context)
            for qa in qas:
                question = qa['question']
                id = qa['id']
                answers = qa['answers']
                is_impossible = qa['is_impossible']
                for answer in answers:
                    text = answer['text']
                    answer_start = answer['answer_start']
    df = pd.DataFrame(data={'title':titles, 'context':contexts})
    return df

def mk_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    schema = Schema(title=TEXT(stored=True),
        context=TEXT(stored=True, analyzer=StemmingAnalyzer()))
    ix = index.create_in("indexdir", schema)
    return ix

def index_docs(ix, df):
    writer = ix.writer()
    print("adding docunents")
    for index, row in df.iterrows():
        writer.add_document(title=row['title'], context=row['context'])
    print("commiting index")
    writer.commit()

def query_index(ix):
    qp = QueryParser("context", schema=ix.schema)
    q = qp.parse(u"nederduits")
    with ix.searcher() as s:
        results = s.search(q)
        for result in results:
            print(result)

df = load_squad()
ix = mk_index()
index_docs(ix, df)
query_index(ix)
