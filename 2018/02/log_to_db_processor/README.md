# log-parsing

 This task requires you to create an application to process “real time” logs and store the processed information in a data store of your choice.  How you plan to implement this is completely up to you but the data should be processed and available in as real time as possible. 
 
 The data store you chose is not important here. What is important is the data model as well as the quality of your code. Remember that this is supposed to work againsst a file that is being appended to over long periods of time. It is also possible that the file may not get logs appended to it for large chunks of time. Even though the file in this example is relatively tiny (300MB) this application should be able to process very large files without requiring an increase in resources. 
 
* The way you structure your schema is up to you but it should allow flexibility in the query patterns.  Most query patterns will filter based on Timestamp, Merchant, Developer App ID, and URI Pattern. The data model you choose should be able to answer questions like the following: 
	* Which merchants generate the most requests?
	* Which merchant requests take the most time (using Request Time field)?
	* Which merchants generate the most requests for a developer? (Using Developer App Id)
	* Which URI patterns are the costliest?
	* Unique requests grouped by different  fields.

* After cloning this project, please start the `proxy_logs.py` script that will output a log called `cos-1.log`.. This will be spitting out log statements to `cos-1.log` at random intervals. 

```
					python proxy_logs.py
```

### Log Structure:
```
- Timestamp - [2018-01-30 00:00:00.000]
- Log Level - [INFO], Possible Options: [DEBUG, INFO, WARN, ERROR]
- URI - u=/v3/merchants/DPA9VR0WM805Y/employees - This is the resource the client is trying to access. 
- URI Pattern -  p=/v3/merchants/{mId}/employees - This is the template of the resource the client is trying to access. 
- Request UUID - r=84098095-7420-18a5-3e16-7c392ba98c64 - Unique identifier per client request. 
- Device UUID - d=7412A5DAD2C24AB1B006B98DA6F6DD2C - Unique identifer for a client device. 
- Merchant ID - m=2278 - Unique identifier for a merchant. 
- Version ID - v=1914 - App verison id
- Request IP - i=50.249.120.58 - IP address of the client. 
- HTTP Method - hm=GET - HTTP Method. Possible Options : [GET, HEAD, PUT, POST]
- HTTP Status - hs=200 - HTTP Status Code
- Developer App ID - da=123 - Unique identifier for a developer. 
- Auth Mechanism - am=APP - Request authentication mechanism. Possible Options: [NONE, APP, DASHBOARD, INVALID, API, URI, INTERNAL].
- Request Time - t=3 in milliseconds. Time spent processing this request.
- Log statement - These can be in various formats. 
    1. RequestLog{uQ=expand=roles&expand=employeeCards&limit=1000&offset=0, rspBody={"href":"http://apisandbox.dev.clover.com/v3/merchants/DPA9VR0WM805Y/employees?offset=0&limit=1000","elements":[{"id":"F46CZ7FQ73GC4","name":"Jamie Zimmerman","nickname":"Jamie Z.","email":"jamiezimmerman@quantumgo.com","inviteSent":false,"claimedTime":1479828425000,"pin":"1234","role":"ADMIN","roles":[{"id":"D6D7M1HXHNTS0","element":{"id":"D6D7M1HXHNTS0","name":"admin","systemRole":"ADMIN"}}],"isOwner":true,"employeeCards":[]}]}, host=sandbox, cT=2018-01-29T23:59:59.996Z, aId=7527}
    2. Returning order count: 0, orders (limit of 50)
- Logging Class - (FileRequestObjectLogger) - The class that logged this line. 

* The Request UUID is unique per external client request and should be present on every log statement.
* Log statements are either informative or are capturing request and response information. Statements that begin with "RequestLog" are only logged once per client request. 
* It is possible for log statements to span multiple lines. 
* Timestamp, Log Level, Request UUID and Logging Class are the only fields that are guaranteed to be populated on each log. Based on the Auth Mechanism, it is possible that certain fields will not be populated. For instance, am=API will not have Device UUID populated. 
```


Please provide some documentation on how to run the application.


***NOTE*** :
If you finish early, try to design this application in manner where it can process multiple files in a distributed manner. 
