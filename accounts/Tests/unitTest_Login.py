import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ll_ATS (unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Safari ( )

    def test_ll(self):
        user = "cjuangas17@gmail.com"
        pwd = "Boxing129"


        driver = self.driver
        driver.maximize_window ( )
        driver.get ("http://127.0.0.1:8000/account/login/")
        time.sleep (1)
        elem = driver.find_element_by_id ("id_username")
        elem.send_keys (user)
        elem = driver.find_element_by_id ("id_password")
        elem.send_keys (pwd)
        time.sleep (1)

        # click on the login button
        driver.find_element_by_xpath("/html/body/div[1]/form/p/input").click()
        time.sleep(3)




def tearDown(self):
    self.driver.close ( )


if __name__ == "__main__":
    unittest.main ( )
