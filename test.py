# import webdriver 
from selenium import webdriver 
  
# create webdriver object 
driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe')
    
# set implicit wait time
driver.implicitly_wait(10) # seconds
  
# get geeksforgeeks.org 
driver.get("https://www.geeksforgeeks.org/") 
    
# get element after 10 seconds
element = driver.find_element_by_link_text("Courses")
  
# click element
element.click()