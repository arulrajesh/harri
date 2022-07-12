from locators import Locator,AnyEc
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException, TimeoutException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
import pandas as pd



class HarriSite:
    def __init__(self, wait, driver):
        self.wait = wait
        self.driver = driver
 

    def harri_login(self, uemail, upass):
        #This function enters the username and password and clicks the Login button on the login page.
        lf = self.driver.find_element_by_name(Locator.oUsername_field)
        pf = self.driver.find_element_by_name('password')
        logn = self.driver.find_element_by_xpath(Locator.oLogin)#"//*[@id='harriApp']/div[1]/ui-view/registration-login-container/div[2]/div/div[2]/div[7]/button")
        lf.send_keys(uemail)
        pf.send_keys(upass)
        logn.click()

    def got_it(self):
        try:
            element = self.driver.find_element_by_xpath(Locator.oGot_it)
            element.click()
        finally:
            pass
    
    def goto_dashboard(self):
        try:
            element = self.driver.find_element_by_xpath(Locator.oMap_icon_on_dashboard)
            element.click()
            element = self.driver.find_element_by_xpath(Locator.oFirst_result_of_first_block)
            element.click()
        except ElementClickInterceptedException:
            self.got_it()
            self.goto_dashboard()
        finally:
            pass
    
    def goto_myteam(self):
        try:
            element = self.driver.find_element_by_xpath(Locator.oMy_team_header)
            element.click()
        except ElementClickInterceptedException:
            self.got_it()
            self.goto_myteam()
        finally:
            pass

    # click forecasting
    def goto_forecasting(self):
        try:
            element = self.driver.find_element_by_xpath(Locator.oForecasting)
            element.click()
        except ElementClickInterceptedException:
            self.click_ignore()
            self.goto_forecasting()
        finally:
            pass

    def goto_historicaldata(self):
        try:  # click the Historical Data
            element = self.driver.find_element_by_xpath(Locator.oHistorical_data_menu_item)
            element.click()
        except ElementClickInterceptedException:
            self.click_ignore()
            self.goto_historicaldata()
        finally:
            pass
    
    def click_ignore(self):
        try:
            ignore_btn = self.driver.find_element_by_xpath(Locator.oIgnore_button)
            ignore_btn.click()
        except NoSuchElementException:
            pass
        finally:
            pass
  
    def upload_modal(self):
        try:  # click the "Upload Historical data" Title in modal popup window 
            element = self.driver.find_element_by_xpath(Locator.oUpload_modal_title)
            print(element.get_attribute("innerText"))  # "Upload Historical Data" Tfis is the title of the modal window.
            element.click()
        finally:
            pass
    
    # the Header of the table. "Upload historical Data". The upload button becomes visible only when the upload historical Data is clicked.
    def click_uploadhistoricaldata(self,attempts=0):
        attempts += 1
        try:  # check if the upload button below the location search is pressed is pressed otherwise click on the
            
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, Locator.oUpload_modal_popup)))
            element = self.driver.find_element_by_xpath(Locator.oUpload_historical_data_table_title)
            element.click()
            print("shipra")
        except ElementClickInterceptedException:
            print("arul")
            self.click_ignore()
            
            self.click_uploadhistoricaldata(attempts)
        except StaleElementReferenceException:
            self.click_uploadhistoricaldata(attempts)
        except TimeoutException:
            attempts = 100        
        finally:
            if attempts>2:print(f"attempts: {attempts}'\n'")
            return attempts

    def hsearch(self,clientID, clickit=True):
        #clickcit is set to false when this function is used to create the list of all brands except the first brand.
        try:  # click somewhere on the page, so that if the right search bar is open it will close.
            element_s = self.driver.find_element_by_xpath(Locator.oHistorical_data_below_team_live)
            element_s.click()
        finally:
            pass

        try:  # click on the top right search
            element_s = self.driver.find_element_by_xpath(Locator.oTop_right_search)
            element_s.click()
        finally:
            pass

        try:  # search for the site
            element =self.driver.find_element_by_xpath(Locator.oSearchbox)
            element.send_keys(clientID)
        finally:
            pass
        if clickit:
            try:  # Click on the first search result
                time.sleep(1)
                element = self.driver.find_element_by_xpath(Locator.oFirst_result_of_first_block)
                element.click()
            finally:
                pass

            try:  # click on the top right search to close the brands list
                element_s = self.driver.find_element_by_xpath(Locator.oTop_right_search)
                element_s.click()
            finally:
                pass
                # time.sleep(10)
        else:
            elems = self.driver.find_elements_by_xpath(Locator.oSearch_group_brandnames)
            companies = ""
            for x in elems:
                companies += x.get_attribute('innerText')+'|'
            return companies[:-1], len(elems)

    def click_upload(self):
        self.click_uploadhistoricaldata()
        try:
            element = self.wait.until(AnyEc(EC.element_to_be_clickable((By.XPATH, Locator.oUpload_button_below_brands_list)),EC.element_to_be_clickable((By.XPATH,Locator.oIgnore_button))))
            if element.get_attribute('innerText') == 'Ignore':
                element.click()
                self.click_uploadhistoricaldata()
                element = self.driver.find_element_by_xpath(Locator.oUpload_button_below_brands_list)
        except NoSuchElementException:
            self.click_uploadhistoricaldata()
            self.click_upload()
        finally:
            element.click()
    
    def hbrowse(self,fpath):
        try:  # click the "Browse" popup window
            element = self.driver.find_element_by_xpath(Locator.oBrowse_button)
            element.click()
        finally:
            pass
        time.sleep(2)
        subprocess.Popen(f'''fileupload/fileupload.exe "{fpath}"''')
        time.sleep(2)

    def final_upload(self,upload=True):
        try:  # click the Upload button in the popup window
            if upload:
                element = self.driver.find_element_by_xpath(Locator.oUpload_button_final)
            else:
                element = self.driver.find_element_by_xpath(Locator.oCancel_button_on_upload_modal)
            element.click()
        except ElementClickInterceptedException:
            self.click_ignore()
            element.click()
        finally:
            pass

    def status_write(self):
        attempts = self.click_uploadhistoricaldata(0)
        status = "NA"        
        try:  # Locate the presence of the table after upload and find the status in the last row
            # //*[@id="upload_data"]/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table
            result = self.wait.until(AnyEc(EC.visibility_of_element_located((By.XPATH, Locator.oStatus_table)), EC.visibility_of_element_located(
                (By.XPATH, Locator.oNo_uploaded_files))))
            if result.get_attribute('innerText') != 'No uploaded files':
                rows = self.driver.find_elements_by_xpath(Locator.oRows_in_status_table)
                status = self.driver.find_element(
                    By.XPATH, f"//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr[{len(rows)}]").get_attribute("innerText")
            else:
                status = 'No Uploaded Files'
        finally:
            print(status)
            return status
    
    def validate_search(self):
        df = pd.DataFrame(os.listdir('historicals'), columns=['historicals'])

        clist = []
        nlist = []
        search_terms = []
        
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
                        break
                    else:
                        search_term = 'ZZZZZZZZZZZZ'
                        companies = 'ZZZZZZZZZZZZZZZZ'

            else:
                companies = elemtn[0].get_attribute("innerText")
                search_term = clientid
            search_terms.append(search_term)
            clist.append(companies)
            nlist.append(len(elemtn))
        df['companies'] = clist
        df['#results'] = nlist
        df['clientid'] = search_terms
        df.to_csv('list.csv', index=False)

    # make sure you are on the dashboard page
    def get_list_of_sites(self):
        self.driver.get('http://harristaging.com/dashboard')
        element = self.driver.find_element_by_xpath(Locator.oMap_icon_on_dashboard) #map icon
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
        elems = self.river.find_elements(
            By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]")
        print(len(elems))
        sites = []
        for ele in elems:
            print(f"{ele.get_attribute('innerText')}")
            sites.extend(f"{ele.get_attribute('innerText')}".split('\n'))
        print(sites)

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