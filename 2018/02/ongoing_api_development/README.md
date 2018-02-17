# Task list

1) Rework, and optimize the python script “export_mixpanel_people.py“.
    - This is a second file, like the one you worked on before. The API is for [Mixpanel](https://mixpanel.com/help/reference/data-export-api).
    - I’d like to rework it so the memory consumption is optimized.
    - I’d like to extract the dataset based on a condition, specifically on a time frame. You can use the key 
    "$last_seen" >= Today – 7 (or something similar).
2) Create an application/script that can run as a job that will extract data from LinkedIn’s API.
    - I’ll need to start with [company data](https://developer.linkedin.com/docs/company-pages), but will clarify the 
    requirements to see if there are other objects, like job posting searches, ..etc.
    - I’d like to base these jobs on a specific time frame, so I can perform incremental loads to the warehouse.
3) Create an application/script that can run as a job that will extract data from our Google AdWords account.
    - All detail data if possible.
    - Again, I’d like to base this on a specific time frame.

# From the messages
- *This script ran much slower than the one you edited last time. I'd like to make sure it's using the correct methods 
to be optimized, so I do not experience problems like the other that I had. It does a complete dump of records. I'd 
like to pull an incremental amount similar to the way the other works. Do you need the other as a reminder?* 
(2018/02/09 6:49 AM)
- *I have python 2 and 3 on the server. I can use either (...) I can load other versions if needed*
- *you can add in the filter for a 7 day period?*
- *if we going to use Python 3 for future work, I'd rather keep consistent*
- *There is a parameter tag in the people file, which I think we can set a selector for a key $last_used*
    - *parameters = {'selector': '(properties["$last_seen"] >= "2018-02-01T00:00:00")'}*
- *the 2 datasets are joined by "distinct_id". The event has a "time" key. Is there a way to query the people records 
and just download those associated with the last 7 days of "distinct_id"s from events?*
- *we just have the 2 recordsets we import as tables. the Pk > Fk relationship is events.distinct_id = people.distinct_id*
- *from there we relate this to other data that's not important for this project*
- *I take these two json recordsets and import into mongodb. I use an upsert based on that distinct_id, so that's why 
I'm trying to get incremental exports*
- He does this daily, but he wants the records to go back a week because *some info gets updated from another system 
after the fact. And sometimes the import fails.*
- *background is this is web tracking from one of our websites (applications). when a user is doing actions in our 
website, mixpanel is caputuring those actions. all the other crap about these people and how we do business with them 
is in another database. we match these visitors to the other system and send a pk to mixpanel (in the sample data for 
people, you'll see a key "Cloudwall_id". That's our Pk for the other system*
- *I'm really trying to get the client that performed actions in mixpanel over the last 7 days. if it's not possible, 
then I'll just have to go with a complete dump.*
- He wants to have *everything available* from the Mixpanel database on the exported people.
- *I need to get the people data associated to the incremental actions (or more than 7 days as an overlap). If I can't 
have the API call find those peple who did actions in the last 7 days, I'll be left with dumping all people from 
actions in history.*
- *I need to get all distinct_ids from the people record set, but for performance, I hoped I could just grab the most recent*
- *it's not huge now, but will grow*
- Me: I suggest that we go through the results of the Events query, get the list of unique distinct_ids, and then query 
Mixpanel for the people records associated with those distinct_ids.
- *Let's try that if possible and see what performance is like. If acceptable. We go with it, and I'll ask you to 
supply 2 scripts one that queries, and the other that dumps full collection of records*
- *If the querying for the weekly records is too slow, we'll just try to optimize the full dumpand I'll use that*
- Me: I think the way to do this is to create a script and test it on a much smaller span of time, like 30 minutes
- Re: desired format for combining event and people data: *json, either 2 file or 1 will work. Let's try one file first.*

## Summary
- He wants you to download the events data for the past week, get the unique distinct_ids, then download the people data
associated with those distinct_ids, then combine that events data and people data into a single file.

# Important links
- https://mixpanel.com/help/reference/exporting-raw-data
    - This page contains the format of the "events" export that we need to use to get the list of distinct_ids (people) 
    who have had an event in the past week.
    - *This endpoint uses gzip to compress the transfer; as a result, raw exports should not be processed until the 
    file is received in its entirety.*
    - *Data returned from this endpoint is JSONL (newline-delimited JSON).*
- https://mixpanel.com/help/reference/data-export-api