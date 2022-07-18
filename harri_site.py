import click
from locators import Locator
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import subprocess
import pandas as pd
import time
import logging

###########################Setup Logging################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler2 =logging.FileHandler('logs\site.log')
file_handler2.setFormatter(formatter)
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler) 
logger.addHandler(file_handler)
logger.addHandler(file_handler2)
#########################################################################

class HarriSite:
    def __init__(self, wait, driver):
        self.wait = wait
        self.driver = driver 

    def harri_login(self, uemail, upass):
        #This function enters the username and password and clicks the Login button on the login page.
        try:
            lf = self.wait.until(EC.element_to_be_clickable((By.NAME,Locator.oUsername_field)))
            pf = self.wait.until(EC.element_to_be_clickable((By.NAME,Locator.oPassword_field)))
            logn = self.driver.find_element("xpath",Locator.oLogin)
            lf.send_keys(uemail)
            pf.send_keys(upass)
            logger.debug(f'Login Attempted')
            logn.click()
        except:
            logger.exception("Unhandled exception while trying to login")
            raise
        finally:
            logger.info("Successfully logged in")

    def got_it(self):
        try:
            element = self.driver.find_element('xpath',Locator.oGot_it)
            element.click()
        except Exception as e:
            logger.exception("Failed to click got it, did it show 'next' instead of got it")
        finally:
            pass

    def goto_dashboard(self):
        logger.debug("Attempting to navigate to dashboard.")
        while True:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oMap_icon_on_dashboard)))
                element.click()
                element = self.driver.find_element('xpath',Locator.oFirst_result_of_first_block)
                element.click()
                logger.info("Success: Navigated to dashboard")
                break
            except ElementClickInterceptedException:
                logger.info("Clicked 'Got it' on the way to the Dashboard")
                pass
            except NoSuchElementException:
                logger.info("waiting for dashboard page to load after Login......")
            except:
                logger.exception("Unhandled exception while going to dashboard")
                raise
            finally:
                pass

    def goto_myteam(self):
        logger.debug("Attempting to click on 'My Team'")
        while True:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oMy_team_header)))
                element.click()
                logger.info("Success: navigated to MyTeam")
                break
            except ElementClickInterceptedException:
                logger.info("Clicked 'got it' on the way to clicking my team")
                pass
            except:
                logger.exception("Unhandled exception while going to MyTeam")
                raise
            finally:
                pass

    # click forecasting
    def goto_forecasting(self):
        logger.debug("Attempting to click Forecasting")
        while True:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oForecasting)))
                element.click()
                logger.info("Success: Navigated to Forecasting")
                break
            except ElementClickInterceptedException:
                logger.info("clicked 'Ignore' while going to Forecasting")
                pass
            except:
                logger.exception("Unhandled exception Forecasting")
                raise
            finally:
                pass

    def goto_historicaldata(self):
        while True:
            try:  # click the Historical Data
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oHistorical_data_menu_item)))
                element.click()
                logger.info("Success: Navigated to HistoricalData")
                break
            except ElementClickInterceptedException:
                logger.info("Trying to click Ignore while going to Historical data")
                pass
            except:
                logger.info("Unhandled exception Historical Data")
                raise
            finally:
                pass

    def click_ignore(self):
        try:
            ignore_btn = self.driver.find_element('xpath',Locator.oIgnore_button)
            ignore_btn.click()
        except NoSuchElementException:
            logger.info("Ignore Button not found, when trying to click it.")
        finally:
            pass

    def upload_modal(self):
        while True:
            try:  # click the "Upload Historical data" Title in modal popup window 
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oUpload_modal_title)))
                print(element.get_attribute("innerText"))  # "Upload Historical Data" Tfis is the title of the modal window.
                element.click()
                break
            finally:
                pass

    # the Header of the table. "Upload historical Data". The upload button becomes visible only when the upload historical Data is clicked.
    def click_uploadhistoricaldata(self,attempts=0):
        logger.debug("CLick upload Historicaldata table header")
        while True:        
            try:  # check if the upload button below the location search is pressed is pressed otherwise click on the
                #self.wait.until(EC.invisibility_of_element_located((By.XPATH, Locator.oUpload_modal_popup)))
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oUpload_historical_data_table_title)))
                element.click()
                break
            except ElementClickInterceptedException as e:
                logger.info("Trying to click 'Ignore' while going to Historical Data table header")
                pass
            except StaleElementReferenceException:
                logger.info("Stale upload historical Data exception")
            except TimeoutException:
                logger.info("Timed out while trying to click Upload Historical Data table header")
                raise
            finally:
                pass

    def hsearch(self,clientID, clickit=True):
        #clickcit is set to false when this function is used to create the list.csv file.
        logger.info(f'Processing "{clientID}" file')
        try:  # click somewhere on the page
            element_s = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,Locator.oHistorical_data_below_team_live)))
            element_s.click()
        finally:
            pass

        try:  # click on the top right search
            element_s = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,Locator.oTop_right_search)))
            element_s.click()
        finally:
            pass
        try:  # search for the site
            element = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,Locator.oSearchbox)))
            element.send_keys(clientID)
        finally:
            pass
        if clickit:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH,Locator.oFirst_result_of_first_block)))
            element.click()
            self.wait.until(EC.invisibility_of_element_located((By.XPATH,Locator.oSpinner_brands_list)))
            if EC.visibility_of_all_elements_located((By.XPATH,Locator.oSearchbox))(self.driver):  # click on the top right search
                element_s = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH,Locator.oTop_right_search)))
                element_s.click()
            self.click_uploadhistoricaldata()
        else:
            elems =self.driver.find_elements(
                By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]")
            companies = ""
            for x in elems:
                companies += x.get_attribute('innerText')+'|'
            logger.info(f"found ({len(elems)}) for {clientID} :['{companies[:-1]}']")
            return companies[:-1], len(elems)

    def click_upload(self):
        logger.info(f'Attempting to click the Upload buttton below brands list' )
        self.driver.implicitly_wait(1)
        while True:
            try:
                element = self.driver.find_element('xpath',Locator.oUpload_button_below_brands_list)
                element.click()
                logger.info('Success: started upload interface')
                break
            except NoSuchElementException:
                logger.info("Upload button not found, attempting to click the upload historical data table header.")
                self.click_uploadhistoricaldata()
            except StaleElementReferenceException:
                logger.info("Stale element exception while clicking upload button below brands lits")    
                self.click_uploadhistoricaldata()
            except ElementClickInterceptedException:
                pass
            finally:
                pass

    def hbrowse(self,fpath):
        logger.info(f'Attempting to browse to {fpath}')
        while True:
            try:  # click the "Browse" popup window
                element = self.driver.find_element('xpath',Locator.oBrowse_button)
                element.click()
                time.sleep(2)
                subprocess.Popen(f'''fileupload/fileupload.exe "{fpath}"''')
                time.sleep(1)
                break
            except ElementClickInterceptedException:
                pass

    def final_upload(self,upload=True):
        while True:
            try:  # click the Upload button in the popup window
                if upload:
                    element = self.driver.find_element('xpath',Locator.oUpload_button_final)
                    msx = f'File selected, clicking upload'
                else:
                    element = self.driver.find_element('xpath',Locator.oCancel_button_on_upload_modal)
                    msx = f'File selected, however clicking "Cancel" as we are in test mode.'
                element.click()
                logger.info(msx)
                self.wait.until(EC.invisibility_of_element(element))
                break
            except ElementClickInterceptedException:
                pass


    def status_write(self):
        status = "NA"
        ctr=1
        self.driver.implicitly_wait(1)
        while True:
            logger.info(f'attempt:{ctr}')        
            try:  # Locate the presence of the table after upload and find the status in the last row
                # //*[@id="upload_data"]/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table
                logger.debug('waiting for upload table to show up')
                ctr+=1
                result = WebDriverWait(self.driver,3).until(AnyEc(EC.visibility_of_element_located((By.XPATH, Locator.oStatus_table)), EC.visibility_of_element_located(
                (By.XPATH, Locator.oNo_uploaded_files)),EC.element_to_be_clickable((By.XPATH,Locator.oLoadingtable))))
                innerT = result.get_attribute('innerText') 
                if 'Loading' in innerT:
                    if ctr>10:
                        print(ctr)
                        status = 'Took too long'
                        return status
                elif innerT == 'No uploaded files':
                    logger.debug('could not find the table')
                    status = 'No Uploaded Files'
                    return status 
                else:
                    logger.debug('Found the table')
                    rows = self.driver.find_elements('xpath',Locator.oRows_in_status_table)
                    status = self.driver.find_element(
                        By.XPATH, f"//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr[{len(rows)}]").get_attribute("innerText")
                    return status                    
            except:
                logger.exception('There was an exception')
                self.click_uploadhistoricaldata()
                pass
            finally:
                logger.info(status)
                print(status)
        
    def validate_search(self):
        '''Have to definitely write a help file for this'''
        df = pd.DataFrame(os.listdir('historicals'), columns=['historicals'])
        clist = []
        nlist = []
        search_terms = []
        uploadss= []
        self.driver.implicitly_wait(0) 
        for row in df.itertuples():
            clientid = row.historicals[:-4]
            self.hsearch(clientid, False)
            elemtn = self.driver.find_elements(
                By.XPATH, Locator.oBrand_name_results)
            if len(elemtn) != 1:
                # try to split the file name and do a search for each
                sterms = clientid.split(' ')
                for x in sterms:
                    companies, tin = self.hsearch(x.strip(), False)
                    if tin == 1:
                        search_term = x
                        uploads = 1
                        break
                    else:
                        search_term = 'ZZZZZZZZZZZZ'
                        companies = 'ZZZZZZZZZZZZ'
                        uploads = 0
            else:
                companies = elemtn[0].get_attribute("innerText")
                search_term = clientid
                uploads =1
            search_terms.append(search_term)
            clist.append(companies)
            nlist.append(len(elemtn))
            uploadss.append(uploads)
        df['companies'] = clist
        df['#results'] = nlist
        df['clientid'] = search_terms
        df['upload'] = uploadss
        df.sort_values(by=['upload','#results'], inplace=True)
        df.to_csv('list.csv', index=False)
        logger.info('Successfully exported "list.csv" file. Please check file for any ZZZZZZs. Correct and set upload to 1.')

    # make sure you are on the dashboard page
    def get_list_of_sites(self):
        logger.info('Running get list of sites')
        self.driver.get('http://harristaging.com/dashboard')
        element = self.Webdriverwait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH,Locator.oMap_icon_on_dashboard))) #map icon
        element.click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,Locator.oTop_title_in_right_location_bar)))
        element_blk = self.driver.find_elements(
            By.XPATH,Locator.oFirst_result_of_everyblock)
        for ele in element_blk:
            self.driver.execute_script("""
            var ele = arguments[0];
            ele.parentNode.removeChild(ele);
            """, ele)
        elems = self.driver.find_elements(
            By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]")
        logger.info(f'{len(elems)} sites found in brand list, excluding first in each group')
        sites = []
        for ele in elems:
            logger.info(f"{ele.get_attribute('innerText')}")
            sites.extend(f"{ele.get_attribute('innerText')}".split('\n'))
        return sites

class AnyEc:

    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                res = fn(driver)
                if res:
                    return res
                    # Or return res if you need the element found
            except:
                    pass
