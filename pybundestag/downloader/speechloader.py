# -*- coding: utf-8 -*-

# Import modules
from selenium import webdriver
import re
import time


# Collect Links
def get_links(browser = "Firefox"):
    """
    This function will return the links
    to the five most recent Bundestag
    protocols in XML format. You can
    use those links in your scripts
    to download these links.
    """
    # Open Website in Selenium
    browser = browser.lower()
    if browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "ie":
        driver = webdriver.Ie()
    driver.get("https://www.bundestag.de/services/opendata")
    
    # List all Documents
    links_result = []
    counter = 1
    while (len(links_result) == 0) and (counter < 10):
        docs = driver.find_elements_by_class_name("bt-documents-description")
        protocols = [x for x in docs if re.match("^Plenarprotokoll der ", x.text) is not None]
        links = [x.find_element_by_class_name("bt-link-dokument") for x in protocols]
        links_result.extend([x.get_attribute("href") for x in links])
        if len(links) == 0:
            time.sleep(1)
            counter += 1
    
    # Close Selenium Driver
    driver.close()
    
    # Return Link List
    return(links_result)
    
