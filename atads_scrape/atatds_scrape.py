
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:54:04 2023

@author: pjhmx
"""
########################################################################
#
# Load libraries 
#
########################################################################


from selenium import webdriver
import time
from selenium.webdriver.common.by import By

########################################################################
#
# USER SETTING
#
########################################################################

do_year = "2000"

#######################################################################
#
# Set the target page URL 
#
#######################################################################

urlpage = 'https://aspm.faa.gov/opsnet/sys/airport.asp' 
print(urlpage)


#######################################################################
#
# Tell Chrome where to save downloaded data 
#
#######################################################################

options = webdriver.ChromeOptions()
profile = { 
    "download.default_directory": "C:/windows/Users/pjhmx/Desktop/", 
    "download.prompt_for_download": False
    }
options.add_experimental_option("prefs", profile)


#######################################################################
#
# Load the Chrome driver 
#
#######################################################################

driver = webdriver.Chrome(options=options)

#driver = webdriver.Chrome()

# get web page

######################################################################### 
#
# Activate the driver 
#
#########################################################################

driver.get(urlpage)


# execute script to scroll down the page
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s

######################################################################### 
#
# Wait for the driver to open and load the target page in a browser 
#
#########################################################################

time.sleep(30)
#driver.find_element_by_partial_link_text("opsnet").click()

#########################################################################
#
# Set BUTTON:REPORT parameters
#
#########################################################################

mylink=driver.find_element(By.ID,"b_repOpt")
print(mylink)
mylink.click()

driver.find_element(By.CSS_SELECTOR,"input[type='radio'][value='msexcel']").click()
driver.find_element(By.NAME,'nosubtot').click()
driver.find_element(By.NAME,'ifr').click()
driver.find_element(By.NAME,'vfr').click()

########################################################################
#
# Set BUTTON:DATE Parameters
#
########################################################################

mylink=driver.find_element(By.ID,"b_dSelector")
print(mylink)
mylink.click()

driver.find_element(By.ID,'RangeOption').click()
driver.find_element(By.XPATH,"//select[@name='fm_r']/option[text()='Jan']").click()
driver.find_element(By.XPATH,"//select[@name='fy_r']/option[text()="+do_year+"]").click()
driver.find_element(By.XPATH,"//select[@name='fd_r']/option[text()='1']").click()

driver.find_element(By.XPATH,"//select[@name='tm_r']/option[text()='Dec']").click()
driver.find_element(By.XPATH,"//select[@name='ty_r']/option[text()="+do_year+"]").click()
driver.find_element(By.XPATH,"//select[@name='td_r']/option[text()='31']").click()

#######################################################################
#
# Set BUTTON:FACILITIES parameters
#
#######################################################################

mylink=driver.find_element(By.ID,"b_locOpt")
print(mylink)
mylink.click()

#######################################################################
#
# Set BUTTON:FILTERS parameters
#
#######################################################################

mylink=driver.find_element(By.ID,"b_addOpt")
print(mylink)
mylink.click()

#######################################################################
#
# Set BUTTON:GROUP parameters
mylink=driver.find_element(By.ID,"b_groupSelector")
print(mylink)
mylink.click()


#######################################################################
#
# Build data request
#
#######################################################################

js = "addFld('DATE')"
driver.execute_script(js)  
js = "addFld('LOCID')"   
driver.execute_script(js)  
js = "addFld('STATE')"   
driver.execute_script(js)  
js = "addFld('REGION')"   
driver.execute_script(js)  
js = "addFld('DDSO_SA')"   
driver.execute_script(js) 
js = "addFld('CLASS_ID')"   
driver.execute_script(js)                     
                      
#######################################################################
#
# Submit data request
#
#######################################################################
mylink=driver.find_element(By.ID,"b_Submit")
print(mylink)
mylink.click()


