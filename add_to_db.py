from selenium import webdriver
from sys import argv
from csv import DictReader
import configparser, re
import pandas as pd

config = configparser.ConfigParser()
config.read('../.config.ini')
username = config['credentials']['username']
password = config['credentials']['passwd']
error_count = 0

browser = webdriver.Chrome()
browser.get("http://127.0.0.1:8000")
browser.find_element_by_name("username").send_keys(username)
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_id("login").click()

approved_files = []
for file in argv[2:]:
    try:
        data = pd.read_table(open(file, "r"), sep="\t")
        approved_files.append(file)
    except UnicodeDecodeError:
        print("unicode error in", file)
        error_count+=1

for file in approved_files:
    dr = DictReader(open(file, "r"), delimiter="\t")
    p = re.compile(r'.+, (.+), (.+)')
    patient_dict = {}
    for row in dr:
        patient_dict.update(row)
    try:
        browser.get("http://127.0.0.1:8000/patients/add/")
        browser.find_element_by_name('forename').send_keys(p.search(patient_dict['Patient Name:']).group(1))
        browser.find_element_by_name('surname').send_keys(p.search(patient_dict['Patient Name:']).group(2))
        browser.find_element_by_name('dob').send_keys(patient_dict['Date of Birth:'])
        browser.find_element_by_name('nhs_number').send_keys(patient_dict['NHS Number:'])
        browser.find_element_by_name('sex').send_keys(patient_dict['Sex:'])
        browser.find_element_by_name('ethnicity').send_keys(patient_dict['Ethnic Group:'])
        browser.find_element_by_name('#1_incident').send_keys(patient_dict['First incident:'])
        browser.find_element_by_name('dead_censor').send_keys(patient_dict['DOD:'])
        browser.find_element_by_name('snumber').send_keys(patient_dict['Hospital Number:'])
        if patient_dict['Deceased:'] == 'True':
            browser.find_element_by_id('deceased_t').click()
        else:
            browser.find_element_by_id('deceased_f').click()
        browser.find_element_by_id('save').click()
    except KeyError:
        print("Unable to add:", file, "due to column absence")
        error_count+=1


browser.find_element_by_link_text("Log out").click()
browser.close()
print('Number of erroneous files = ', error_count)