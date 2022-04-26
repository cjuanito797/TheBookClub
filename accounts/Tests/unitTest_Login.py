import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ll_ATS (unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Safari ( )

    def test_ll(self):
        driver = self.driver
        driver.maximize_window ( )
        driver.get ("http://127.0.0.1:8000/")
        time.sleep (3)



def tearDown(self):
    self.driver.close ( )


if __name__ == "__main__":
    unittest.main ( )
