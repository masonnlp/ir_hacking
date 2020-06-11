"""
This file has the beginnning of the SQUAD_IR module
TODO: add index deletion and checking utility methods
TODO: clean up documentations
TODO: add individual search functions
"""
import json
import shutil
import pandas as pd
import os
import os.path
from whoosh import index
import hashlib
# from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.fields import Schema, TEXT, BOOLEAN, ID, NUMERIC
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
        TODO gzip data to minimize download
        TODO get path using standard methods
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

    def mk_index(self, indexpath="indexdir", overwrite=False):
        """
        creates an index for IR operations
        """
        if os.path.exists(indexpath):
            if overwrite:
                shutil.rmtree(indexpath)
        if not os.path.exists(indexpath):
            os.mkdir(indexpath)
        self.context_schema = Schema(
            contextid=ID(stored=True), title=TEXT(stored=True),
            context=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.context_ix = index.create_in("indexdir", self.context_schema)
        self.question_schema = Schema(
            contextid=ID(stored=True), questionid=ID(stored=True),
            is_impossible=BOOLEAN(stored=True),
            question=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.question_ix = index.create_in("indexdir", self.question_schema)
        self.answer_schema = Schema(
            contextid=ID(stored=True), questionid=ID(stored=True),
            answerid=ID(stored=True), answer_start=NUMERIC(stored=True),
            answer=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.answer_ix = index.create_in("indexdir", self.answer_schema)

    def rm_index(self, indexpath="indexdir"):
        if os.path.exists(indexpath):
            os.rmdir(indexpath)

    def index_docs(self):
        """"
        indexes documents
        TODO: add handling LockError
        TODO: add handling test for LockError
        """
        print("adding docunents")
        context_writer = self.context_ix.writer()
        for i, row in self.df_context.iterrows():
            context_writer.add_document(
                contextid=row['contextid'],
                title=row['title'], context=row['context'])
        context_writer.commit()
        question_writer = self.question_ix.writer()
        for i, row in self.df_questions.iterrows():
            question_writer.add_document(
                contextid=row['contextid'], questionid=row['questionid'],
                question=row['question'], is_impossible=row['is_impossible'])
        question_writer.commit()
        answer_writer = self.answer_ix.writer()
        for i, row in self.df_answers.iterrows():
            answer_writer.add_document(
                contextid=row['contextid'], questionid=row['questionid'],
                answerid=row['answerid'],
                answer=row['answer'], answer_start=row['answer_start'])
        answer_writer.commit()
        print("commiting index")

    def query_context(self, query=u"nederduits"):
        """
        simple method to query index
        TODO: return results
        """
        qp = QueryParser("context", schema=self.context_schema)
        q = qp.parse(query)
        with self.context_ix.searcher() as s:
            results = s.search(q)
            for result in results:
                print(result)

    def query_question(self, query=u"nederduits"):
        """
        simple method to query index
        TODO: return results
        """
        qp = QueryParser("question", schema=self.question_schema)
        q = qp.parse(query)
        with self.question_ix.searcher() as s:
            results = s.search(q)
            for result in results:
                print(result)

    def query_answer(self, query=u"nederduits"):
        """
        simple method to query index
        TODO: return results
        """
        qp = QueryParser("answer", schema=self.question_schema)
        q = qp.parse(query)
        with self.answer_ix.searcher() as s:
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
    squad_ir.mk_index(overwrite=True)
    squad_ir.index_docs()
    squad_ir.query_context("hello")
