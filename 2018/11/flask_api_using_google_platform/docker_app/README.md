### Setup

1. Build the Docker image: `docker build -t logleap-pubsub-subscriber .`
1. Run the image: `docker run -it -e GOOGLE_APPLICATION_CREDENTIALS_PLAINTEXT='<contents of credentials JSON with newlines removed>' logleap-pubsub-subscriber`
    - Note the single-quotes surrounding the environment variable's value.
    - The `-it` flag is to make the container's STDOUT show up in the Docker window you have open. 