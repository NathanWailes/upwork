import os


def create_credentials_and_run_subscriber():
    with open('./google_application_credentials.json', 'w') as credentials_file:
        credentials_file.write(os.environ['GOOGLE_APPLICATION_CREDENTIALS_PLAINTEXT'])

    # We need to create the credentials file before running this import, because on import the Google clients will be
    # created, which require the credentials file to exist.
    from pull_pubsub_messages import pull_pubsub_messages

    pull_pubsub_messages()


if __name__ == '__main__':
    create_credentials_and_run_subscriber()
