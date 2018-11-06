import re

import requests, csv
from bs4 import BeautifulSoup


#
# This script for fetching data from  www.muhs.ac.in
# all results of students will be exported to csv file
#


def get_classes_seat(room, clas):  # this function get LIST of students from specified CLASS/COLLEGE
    post = requests.post(url="https://centres.muhs.edu.in/mnk/ug_res/cres_x4.asp",
                         data={'cr': 'BHMS-2015', 'cl': clas, 'sn': room})
    soup = BeautifulSoup(post.text, "lxml")
    result = []
    for j in range(len(soup.html.body.table.nextSibling.nextSibling.findAll("tr"))):
        result.append(
            [i.text.strip("\n") for i in soup.html.body.table.nextSibling.nextSibling.findAll("tr")[j].findAll("td")])
    seats = [i[0] for i in result]
    return seats


def get_scores(seats,
               clas):  # this function get result LIST of seats from get_classes_seat and crawl info for every seat/student
    students = {}
    for seat in seats:
        post_s = requests.post(url="https://centres.muhs.edu.in/mnk/ug_res/res_x4.asp",
                               data={'cr': 'BHMS-2015', 'cl': clas, 'sn': seat})
        soup_seat = BeautifulSoup(post_s.text, "lxml")
        student = {}
        ab = [j for j in [i.text for i in soup_seat.html.body.table.findAll("p")]]
        student['name'] = ab[2].split("-")[1]
        student['college'] = ab[3].split("-")[1].replace("\xa0", "")

        student['seat_st'] = ab[4].split("-")[1].split(" ")[0]

        student['prn_numb'] = ab[4].split("-")[2].strip()
        for subject_element in soup_seat.html.body.findAll("td", attrs={'align': "left", 'colspan': '2', 'height': 26}):
            subj = subject_element.text
            student[subj + "_theor"] = subject_element.nextSibling.nextSibling.text.strip("\n")
            student[subj + "_pract"] = subject_element.nextSibling.nextSibling.nextSibling.nextSibling.text.strip("\n")
            student[subj + "_total"] = subject_element.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.text.strip("\n")
            student['grand_total'] = \
            soup_seat.html.body.table.nextSibling.nextSibling.findAll("td", text='GRAND TOTAL')[
                0].nextSibling.nextSibling.text.replace("\n", "").replace("\r", "").replace("\xa0", "")
            student['stud_result'] = soup_seat.html.body.table.nextSibling.nextSibling.findAll("td", text='RESULT')[
                0].nextSibling.nextSibling.text.replace("\n", "").replace("\r", "").replace("\xa0", "")
        students[seat] = student
    return students


""" comment fields function with bug
def get_fieldnames(student_result):
    return sorted(sorted(list(list(studes.values())[0].keys()),key=lambda x:x[0]),key=lambda y:len(y))
"""


def get_fieldnames(student_result):
    s = sorted(list(student_result.keys()), key=lambda x: x[0])
    return sorted(s, key=lambda x: len(x))


clas = input("Input class:")
room = input("Input college code:")

seats = get_classes_seat(room, clas)
studes = get_scores(seats, clas)
fieldnames = get_fieldnames(list(studes.values())[0])
# exporting to csv
filename = "%s_class_%s_college_results.csv" % (clas, room)
with open(filename, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in sorted(list(studes.keys())):
        writer.writerow(studes[i])
