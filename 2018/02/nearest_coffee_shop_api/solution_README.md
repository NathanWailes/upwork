# Instructions for using the solution
- The Python version used while developing the solution is `3.5.2`.
- You should add your Google Geocoding API key to settings.ini to get it to work. You can get one [here](https://developers.google.com/maps/documentation/geocoding/start#get-a-key).
- Just a heads up: I added the header "id, name, address, latitude, longitude" to the top of the CSV file for ease of use.
- The `requirements.txt` contains the list of packages you need to install to run the program. Use `pip install -r requirements.txt`
from your command line to install them.

## Running the server
1. Run `python api.py` from the command line to run the server.

## Running the tests
1. Run `python tests.py` from the command line.


# Example queries and responses

- I recommend using [Advanced REST Client](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo)
to send `GET` and `POST` requests to your `localhost` server.

## Create
### Request
- Method: POST
- URL: `http://localhost:5000/create`
- Body: `{"name": "a", "address": "b", "latitude": "c", "longitude": "d"}`

### Response
```
{"id": 57}
```

## Read
### Request
- Method: GET
- URL: `http://localhost:5000/read/1`

### Response
```
{"address": "986 Market St", "latitude": 37.782394430549445, "id": 1, "longitude": -122.40997343121123, "name": "Equator Coffees & Teas"}
```

## Update
### Request
- Method: POST
- URL: `http://localhost:5000/update/1`
- Body: `{"name": "a", "address": "b", "latitude": "c", "longitude": "d"}`

### Response
```
{"message": "Record updated."}
```

## Delete
### Request
- Method: POST
- URL: `http://localhost:5000/delete/1`

### Response
```
{"message": "Record deleted."}
```

## Nearest
### Request
- Method: GET
- URL: `http://localhost:5000/nearest/535+Mission+St.,+San+Francisco,+CA`

### Response
```
{"id": 16, "longitude": -122.39933341741562, "latitude": 37.78746242830388, "distance": 0.0017977987083765941, "name": "Red Door Coffee", "address": "111 Minna St"}
```