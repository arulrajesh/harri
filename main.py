# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import os,pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe')
driver.maximize_window()
driver.get('http://harristaging.com/user/login')
wait = WebDriverWait(driver,60)

# %%
def harri_login(hwait,uname,upass):
    uname = hwait.until(EC.element_to_be_clickable((By.NAME,'username')))
    passw = hwait.until(EC.element_to_be_clickable((By.NAME,'password')))
    login = hwait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='harriApp']/div[1]/ui-view/registration-login-container/div[2]/div/div[2]/div[7]/button")))
    uname.send_keys(uemail)
    passw.send_keys(upass)
    login.click()

# %%
# click "Got it" on the Create your own dashboard view page.
def got_it():
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='top']/div/nav/div/div/div[4]/a[4]")))
        element.click()
    finally:
        pass

# %%
# Get into the dashboard by clicking on the first parent in the list
def goto_dashboard():
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div/div/div/div/div[1]/div/div[1]")))
        element.click()
    finally:
        pass

# %%
# once at dashboard page. Go to My Team
def goto_myteam():
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']/li[3]/a")))
        if (element.get_attribute("innerText")) == "MY TEAM":
            element.click()
        print(element.get_attribute("innerText"))
    finally:
        pass


# %%
#click forecasting
def goto_forecasting():
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']/ul/li[5]/div/button")))

        while (element.get_attribute("innerText")) != "Forecasting":
            
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']/ul/li[5]/div/button")))

        element.click()
        print(element.get_attribute("innerText")) # should be Forecasting
    finally:
        pass

# %%
def goto_historicaldata():
    try: #click the Historical Data 
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']/ul/li[5]/div/ul/li[2]/a")))
        print(element.get_attribute("innerText")) # should be "Historical data"
        element.click()
    finally:
        pass
        

# %%
def upload_modal():
    try: #click the "Upload Historical data" popup window
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='manage-template-modal']/div/div/div[1]/h4/span")))
        print(element.get_attribute("innerText")) # should be modal window
        element.click()
    finally:
        pass

# %%
def click_uploadhistoricaldata():
    try: #check if the upload button is pressed otherwise click on the 
        time.sleep(1)
        
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='upload_data']/a")))
        wait.until(EC.invisibility_of_element_located((By.XPATH,"//*[@id='manage-template-modal']/div/div")))
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='upload_data']/a")))
        element.click()
    finally:
        pass

# %%
def hsearch(clientID):
    try:#click somewhere on the page
        element_s = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[1]")))
        element_s.click()
    finally:
        pass    

    try: #click on the top right search
        element_s = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/a/div/div[2]/div[1]")))
        element_s.click()
    finally:
        pass
    try: # search for the site
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[1]/div/input")))
        element.send_keys(clientID)
    finally:
        pass
    try: #Click on the first search result
        time.sleep(1)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[6]/div/div[2]")))
        element.click() 
    finally:
        pass
    try: #click on the top right search
        element_s = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/a/div/div[2]/div[1]")))
        element_s.click()
    finally:
        pass
        #time.sleep(10)
    

# %%
def click_upload():
    click_uploadhistoricaldata()
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[2]/button[2]")))
    except NoSuchElementException:
        click_uploadhistoricaldata()
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[2]/button[2]")))
    finally:
        element.click()


# %%
def hbrowse(fpath):
    try: #click the "Browse" popup window
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='manage-template-modal']/div/div/div[2]/div/div[3]/div[2]/button")))  
        element.click()
    finally:
        pass
    time.sleep(1)
    subprocess.Popen(f'''fileupload/fileupload.exe "{fpath}"''')
    time.sleep(2)

# %%
def final_upload():
    try: #click the Upload button in the popup window
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='manage-template-modal']/div/div/div[3]/div/button[2]/span[1]")))
            #EC.element_to_be_clickable((By.XPATH, "//*[@id='manage-template-modal']/div/div/div[3]/div/button[1]")))
        print(element.get_attribute("innerText")) 
        element.click()
    finally:
        pass

# %%
def status_write():
    click_uploadhistoricaldata()
    try: #Locate the presence of the table after upload and find the status in the last row
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table")))#//*[@id="upload_data"]/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table
        rows =  driver.find_elements_by_xpath("//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr")
        status = driver.find_element(By.XPATH,f"//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr[{len(rows)}]/td[4]").get_attribute("innerText")
    finally:
        return status

# %%

uemail = 'STAGING_Jmharri@harri.com'
upass = 'House123!'
harri_login(wait,uemail,upass)
got_it()
goto_dashboard()
got_it()
goto_myteam()
goto_forecasting()
goto_historicaldata()



# %%
df= pd.read_csv("list.csv")
df2 = df.copy()
statuss=[]
for row in df.itertuples():
    clientid, fname = row.clientId, f"{os.getcwd()}\historicals\{row.historicals}"
    click_uploadhistoricaldata()
    hsearch(clientid)
    print(f'"{fname}"        {clientid}')
    click_upload()
    hbrowse(fname)
    final_upload()
    statuss.append(status_write())
df2['status'] = statuss
df2.to_csv('output.csv')

# %% [markdown]
# ##Rename the files to be uploaded for testing

# %%
def rename_files():
    df = pd.read_csv('list.csv')
    fpath1 = os.getcwd()
    for rws in df.itertuples():
        os.rename(f'''{fpath1}\historicals\{rws.old_name}''',f'''{fpath1}\historicals\{rws.historicals}''')




# %% [markdown]
# #top right search for site.
# //*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/a/div/div[2]/div[1] 
# 
# #search input field
# //*[@id='harriapp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[1]/div/input
# 
# #first element of search
# //*[@id='harriapp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[6]/div/div[2]
# 
# #upload historical data
# //*[@id="upload_data"]/a
# 
# #view historical data
# //*[@id="view_data"]/a
# 
# 
# #cancel button in upload
# //*[@id="manage-template-modal"]/div/div/div[3]/div/button[1]


