import csv
import configparser
from pymongo import MongoClient
import logging
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

logger = logging.getLogger('insert_text')
hdlr = logging.FileHandler('./insert_text.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


def insert_text(mongo_index_folder_path, host_name, port, db_name, collection_name,
                path_to_csv, field_name_in_csv_to_match_on, document_field_to_insert_tag_into, text_to_insert,
                insert_if_text_is_already_present_in_destination_field=True):
    phrases_to_search_for = get_csv_phrases_to_search_for(path_to_csv, field_name_in_csv_to_match_on)

    client = MongoClient(host_name, port)
    db = client[db_name]
    document_collection = db[collection_name]

    mongo_search_index = open_dir(mongo_index_folder_path)
    with mongo_search_index.searcher() as searcher:
        for phrase in phrases_to_search_for:
            for document in get_matching_documents_for_phrase(db, collection_name, mongo_search_index,
                                                              searcher, phrase):
                print("Found a document: %s" % str(document['_id']))
                if not insert_if_text_is_already_present_in_destination_field:
                    if isinstance(document[document_field_to_insert_tag_into], str) or isinstance(document[document_field_to_insert_tag_into], unicode):
                        if text_to_insert == document[document_field_to_insert_tag_into]:
                            continue
                    elif isinstance(document[document_field_to_insert_tag_into], list):
                        if text_to_insert in document[document_field_to_insert_tag_into]:
                            continue

                if isinstance(document[document_field_to_insert_tag_into], str) or isinstance(document[document_field_to_insert_tag_into], unicode):
                    list_of_values = [document[document_field_to_insert_tag_into]]
                    list_of_values.append(text_to_insert)
                    document[document_field_to_insert_tag_into] = list_of_values
                elif isinstance(document[document_field_to_insert_tag_into], list):
                    document[document_field_to_insert_tag_into].append(text_to_insert)
                else:
                    logger.error('Invalid type to insert into for document ID: %s' % str(document['_id']))
                    continue

                document_collection.replace_one({'_id': document['_id']}, document, upsert=False)

    print("Done.")


def get_matching_documents_for_phrase(db, collection_name, mongo_search_index, searcher, phrase):
    query = QueryParser("content", mongo_search_index.schema).parse(phrase)
    results = searcher.search(query, limit=None)
    document_object_ids = [result['mongodb_id'] for result in results]
    documents = db[collection_name].find({'_id': {'$in': document_object_ids}})
    return documents


def get_csv_phrases_to_search_for(path_to_csv, field_name_in_csv_to_match_on):
    with open(path_to_csv) as csvfile:
        csv_data = csv.DictReader(csvfile)
        phrases_to_search_for = {row[field_name_in_csv_to_match_on] for row in csv_data}

    return phrases_to_search_for


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    _mongo_index_folder_path = config['database']['index_folder_path']
    _host_name = config['database']['host_name']
    _port = int(config['database']['port'])
    _db_name = config['database']['db_name']
    _collection_name = config['database']['collection_name']
    _path_to_csv = config['csv']['path']
    _field_name_in_csv_to_match_on = config['csv']['field_to_match_on']
    _document_field_to_match_on = config['mongo_document']['field_to_match_on']
    _document_field_to_insert_tag_into = config['mongo_document']['field_to_insert_text_into']
    _text_to_insert = config['mongo_document']['text_to_insert']
    _insert_if_text_is_already_present_in_destination_field = config.getboolean('mongo_document', 'insert_if_text_is_already_present_in_destination_field')

    insert_text(_mongo_index_folder_path, _host_name, _port, _db_name, _collection_name,
                _path_to_csv, _field_name_in_csv_to_match_on,
                _document_field_to_insert_tag_into, _text_to_insert,
                _insert_if_text_is_already_present_in_destination_field)
