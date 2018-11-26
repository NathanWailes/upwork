import json
from functools import wraps
from uuid import uuid4


from flask import Flask, Response, request
from google.cloud import bigquery, pubsub_v1, exceptions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Set up the Google BigQuery client
bigquery_client = bigquery.Client()
bigquery_dataset_id = 'LogLeapTraining'
bigquery_dataset_ref = bigquery_client.dataset(bigquery_dataset_id)
bigquery_dataset = bigquery.Dataset(bigquery_dataset_ref)

# Set up the BigQuery template table
bigquery_template_table_id = 'LogLeapTrainingTemplate'
bigquery_template_table_ref = bigquery_client.dataset(bigquery_dataset_id).table(bigquery_template_table_id)
bigquery_template_table = bigquery_client.get_table(bigquery_template_table_ref)

# Set up the Google Pub/Sub client so we can use it for the /train/<training_set_id> route:
project_id = "logleap-223119"
topic_name = "logleap_train"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

# Set up Firestore
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})
db = firestore.client()
firestore_training_sets_metadata_collection = db.collection('LogLeapTraining')


def valid_training_set_id_required(view_function):
    """ Important: This validator requires the training set ID to be the first argument to the view function.

    :param view_function:
    :return:
    """
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        training_set_id = kwargs['training_set_id']
        firestore_document_reference = firestore_training_sets_metadata_collection.document(training_set_id)
        try:
            # TODO: Get Firestore permissions working so this call will work.
            firestore_document = firestore_document_reference.get()
        except exceptions.NotFound:
            return Response(json.dumps({}), status=404, mimetype='application/json')

        return view_function(*args, **kwargs)

    return wrapper


@app.route('/data', methods=['POST'])
def create_training_set():
    """ The user makes an initial POST to this endpoint to announce a new training set is going to be uploaded.  The
    user gets an identifier for that dataset in return.

    :return:
    """
    training_set_id = str(uuid4())
    data = {
        'id': training_set_id,
        'status': 'created'
    }

    # Code from https://firebase.google.com/docs/firestore/manage-data/add-data
    # TODO: Make sure this is storing the document to Firestore.
    db.collection('LogLeapTraining').document(training_set_id).set(data)

    return Response(json.dumps({'status': 'OK',
                                'dataId': training_set_id}),
                    status=201, mimetype='application/json')


@app.route('/data/<training_set_id>', methods=['POST'])
@valid_training_set_id_required
def add_training_set_entry(training_set_id):
    """ After creating a new training set, the user uses this endpoint to POST a number of entries to the set. We
    expect the client to structure each entry to include a timestamp, the key message, and optionally some context data.

    :param training_set_id:
    :return:
    """
    training_set_entry_content = request.form.get('data')

    # The schema is:
    # timestamp segmentId owner content context
    # TODO: Confirm that the timestamp is the timestamp of the original content
    rows_to_insert = [
        ("2014-09-27T12:30:00.45Z", training_set_id, "Example API Key", training_set_entry_content, "example context"),
    ]

    # We are going to have BigQuery create a new table for this training set if necessary (i.e. if they haven't already
    # created the table for us).  To do this we supply a "template suffix" which they will add to the end of the name
    # of the template table we're specifying to determine the name of the new table to create.
    template_suffix = training_set_id.replace('-', '_')  # The BigQuery template suffix can't include the "-" character.

    errors = bigquery_client.insert_rows(bigquery_template_table, rows_to_insert, template_suffix=template_suffix)

    assert errors == []
    return Response(json.dumps({}), status=204, mimetype='application/json')


@app.route('/train/<training_set_id>', methods=['POST', 'GET'])
@valid_training_set_id_required
def train(training_set_id):
    """
    ## POST

    Starts the training logic.

    Example message that will be published to Pub/Sub:

    Message {
        data: b'923984af-b256-41e7-88d4-d04784078eaf'
        attributes: {}
    }

    ## GET

    Returns the current status of the training:

    - idle: training was not requested yet
    - training: training is ongoing
    - ready: training has been completed and sent to the scoring agent

    :param training_set_id:
    :return:
    """
    if request.method == 'POST':
        # Publish a message to Google Pub/Sub indicating that this training set should now be trained on.
        data = training_set_id
        # Data must be a bytestring
        data = data.encode('utf-8')
        # When you publish a message, the client returns a Future.
        message_future = publisher.publish(topic_path, data=data)

        return Response("", status=204, mimetype='application/json')
    elif request.method == 'GET':
        status = None

        # TODO: Make sure this retrieves the status correctly.
        firestore_document_reference = firestore_training_sets_metadata_collection.document(training_set_id)
        try:
            firestore_document = firestore_document_reference.get()
            status = firestore_document.status
        except exceptions.NotFound:
            print(u'No such document!')

        return Response(json.dumps({'status': status}), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
