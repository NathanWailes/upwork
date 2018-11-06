"""
The idea behind this solution is to make the code as easy as possible to adapt to different input streams and output
streams. All you need to do to adapt it is to change the InputStream class and OutputStream class, and the code is kind
of separated and not dependent on a particular implementation.
"""
import json
import time
from collections import Generator

from datetime import datetime
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream


def move_entries_from_the_input_stream_to_the_output_stream(input_stream):
    """ Note that the 'finally' blocks don't actually get executed if you manually stop the program, so they may not be
    necessary at all. Apparently it's OK in a situation like this to just let the OS garbage-collect whatever open
    connection you may have (whether it's to a file or a database) rather than closing it explicitly.

    :return:
    """
    try:
        output_stream = OutputStream()
        try:
            for entry in input_stream:
                output_stream.add_log_entry(entry)
        finally:
            output_stream.close()
    finally:
        input_stream.close()


class InputStream(Generator):
    """ I used https://stackoverflow.com/a/42983747/4115031 to guide me in creating a Generator class.
    """
    def __init__(self, aws_region, stream_name, kinesis_app_name,
                 stream_initial_position=InitialPositionInStream.LATEST, stream_checkpoint_interval=2,
                 spark_batch_interval=10):
        self.log_entries = []

        stream_endpoint = 'https://kinesis.' + aws_region + '.amazonaws.com'
        spark_context = SparkContext(appName=kinesis_app_name)

        spark_context.setLogLevel('WARN')

        spark_streaming_context = StreamingContext(spark_context, spark_batch_interval)

        kinesis_stream = KinesisUtils.createStream(spark_streaming_context, kinesis_app_name, stream_name,
                                                   stream_endpoint, aws_region, stream_initial_position,
                                                   stream_checkpoint_interval)

        def add_log_entry(rdd):
            print('/', end='')
            rdd.foreach(lambda record: self.log_entries.append(record))

        kinesis_stream.foreachRDD(add_log_entry)

        spark_streaming_context.start()

        spark_streaming_context.awaitTermination()

    def send(self, value):
        while True:
            return_value = self.log_entries.pop(0) if self.log_entries else None
            if not return_value:
                print('.', end='')
                time.sleep(0.1)
            else:
                print('record found')
                return json.loads(return_value)

    def throw(self, typ, val=None, tb=None):
        raise StopIteration

    def close(self):
        pass


class OutputStream:
    def __init__(self):
        self.output_file = open('example_output.txt', 'a')

        self.pending_minute_datetime = None  # We batch by the minute that the record arrived / was processed by us,
        # not by the minute that the record is actually dated (i.e. when it was created)

        self.pending_log_entries = []

    def add_log_entry(self, entry):
        current_datetime = datetime.now()
        current_minute_datetime = current_datetime.replace(second=0, microsecond=0)

        if current_minute_datetime != self.pending_minute_datetime:
            self._flush_pending_log_entries_to_output()

            self.pending_minute_datetime = current_minute_datetime
            self.pending_log_entries = []

        if self._entry_passes_filter(entry):
            self.pending_log_entries.append(entry)

    @staticmethod
    def _entry_passes_filter(entry):
        """ This is where you can hard-code filters.

        :param entry:
        :return:
        """
        if 'time' not in entry:
            return False

        return True

    def _flush_pending_log_entries_to_output(self):
        if self.pending_log_entries:
            current_batch_datetime_as_string = self.pending_minute_datetime.strftime('%Y-%m-%dT%I:%M:%S')

            sorted_log_entries = sorted(self.pending_log_entries, key=lambda d: d['time'])

            output_dict = {current_batch_datetime_as_string: sorted_log_entries}

            self.output_file.write(json.dumps(output_dict) + '\n')
            self.output_file.flush()
            print(current_batch_datetime_as_string)

    @staticmethod
    def _get_datetime_as_string(datetime_object):
        return datetime_object.strftime()

    def close(self):
        self.output_file.close()


if __name__ == '__main__':
    aws_region = 'us-west-1'
    stream_name = 'test'
    kinesis_app_name = 'test'
    input_stream = InputStream(aws_region, stream_name, kinesis_app_name)

    move_entries_from_the_input_stream_to_the_output_stream(input_stream)
