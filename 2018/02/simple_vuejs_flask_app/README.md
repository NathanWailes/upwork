# Assignment

## Job post

I need a simple single page app to display results from my python script. I have some experience with Flask so would like to use 
that as a backend. I am also wanting to learn Vuejs, so it would be great if I could follow along with the development.

basic idea:
- Area for user to upload txt file (drag and drop and click for file explorer), and a text input for user to give a title to 
the file. Title is stored in database.

- Titles are displayed on the front end in a grid/table with title on the left and 5-star rank on the right. User can select 
a rating for each title and the order of titles will change based on rating (sorted high to low).
- Account creation so that only one account can vote once on each title.

- File is sent to Flask which is then used as input for python script
- Flask returns output from python script
- Output is displayed on the front end (output will be one or more strings)

Also looking for a clean and visually appealing design - something simple where the output display is top center, drag and 
drop upload below that, and the title rating grd on the bottm.

## Messages

for a little more context, the input txt files are movie scripts and my python script will predict the genres of the movie. the 
rating area is just movie title on the left and movie rating on the right (out of 5 stars). to store the titles/ratings I think 
sqlite3 will suffice. I wrote some of the database stuff briefly in flask, but it's not necessary to use if you have a better 
method:
- app.py (attachment)
- data.db (attachment)
