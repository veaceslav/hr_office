import csv
from collections import namedtuple
from string import Template
import datetime
import re
import logging

ClassMarkerLink = namedtuple("ClassMarkerLink", "link password")
CandidateEntry = namedtuple("CandidateEntry", "name surname email job status apply_date phone")

CLASSMARKER_QUIZZES = { "Quant Analyst" : ClassMarkerLink("https://www.classmarker.com/online-test/start/?quiz=4rj5fa92fc7a80ee", "abc123"),
                        "Graduate Trader" : ClassMarkerLink("https://www.classmarker.com/online-test/start/?quiz=gcd5f9bfed0754e3", "abc123"),
                        "Experienced Trader" : ClassMarkerLink("https://www.classmarker.com/online-test/start/?quiz=gqa5fa92f76e1832", "abc123")}

def create_classmarker_link(candidate):
    if candidate.job not in CLASSMARKER_QUIZZES:
        return None, "Job: " + candidate.job + " not in the list of classmarker Quizzes"

    return CLASSMARKER_QUIZZES[candidate.job].link + "&cm_fn=" + candidate.name\
           + "&cm_ln=" + candidate.surname.replace(" ", "%20") \
           + "&cm_e=" + candidate.email, None

def create_email(candidate):

    if not candidate.name:
        return None, "Candidate with no name"

    if not candidate.job:
        return None, "Missing job description: Candidate " + str(candidate)

    clasmarker_link, link_error = create_classmarker_link(candidate)

    if link_error:
        return None, link_error
    d = {
        'applicant_name': candidate.name,
        'job_position' : candidate.job,
        'classmarker_test_link': clasmarker_link,
        'classmarker_test_password' : CLASSMARKER_QUIZZES[candidate.job].password,
        'test_deadline': (datetime.date.today() + datetime.timedelta(days=7)).strftime(" %d %b %Y")
    }

    with open('quant_analyst_template.txt', 'r') as f:
        src = Template(f.read())
        result = src.substitute(d)

        return result, None

def parse_csv(filename):
    try:
        with open(filename, 'r') as csvfile:
            transactions = csv.reader(csvfile, delimiter=';', quotechar='"')

            # skip the first row
            next(transactions)

            entries = []

            for row in transactions:
                if "New/Assess CV" in row[4]:
                    entries.append(CandidateEntry(row[0].split(" ")[0], " ".join(row[0].split(" ")[1:]),
                                                  row[1], row[2], row[4], row[6], row[7]))
    except Exception as e:
        return None, str(e)

    return entries, None

