# ir_hacking
This project's objective is to demonstrate how an IR system can be created for a QA system using simple light weight components.

Instead of the typical java based components such as Lucene, Solr and Elasticsearch we use the Whoosh project (https://whoosh.readthedocs.io/en/latest/intro.html)

Whoosh is written in Python, is light weight, does not require a saperate server process and is very similar to Lucene.

## To run
git clone https://github.com/masonnlp/ir_hacking

cd ir_hacking

pipenv install

pipenv shell

python3 ir_example.py
