# README

## The assignment

The goal of the project is to provide a backend to an API that implements the following user story:


1. Client initiates a new upload of a data set, and a unique ID is returned
1. Client posts JSON entries to the API
1. Backend stores JSON entries into Google Bigquery
1. The client initiates the processing of the data by posting to the API. The API adds a message indicating there is data to be processed to pub/sub.
1. the API provides a sample function for picking up the pub/sub task. For this task, we will limit to a sample task that just queries the BigQuery storage to counts the total number of lines in the data set.(in production this function will be a separate google cloud function that is automatically triggered by the pub/sub)

All metadata in this process (unique ID, processing state) is maintained in a firestore database.

The application should be developed in Flask (Python 3) for local testing (production will use google cloud functions for the data transfer, and a VM for the client processing).

The ideal developer has experience with both Flask and developing for the google cloud platform.

---

I'll take the oppoertunity to give some more background on the project. This is a component in a machine learning platform that takes in (industrial or IT) log information and calculates a model on it for anomaly detection. The training data is pushed through the platform, using the API, at regular time intervals (typically during test runs following configuration changes or maintenance), and used in a number of ways later on (e.g. we have a tool to speed up root cause analysis).

Just for completeness: the sample dataset that i sent you is a simple timestamp/message combination from a .NET application log (the actual product used more complex data, but the principle stays the same). I've set-up the bigquery table with the following fields:

```
timestamp	TIMESTAMP	REQUIRED	
segmentId	STRING	REQUIRED	
owner	STRING	NULLABLE	
content	STRING	REQUIRED	
context	STRING	NULLABLE
```
timestamp/content map to the incoming timestamp/message. Context you can ignore. owner will be an API key used to call the API (not really in scope for the project to implement) and segmentId is the same as the "dataId" in the API specification.

To add data to bigquery, best read up on streaming inserts (https://cloud.google.com/bigquery/streaming-data-into-bigquery).

---

#### Some clarification

the API is indeed used to initiate a new ML training cycle. For this, a client does:

1. an initial call to announce a new dataset is going to be uploaded, and gets an identifier for that dataset in return (i typically generate this with str(uuid4())). -> POST /data
1. a number of entries are posted. We expect the client to structure them into a timestamp, the key message and optional some context data. The sample i added to the sharepoint just has timestamp and a message string. (we do consultancy to structure it to fit the needs of a specific client: a machine log in a factory will be different than an IT log from telecom) -> multiple invocations of POST /data/dataId
1. once the full batch has been loaded, we initiate the training ) -> POST /train/dataId

The API stores the data in BigQuery, training logic will fetch it from there. Firestore is used to create a log that a dataset with that dataId has been created for that user, and updated when training starts (which can be coupled to a cloud function, and trigger the actual training).

## List of links sent to me by the client

### Project links
- [Firestore](https://console.cloud.google.com/firestore/data?project=logleap-223119)
- [BigQuery table](https://console.cloud.google.com/bigquery?project=logleap-223119)
- [API Documentation](https://logleap-training.docs.stoplight.io/)
- [Dataset and OpenAI spec](https://leapstation-my.sharepoint.com/:f:/g/personal/steven_leapstation_eu/Eo-1jbk3jWxNhsVdTIEzS8gBtJcJHtcu3vEvvIFPi-QaGQ?e=QKVgag)

### Reference links
- [Streaming data into BigQuery](https://cloud.google.com/bigquery/streaming-data-into-bigquery)

## Notes from Nathan

- Each LeapStation dataset (training set) will be a separate table within a single BigQuery dataset (you could think of
it as the "training sets" dataset).
- "Once processed we'll archive the [training] table to disk. So there won't be millions of tables"

## Setup

- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your Google API key `.json` file.

### Docker

1. Build the Docker image: `docker build -t logleap-pubsub-subscriber .`
1. Run the image: `docker run -it -e GOOGLE_APPLICATION_CREDENTIALS_PLAINTEXT='<contents of credentials JSON with newlines removed>' logleap-pubsub-subscriber`
    - Note the single-quotes surrounding the environment variable's value.
    - The `-it` flag is to make the container's STDOUT show up in the Docker window you have open. 