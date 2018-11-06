import os
from whoosh.index import create_in
from whoosh.fields import Schema, STORED, TEXT
import configparser
from pymongo import MongoClient
import logging

logger = logging.getLogger('create_mongo_search_index')
hdlr = logging.FileHandler('./create_mongo_search_index.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


def create_mongodb_search_index(index_folder_path, host_name, port, db_name, collection_name,
                                document_field_to_match_on):
    writer = get_search_index_writer(index_folder_path)
    documents = get_mongodb_documents(host_name, port, db_name, collection_name)

    for mongo_document_index, document in enumerate(documents):
        if isinstance(document[document_field_to_match_on], str) or isinstance(document[document_field_to_match_on], unicode):
            writer.add_document(mongodb_id=document['_id'],
                                content=document[document_field_to_match_on])
        elif isinstance(document[document_field_to_match_on], list):
            for value in document[document_field_to_match_on]:
                if not (isinstance(value, str) or isinstance(value, unicode)):
                    logger.error('Invalid value for document ID: %s' % str(document['_id']))
                    continue

                writer.add_document(mongodb_id=document['_id'],
                                    content=value)
        else:
            logger.error('Invalid value for document ID: %s' % str(document['_id']))
            continue

        if mongo_document_index % 10000 == 0:
            print("Committing %d" % mongo_document_index)
    writer.commit()


def get_search_index_writer(index_folder_path):
    mongodb_search_index_schema = Schema(mongodb_id=STORED,
                                         content=TEXT(stored=True))

    if not os.path.exists(index_folder_path):
        os.makedirs(index_folder_path)

    index = create_in(index_folder_path, mongodb_search_index_schema)
    writer = index.writer()

    return writer


def get_mongodb_documents(host_name, port, db_name, collection_name):
    client = MongoClient(host_name, port)
    db = client[db_name]

    document_collection = db[collection_name]
    documents = document_collection.find()

    return documents


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    index_folder_path = config['database']['index_folder_path']
    host_name = config['database']['host_name']
    port = int(config['database']['port'])
    db_name = config['database']['db_name']
    collection_name = config['database']['collection_name']
    document_field_to_match_on = config['mongo_document']['field_to_match_on']

    create_mongodb_search_index(index_folder_path, host_name, port, db_name, collection_name, document_field_to_match_on)
