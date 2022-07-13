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
options=Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


###########################Setup Logging################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.debug(f'Harrisite Initialized')
#########################################################################

@click.group()
def cli():
    pass

@click.command()
@click.option("--user", type =click.Tuple([str,str]), help = "Username Password to login")
def createlist(user):
    """
    This Generates a list file that will need to be validated by opening in excel

    Arguments:
    g generate the list file
    """
    driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe',options=options)
    driver.maximize_window()
    driver.get('http://harristaging.com/user/login')
    wait = WebDriverWait(driver, 60)
    driver.implicitly_wait(1)
    FiHa = HarriSite(wait,driver)
    #u ,p = user
    u  = 'STAGING_Grant.Read@demipower.com'
    p = upass = 'House123!'
    FiHa.harri_login(u, p)
    FiHa.goto_dashboard()
    FiHa.goto_myteam()
    FiHa.goto_forecasting()
    FiHa.goto_historicaldata()
    FiHa.validate_search()



@click.command()
@click.option("--user", type =click.Tuple([str,str]), help = "Username Password to login")
def upload(user):
    """
    This program is supposed to be run after the list.csv file is generated.
    If there are no locations that have a clientID or search term as "ZZZZZZZZZ"
    Then you can run this, Otherwise it will fail
    """
    driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe',options=options)
    driver.maximize_window()
    driver.get('http://harristaging.com/user/login')
    wait = WebDriverWait(driver, 60)
    driver.implicitly_wait(1)
    FiHa = HarriSite(wait,driver)
    #u ,p = user
    u  = 'STAGING_Grant.Read@demipower.com'
    p = upass = 'House123!'
    FiHa.harri_login(u, p)
    FiHa.goto_dashboard()
    FiHa.goto_myteam()
    FiHa.goto_forecasting()
    FiHa.goto_historicaldata()
    df = pd.read_csv("list.csv")
    df2 = df.copy()
    statuss = []
    for row in df.itertuples():
        clientid, fname,upload = row.clientid, f"{os.getcwd()}\historicals\{row.historicals}",row.upload
        if upload:
            FiHa.click_uploadhistoricaldata()
            FiHa.hsearch(clientid)
            print(f'"{fname}"        {clientid}')
            FiHa.click_uploadhistoricaldata()
            FiHa.click_upload()
            FiHa.hbrowse(fname)
            FiHa.final_upload()
            statuss.append(FiHa.status_write())
        else:
            statuss.append('Did not attempt')
    df3 = pd.DataFrame(statuss,columns=['stat'])
    df2[['date','uploadedby','filename','status']]=df3['stat'].str.split('\t',expand=True)

    df2.to_csv('output.csv', index=False)



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