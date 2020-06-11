"""
This file has the beginnning of the SQUAD_IR module
TODO: add index deletion and checking utility methods
TODO: clean up documentations
"""
import json
import shutil
import pandas as pd
import os
import os.path
from whoosh import index
import hashlib
# from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser


class SQUADIR:
    """
    SQUADIR class
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
        ans_count = 0
        context_titles = []
        context_contexts = []
        context_contextids = []
        question_contextids = []
        question_questionids = []
        question_questions = []
        question_is_impossibles = []
        answer_contextids = []
        answer_questionids = []
        answer_answerids = []
        answer_answers = []
        answer_answer_starts = []
        for i in d:
            title = i['title']
            paragraphs = i['paragraphs']
            # print(title)
            for p in paragraphs:
                qas = p['qas']
                context = p['context']
                contextid = hashlib.sha1(context.encode()).hexdigest()
                context_titles.append(title)
                context_contextids.append(contextid)
                context_contexts.append(context)
                for qa in qas:
                    question = qa['question']
                    questionid = qa['id']
                    is_impossible = qa['is_impossible']
                    question_contextids.append(contextid)
                    question_questionids.append(questionid)
                    question_questions.append(question)
                    question_is_impossibles.append(is_impossible)
                    answers = qa['answers']
                    for answer in answers:
                        ans_count += 1
                        text = answer['text']
                        answer_start = answer['answer_start']
                        answerid = hashlib.md5(text.encode()).hexdigest()
                        answer_contextids.append(contextid)
                        answer_questionids.append(questionid)
                        answer_answerids.append(answerid)
                        answer_answers.append(text)
                        answer_answer_starts.append(answer_start)
        self.df_context = pd.DataFrame(
            {'contextid': context_contextids, 'title': context_titles,
             'context': context_contexts})
        self.df_questions = pd.DataFrame(
            {'contextid': question_contextids,
             'questionid': question_questionids,
             'question': question_questions,
             'is_impossible': question_is_impossibles})
        self.df_answers = pd.DataFrame(
            {'contextid': answer_contextids,
             'questionid': answer_questionids,
             'answerid': answer_answerids,
             'answer': answer_answers,
             'answer_start': answer_answer_starts})

    def mk_index(self, indexpath="indexdir", overwrite=True):
        """
        creates an index for IR operations
        """
        if os.path.exists(indexpath):
            if overwrite:
                shutil.rmtree(indexpath)
        if not os.path.exists(indexpath):
            os.mkdir(indexpath)
        schema = Schema(title=TEXT(stored=True),
                        context=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.ix = index.create_in("indexdir", schema)

    def rm_index(self, indexpath="indexdir"):
        if os.path.exists(indexpath):
            os.rmdir(indexpath)

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
