## The Assignment

I am looking for someone skilled in Python to automate the download of reports from the Texas Judicial Branch database:

http://www.txcourts.gov/statistics/court-activity-database/

I will provide a shared cloud folder with a separate folder for each county in the state. From the following link:

https://card.txcourts.gov/ReportSelectionOld.aspx

I need to

(1) Select "district court data reports" in the "report type" menu. Select "district activity summary by case type" in the "report" menu. Click continue. For each of the years 2000-2010 (January to December - except for the year 2010, which only goes from January to August), for each county, choose "export to Excel" in the "format" menu, run the report, and save the file as "district_20xx" in the corresponding county folder within the shared cloud folder. The xx denotes the year of the report.

(2) Do the same thing but select "county-level court data reports" in the "report type" menu, then click "county activity summary by case type" in the report menu. Save each Excel report as "county_20xx" in the corresponding county folder.

I would love to see your code afterward if you don't mind sharing it.

If you have a preferred e-mail for sharing the cloud folder, please let me know, and I'll provide access.

## Nathan's notes

I completed this in about two hours, including the time I spent managing the program as it downloaded the files (it 
crashed several times when my WiFi stopped working or when I closed my laptop, so I needed to restart the program a few 
times).