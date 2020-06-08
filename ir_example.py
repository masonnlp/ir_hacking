"""
This file has the beginnning of the SQUAD_IR module
TODO: add index deletion and checking utility methods
TODO: clean up documentations
"""
import json
import pandas as pd
import os
import os.path
from whoosh import index
# from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser


class SQUADIR:
    """
    SQUAD_IR class
    TODO flush out docustring
    """

    def SQUADIR(self):
        """
        default construstor for now
        """
        pass

    def load(self):
        """
        utiltiy method to load squad data set
        TODO reorganize locaiton of data set into data subdirectory
        TODO get path using standard methods
        TODO gen ID for contexts
        TODO save remainsing data as instance variable
        """
        with open('train-v2.0.json') as f:
            data = json.load(f)
        d = data['data']
        titles = []
        contexts = []
        # context_ids = []
        for i in d:
            title = i['title']
            paragraphs = i['paragraphs']
            # print(title)
            for p in paragraphs:
                qas = p['qas']
                context = p['context']
                # print("    " + context)
                titles.append(title)
                contexts.append(context)
                for qa in qas:
                    # question = qa['question']
                    # id = qa['id']
                    # print("        " + question)
                    # print("        " + id)
                    answers = qa['answers']
                    # is_impossible = qa['is_impossible']
                    # print("        " + str(is_impossible))
                    for answer in answers:
                        # text = answer['text']
                        # answer_start = answer['answer_start']
                        # print("            " + text)
                        # print("            " + str(answer_start))
                        pass
        self.df_context = pd.DataFrame(data={'title': titles,
                                             'context': contexts})

    def mk_index(self):
        """
        creates an index for IR operations
        TODO: add variable for placement of index
        """
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        schema = Schema(title=TEXT(stored=True),
                        context=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.ix = index.create_in("indexdir", schema)

    def index_docs(self):
        """"
        indexes documents
        TODO: move df to instance variable
        """
        writer = self.ix.writer()
        print("adding docunents")
        for i, row in self.df_context.iterrows():
            writer.add_document(title=row['title'], context=row['context'])
        print("commiting index")
        writer.commit()

    def query_index(self, query=u"nederduits"):
        """
        simple method to query index
        TODO: return results
        """
        qp = QueryParser("context", schema=self.ix.schema)
        q = qp.parse(query)
        with self.ix.searcher() as s:
            results = s.search(q)
            for result in results:
                print(result)


def test_main():
    """
    main testing method
    TODO: make it more exhaustive
    """
    squad_ir = SQUADIR()
    squad_ir.load()
    squad_ir.mk_index()
    squad_ir.index_docs()
    squad_ir.query_index("hello")
