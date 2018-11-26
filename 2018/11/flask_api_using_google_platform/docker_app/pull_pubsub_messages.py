import time
from google.cloud import pubsub_v1
from query_bigdata_table_size import get_training_set_size


def pull_pubsub_messages():
    project_id = "XXXXXXXXXXXXXXXXX"
    subscription_name = "XXXXXXXXXXXXXXXXX"

    subscriber = pubsub_v1.SubscriberClient()

    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        print(get_training_set_size(message.data.decode("utf-8")))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking. We must keep the main thread from
    # exiting to allow it to process messages asynchronously in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        print("waiting...")
        time.sleep(5)
