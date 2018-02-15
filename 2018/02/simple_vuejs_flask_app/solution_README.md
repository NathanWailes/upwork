# How to use the program

## Python version used in development
3.5.2

## How to create the database
Run `create_database.py`.


# My plan of attack
1. Create a Flask website that just returns an `index.html` page.
1. Add a simple empty Vue.js in-page application.
1. Allow the user to select a title and have that data POSTed to the server, and then get a response.
1. Have any submitted title added to a database.
1. Have the database queried to populate a displayed list of titles on the index.html page.
1. Allow the user to upload a file (not with drag-and-drop) with input and have the output displayed on-screen.
1. Allow the user to vote on titles.
1. Query an IP server to get the client's IP address as a quick-and-dirty way to limit votes.
    - https://stackoverflow.com/questions/391979/how-to-get-clients-ip-address-using-javascript-only
1. Optional: Add drag-and-drop functionality.
    - https://scotch.io/tutorials/how-to-handle-file-uploads-in-vue-2
1. Add styling.