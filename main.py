import sys
from getpatientdetails import GetPatientDetails, GetFirstAppointment
from webformhandler import WebHandler
from bs4 import BeautifulSoup
from csv import DictWriter
import pandas as pd

### This section is for using selenium to get to the information remotely ###
page = sys.argv[1]
snumbers = pd.read_csv("C:/Users/felix.woodhead/Documents/NoDupMDT.csv")
handler = WebHandler()

for snumber in snumbers['HospNo']:
    try:
        handler.go_to_page(page)
        handler.go_to_frame()
        handler.search_patient(snumber)
        handler.click_patient()
        handler.view_details()

        ### This section is for parsing the patient info from the ICE database ###

        gpd = GetPatientDetails()
        gfa = GetFirstAppointment()
        bs = BeautifulSoup(handler.get_source(), 'lxml')

        # Step 1: get the patient info table
        patient_table = gpd.get_patient_table(bs)

        # Step 2: get the table rows that contain the relevant information
        patient_rows = gpd.get_patient_info(patient_table)
        patient_rows_string = "".join(patient_rows)
        patient_rows = patient_rows_string.split(sep="\n")

        # Step 3: create the dict containing the patient information
        patient_dict = gpd.clean(patient_rows)
        patient_dict = gpd.addDOD(patient_dict)

        # Step 4: get the table with the patient locations
        appointment_table = gfa.get_location_table(bs)

        # Step 5: get the first date the patient came to the doctor about ILD
        location_rows = gfa.get_location_info(appointment_table)
        location_rows_string = "".join(location_rows)
        location_rows = location_rows_string.split(sep="\n")
        inicident_date = gfa.first_incident_date(location_rows)

        # Step 6: add the date to the patient_dict
        patient_dict.update({'First incident:': inicident_date})

        # Step 7: save information to a tab separated file named after the NHS number
        outfile = open(patient_dict["NHS Number:"] + ".tsv", "w")
        dw = DictWriter(outfile, patient_dict.keys(), delimiter="\t")
        dw.writeheader()
        dw.writerow(patient_dict)

    except Exception:
        handler.go_to_page(page)

handler.close_browser()