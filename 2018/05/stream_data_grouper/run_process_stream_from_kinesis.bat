call C:\Users\Nathan\Desktop\spark_test\venv\Scripts\activate.bat
set HADOOP_HOME=C:\Program Files\hadoop-3.0.0
spark-submit --jars lib/spark-streaming-kinesis-asl_2.11-2.3.0.jar,lib/spark-streaming_2.11-2.3.0.jar,lib/spark-streaming-kinesis-asl-assembly_2.11-2.0.0.jar,lib/hadoop-aws-3.1.0.jar process_stream_from_kinesis.py
