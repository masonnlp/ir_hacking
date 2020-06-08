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

## Design notes

1. Solr is complex -- an alternative to solr is Elastic search 
2. Ideally need a module do explicit process control with like launching a server process saperately
3. No need to secure it saperately
4. You can run solr in process but it's not recommended and will still require the installation of java and the Solr binaries
5. Whoosh I looks like lucene from an API perspective
6. Whoosh is all python
7. Whoosh can be installed using pip
8. Whoosh can be run in process
