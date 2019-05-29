# -*- coding: utf-8 -*-

# Import modules
from selenium import webdriver
import re



# Collect Links
def get_links():
    """
    This function will return the links
    to the five most recent Bundestag
    protocols in XML format.
    """
    # Open Website in Selenium
    driver = webdriver.Firefox()
    driver.get("https://www.bundestag.de/services/opendata")
    
    # List all Documents
    docs = driver.find_elements_by_class_name("bt-documents-description")
    protocols = [x for x in docs if re.match("^Plenarprotokoll der ", x.text) is not None]
    links = [x.find_element_by_class_name("bt-link-dokument") for x in protocols]
    links = [x.get_attribute("href") for x in links]
    
    # Close Selenium Driver
    driver.close()
    
    #Return Link List
    return(links)
    
