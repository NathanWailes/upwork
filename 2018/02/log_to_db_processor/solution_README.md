# How to run the program

### The main program (what the client asked for)
- To run log_processor.py, run `python log_processor.py "path_to_log_file" "path_to_sqlite_db"`
from the command line.
  - Alternatively, open up the file, scroll to the bottom, and set the paths manually, and then
  run the file from an IDE like PyCharm or Sublime Text 2.

### The tests
- There are two groups of tests: the tests within `test_log_processor.py` and the tests
within `test_database_handler.py`.
- To run the tests, open up one of the two files mentioned above in an IDE like PyCharm or Sublime Text 2
and run the file.

### Other files
- `generate_example_log.py` is just a modified version of the Python file given to me
by the client to simulate the gradual addition of log entries to a log file.
- `utils.py` just contains some code shared between the different Python files.
- `parse_log_entry.py` contains the code used to take a string representation of a log
entry and turn it into a key-value dictionary.
- `database_handler.py` contains the code used to create the database and add log entries
to it.

# How to do the queries requested by the client

#### Which merchants generate the most requests?
```
select merchant_id, count(timestamp) as num_requests
from log_entries
where merchant_id is not null
group by merchant_id
order by num_requests desc;
```

#### Which merchant requests take the most time (using Request Time field)?
```
select merchant_id, sum(request_time) as total_time_taken
from log_entries
where merchant_id is not null
group by merchant_id
order by total_time_taken desc;
```

#### Which merchants generate the most requests for a developer? (Using Developer App Id)
```
select developer_app_id, merchant_id, count(timestamp) as num_requests
from log_entries
where merchant_id is not null
      and developer_app_id is not null
group by developer_app_id, merchant_id
order by developer_app_id, num_requests desc;
```

#### Which URI patterns are the costliest?
```
select uri_pattern, sum(request_time) as total_time_taken
from log_entries
where uri_pattern is not null
group by uri_pattern
order by total_time_taken desc;
```

# Approach used in coding up the solution

1. First, figure out how to parse the log into individual entries.
2. Then, figure out how to parse each entry into its constituent keys and values.
3. Finally, store the keys and values in a sqlite database.

# Good-to-know

- The demo data (cos.log.zip) appears to contain the logs from an entire single day (1/30).
The logs begin at 00:00:00 and end at 23:59:58.
- The README says "The request UUID should be present in every log entry", but if you
look at the actual sample data you can see that that is not the case.