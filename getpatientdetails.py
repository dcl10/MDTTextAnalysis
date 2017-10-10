import datetime, bs4, re


class GetPatientDetails():

    # This method retrieves the patient information table from the ICE html page containing it.
    # The patient_soup parameter is a BeautifulSoup object.
    def get_patient_table(self, patient_soup):
        table = patient_soup.find("table", {"id": "patientDetailTable"})
        return str(table)

    # This method the rows from the table in the patient info table extracted by get_patient_table().
    # The table parameter is a string containing the html of the patient info table.
    # The titles list contains text from the table rows from the patient info table.
    def get_patient_info(self, table):
        titles = []
        table_soup = bs4.BeautifulSoup(table, "lxml")
        for tag in table_soup.find_all("tr", {"class": "title"}):
            titles.append(tag.text)
        return titles

    # This method cleans out empty array elements from the patient info table rows and builds a dict from the
    # remaining data.
    # The parse_lines parameter is a list that will be converted to a dict called patient_dict.
    # The returned dict (patient_dict) contains the fully parsed patient information.
    def clean(self, parse_lines):
        patient_dict = {}
        for line in parse_lines:
            if line is '':
                parse_lines.remove(line)

        for line in range(len(parse_lines)):
            if re.match('.+:', parse_lines[line]):
                patient_dict.update({parse_lines[line]:parse_lines[line+1]})

        return patient_dict

    # This method checks the record for a date of death. If there is no date of death, a date of censor is added
    # as the current date in the same format as a date of death would appear (e.g. 01 Jan 2017).
    # The patient_dict argument is a dict variable that will be searched. The updated patient_dict is returned to
    # the main.
    def addDOD(self, patient_dict):
        if 'DOD:' not in patient_dict.keys():
            patient_dict.update({"Deceased:": False})
            patient_dict.update({'DOD:': datetime.date.today().strftime('%d %b %Y')})
        else:
            patient_dict.update({"Deceased:": True})
        return patient_dict

class GetFirstAppointment():

    def get_location_table(self, patient_soup):
        table = patient_soup.find("table", {"id": "patientLocationTable"})
        return str(table)

    def get_location_info(self, table):
        titles = []
        table_soup = bs4.BeautifulSoup(table, "lxml")
        for tag in table_soup.find_all("tr", {"class": "title"}):
            titles.append(tag.text)
        return titles

    # Note: this method gets the wrong first incident date. This must be found using: [insert program name]
    def first_incident_date(self, parse_lines):
        pattern = re.compile('\d{2}\s\w{3}\s\d{4}')
        string = "".join(parse_lines)
        dates = pattern.findall(string)
        return dates[0]