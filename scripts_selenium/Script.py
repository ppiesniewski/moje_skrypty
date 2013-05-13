from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Script(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://poczta.o2.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_script(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("login").clear()
        driver.find_element_by_id("login").send_keys("piesniu")
        driver.find_element_by_id("pass").clear()
        driver.find_element_by_id("pass").sen5d_keys("mirrors")
        driver.find_element_by_id("login-button").click()
        driver.find_element_by_css_selector("span.label > span.link").click()
        driver.find_element_by_id("composer-receivers").clear()
        driver.find_element_by_id("composer-receivers").send_keys("piesniu@o2.pl")
        driver.find_element_by_id("composer-subject").clear()
        driver.find_element_by_id("composer-subject").send_keys("jajaj")
        driver.find_element_by_css_selector("#composer-send > span.inner > span.label").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
