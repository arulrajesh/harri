from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
import pandas as pd
import click
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException, TimeoutException
from harri_site import HarriSite
import logging
from selenium.webdriver.chrome.options import Options
import threading
import time
from locators import Locator
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options=Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
import cred


###################################################
U = cred.U
P = cred.P
URL = cred.LoginURL
###################################################


###########################Setup Logging################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)-11s - %(levelname)-6s -%(funcName)-20s - %(message)s')
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
#########################################################################

def pop_up_killer(driver):
    while True:
        time.sleep(1)
        driver.implicitly_wait(0)
        for i in Locator.pops:
            try:
                s= driver.find_element('xpath',i)
                s.click()
                logger.info(f'Clicked {i}')
            except:
                pass
        driver.implicitly_wait(1)

@click.group()
def cli():
    pass

@click.command()
@click.option("-n","--nogui", default = False, help = "Set to True to hide the browser.")
def createlist(nogui):
    """
    \b
    This generates a 'list.csv' file based on the files present in the historicals folder.
    The program logs into the harri URL provided, goes to the dashboard page and searches
    for each filename, trying to search the exact location. If doesn't find a unique match with 
    the file name, the program breaks up the filename by space and searches each portion till 
    it finds a unique match. 
        e.g., If there is a file named "bury-road.csv" in the historicals folder, 
        it will first search for "Ipswich bury-road". If there are no matches it 
        will next search for "Ipswich", then for "bury-road" until it finds a 
        unique match in the locations list.
    \b
    The 'list.csv' file will have five folowing columns:
    historicals: The list of file names in the historicals folder.
    companies  : The list of matches if found in the harri URL.
    #results   : 1 if the file name returns a match as is, 0 if no 
                match is found with just file name.
    clientid   : The search term that resulted in a unique match.
    upload     : 1 if the csv file is to be uploaded. 0 if you want
                 to skip uploading the csv file.
    \b
    You will have to validate the list.csv before you run the next step.
        1. Check if there are any "clientid" that are ZZZZZZZZZZZZ. These are the files that did not
            return any matches in the location.
        2. You will have to manually update the 'clientid' to a phrase that uniquely 
            identifies the location     e.g., in the above "Ipswich bury-road" example.
            This would be "bury road", notice how the hyphen was replaced with a space.
        3. Change the 'upload' column to 1.
    \b
    Tips:
        For this to generate the list.csv file. Place all the files that need to be uploaded to harri
    in the "Historicals" folder. Make sure the Name of each file is similar to the one in brand list.
    """
    try:
        if nogui: 
            options.headless = True
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options) #driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe',options=options)
        driver.maximize_window()
        driver.get(URL)
        wait = WebDriverWait(driver, 60)
        driver.implicitly_wait(1)
        x = threading.Thread(target=pop_up_killer,args=(driver,),daemon=True)
        x.start()
        FiHa = HarriSite(wait,driver)
        #u ,p = user
        u  = U
        p = P
        FiHa.harri_login(u, p)
        FiHa.goto_dashboard()
        FiHa.goto_myteam()
        FiHa.goto_forecasting()
        FiHa.goto_historicaldata()
        FiHa.validate_search()
        driver.close()
    except:
        logger.exception("There was an unexpected error please contact the developer.")
        driver.close()
        raise


@click.command()
@click.option("-n","--nogui", default = False, help = "Set to True to hide the browser.")
def upload(nogui):
    """
    This program is supposed to be run after the list.csv file is generated.
    If there are no locations that have a clientID or search term as "ZZZZZZZZZ"
    Then you can run this, Otherwise it will fail. 


    This program will search for the "clientID" field in the list.csv file in the brands list.
    then it will upload the corresponding csv file as named in the "historicals" feild.
    """
    try:
        df = pd.read_csv("list.csv")
        df2 = df.copy()
        statuss = []
        if nogui:
            options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options) #webdriver.Chrome(executable_path='chromedriver\chromedriver.exe',options=options)
        if 1 in df['upload'].values:
            driver.maximize_window()
            driver.get(URL)
            wait = WebDriverWait(driver, 60)
            driver.implicitly_wait(1)
            x = threading.Thread(target=pop_up_killer,args=(driver,),daemon=True)
            x.start()
            FiHa = HarriSite(wait,driver)
            #u ,p = user
            u  = U
            p = P
            FiHa.harri_login(u, p)
            FiHa.goto_dashboard()
            FiHa.goto_myteam()
            FiHa.goto_forecasting()
            FiHa.goto_historicaldata()
        for row in df.itertuples():
            clientid, fname,upload = row.clientid, f"{os.getcwd()}\historicals\{row.historicals}",row.upload
            if upload:
                FiHa.click_uploadhistoricaldata()
                FiHa.hsearch(clientid)
                FiHa.click_uploadhistoricaldata()
                FiHa.click_upload()
                FiHa.hbrowse(fname)
                FiHa.final_upload()
                fial_sta =FiHa.status_write()
                statuss.append(fial_sta)
                logger.info(fial_sta)
            else:
                statuss.append(f'{datetime.now().strftime("%b %d, %Y %H:%M:%S")}\t\t\tDid not attempt')
            
        df3 = pd.DataFrame(statuss,columns=['stat'])
        df2[['date','uploadedby','filename','status']]=df3['stat'].str.split('\t',expand=True)
        while True:
            try:
                df2.to_csv('output.csv', index=False)
                logger.info(f'"output.csv" saved. PLease check status column')
                break
            except PermissionError:
                input("Could not save output.csv file! Please close the file & Press Enter to retry:\n>>")
        driver.close()
    except:
        logger.exception("There was unexpected error. Please contact the developer.")
        driver.close()
        raise


@click.command()
def logtest():
    '''This is a test to generate a logfile'''
    logger.debug("Testing in progress")
    print("a")
    pass

cli.add_command(upload)
cli.add_command(createlist)
cli.add_command(logtest)

if __name__ == "__main__":
    cli()
