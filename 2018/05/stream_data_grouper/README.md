# Readme

## The assignment

### Background / overview

(Written by Nathan)

My client is a programmer who has a client of his own.

That client apparently has an AWS instance that is generating a
lot of logging-related data, and it's coming so rapidly and in such a volume that the existing database they have set up
to save these logging records cannot save the records as quickly as they are coming. My client's assignment is to
create a system that can save these logging records as quickly as they're coming.

To do this, he plans to create a program / system that will read from Amazon Kinesis, group the events by minute, sort 
each group internally by the events' datetimes, and then save each group to an OrientDB database (which is apparently a 
key-value database like MongoDB). And somehow the plan also involves using Docker and PySpark.

I told my client that I was unfamiliar with all of those tools, and so he suggested that I create a pure(?)-Python 
program that assumes the input is a file being constantly written to and the output is a file (rather than a database), 
and that he would then handle the task of modifying the code to use the above-mentioned other tools, since he was more
familiar with them.

### The deliverables / What my client wants

1. A generator script.
    - The script should continuously add messages to the "input" text file.

1. A processor script.
    - bite off per minute.
    - Order by created date within each group
    - keep a stream to an output file the entire time and re-use that every time.

1. Write unit tests that use the processor script to any degree.


## The solution

Created with Python 3.5.