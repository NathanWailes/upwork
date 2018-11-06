import csv

from pymongo import MongoClient


def generate_tags(host_name, port, db_name, collection_name, path_to_csv, field_name_in_csv_to_match_on,
                  document_field_to_match_on, document_field_to_insert_tag_into,
                  field_names_in_csv_to_copy_over_to_tag=None):
    client = MongoClient(host_name, port)
    db = client[db_name]

    with open(path_to_csv) as csvfile:
        csv_data = csv.DictReader(csvfile)

        csv_keyword_to_row_data = {row[field_name_in_csv_to_match_on]: row for row in csv_data}

    document_collection = db[collection_name]
    documents = document_collection.find()

    for document in documents:
        for value in document[document_field_to_match_on]:
            if value in csv_keyword_to_row_data.keys():
                new_tag = csv_keyword_to_row_data[value]
                for csv_field_name in new_tag.copy().keys():
                    if field_names_in_csv_to_copy_over_to_tag and csv_field_name not in field_names_in_csv_to_copy_over_to_tag:
                        del new_tag[csv_field_name]
                document[document_field_to_insert_tag_into].append(new_tag)
                document_collection.replace_one({'_id': document['_id']}, document, upsert=False)


if __name__ == '__main__':
    host_name = 'localhost'
    port = 27017
    db_name = 'db_name'
    collection_name = 'collection_name'
    path_to_csv = 'Party1PythonInput.csv'
    field_name_in_csv_to_match_on = '_keyword'
    document_field_to_match_on = 'Party1'
    document_field_to_insert_tag_into = 'Party1Details'
    field_names_in_csv_to_copy_over_to_tag = ['_keyword', 'firstName', 'lastName', 'gender']
    generate_tags(host_name, port, db_name, collection_name, path_to_csv, field_name_in_csv_to_match_on,
                  document_field_to_match_on, document_field_to_insert_tag_into,
                  field_names_in_csv_to_copy_over_to_tag)
