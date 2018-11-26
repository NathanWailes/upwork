# This code is based on the example at https://googleapis.github.io/google-cloud-python/latest/bigquery/index.html#

from google.cloud import bigquery

bigquery_client = bigquery.Client()

project_id = "XXXXXXXXXXXXXXXXX"
bigquery_dataset_id = 'XXXXXXXXXXXXXXXXX'
bigquery_template_table_id = 'XXXXXXXXXXXXXXXXX'


def get_training_set_size(training_set_id):
    template_suffix = training_set_id.replace('-', '_')
    table_id = "%s.%s.%s%s" % (project_id, bigquery_dataset_id, bigquery_template_table_id, template_suffix)

    QUERY = ('select count(*) from `%s`' % table_id)
    query_job = bigquery_client.query(QUERY)
    rows = query_job.result()

    for row in rows:
        return row[0]
