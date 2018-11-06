from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream


conf = SparkConf(loadDefaults=False)


def print_record(rdd):
    print("========================================================")
    print("Starting new RDD")
    print("========================================================")
    rdd.foreach(lambda record: print(record.encode('utf8')))


if __name__ == "__main__":
    conf = SparkConf()
    conf.set('spark.jars.packages', 'org.apache.spark:spark-streaming-kinesis-asl_2.11:2.3.0')

    # conf.set('driver-memory', '2g')
    # conf.set('executor-memory', '2g')

    spark_context = SparkContext(appName="PythonStreamingKinesisWordCountAsl", conf=conf)

    print(spark_context.version)

    spark_streaming_context = StreamingContext(spark_context, 10)

    app_name = 'test'
    stream_name = 'test'
    endpoint_url = 'https://kinesis.us-west-1.amazonaws.com'
    region_name = 'us-west-1'

    dstream = KinesisUtils.createStream(spark_streaming_context, app_name, stream_name, endpoint_url, region_name,
                                        InitialPositionInStream.TRIM_HORIZON, checkpointInterval=10)

    dstream.foreachRDD(print_record)

    spark_streaming_context.start()

    spark_streaming_context.awaitTermination()
