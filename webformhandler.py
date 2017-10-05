from selenium import webdriver
from selenium.webdriver.support.ui import Select

class WebHandler():

    def __init__(self):
        self.browser = webdriver.Ie()

    def go_to_page(self, url):
        self.browser.get(url)

    def go_to_frame(self, frame="Right"):
        self.browser.switch_to.frame(frame)

    def login_form(self, username="", passwd="", unfield="txtName", pwfield="txtPassword", btnid="btnSubmit"):
        user_field = self.browser.find_element_by_name(unfield)
        user_field.send_keys(username)
        pass_field = self.browser.find_element_by_name(pwfield)
        pass_field.send_keys(passwd)
        button = self.browser.find_element_by_id(btnid)
        button.click()

    def pick_location(self, location, btn="btnSubmit", selection="selUserLocationIndex"):
        select = Select(self.browser.find_element_by_name(selection))
        select.select_by_value(location)
        button = self.browser.find_element_by_name(btn)
        button.click()

    def search_patient(self, snumber):
        search_bar = self.browser.find_element_by_name("PatientSearch1$txtSearch")
        button = self.browser.find_element_by_id("PatientSearch1_btnSearch")
        search_bar.send_keys(snumber)
        button.click()

    def click_patient(self, patient="dgrPatients"):
        self.browser.find_element_by_id(patient).click()

    def view_details(self):
        self.browser.find_element_by_link_text("View Details").click()

    def get_source(self):
        source = self.browser.page_source
        return source

    def close_browser(self):
        self.browser.close()
