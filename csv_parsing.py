import csv
from collections import namedtuple
from string import Template
import datetime
import re
import logging

ClassMarkerLink = namedtuple("ClassMarkerLink", "link password")
CandidateEntry = namedtuple("CandidateEntry", "name surname email job status apply_date")

CLASSMARKER_QUIZZES = { "Quant Analyst" : ClassMarkerLink("https://www.classmarker.com/online-test/start/?quiz=4rj5fa92fc7a80ee", "abc123")}

def create_classmarker_link(candidate):
    if candidate.job not in CLASSMARKER_QUIZZES:
        return "", "Job" + candidate.job + " not in the list of classmarker Quizzes"

    return CLASSMARKER_QUIZZES[candidate.job].link + "&cm_fn=" + candidate.name\
           + "&cm_ln=" + candidate.surname.replace(" ", "%20") \
           + "&cm_e=" + candidate.email

def create_email(candidate):
    d = {
        'applicant_name': candidate.name,
        'job_position' : candidate.job,
        'classmarker_test_link': create_classmarker_link(candidate),
        'classmarker_test_password' : CLASSMARKER_QUIZZES[candidate.job].password,
        'test_deadline': (datetime.date.today() + datetime.timedelta(days=7)).strftime(" %d %b %Y")
    }

    with open('quant_analyst_template.txt', 'r') as f:
        src = Template(f.read())
        result = src.substitute(d)

        return result

def parse_csv(filename):
    with open(filename, 'r') as csvfile:
        transactions = csv.reader(csvfile, delimiter=';', quotechar='"')

        # skip the first row
        next(transactions)

        entries = []

        for row in transactions:
            if "New/Assess CV" in row[4]:
                entries.append(CandidateEntry(row[0].split(" ")[0], " ".join(row[0].split(" ")[1:]), row[1], row[2], row[4], row[6]))

    return entries

