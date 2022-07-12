# %%
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException, TimeoutException
import time
import subprocess
# %%
def harri_login(hwait, uemail, upass):
    uname = hwait.until(EC.element_to_be_clickable((By.NAME, 'username')))
    passw = hwait.until(EC.element_to_be_clickable((By.NAME, 'password')))
    plogin = hwait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='harriApp']/div[1]/ui-view/registration-login-container/div[2]/div/div[2]/div[7]/button")))
    print(plogin.get_attribute('innerText'))
    uname.send_keys(uemail)
    passw.send_keys(upass)
    plogin.click()

# %%
class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """

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


# %%
# click "Got it" on the Create your own dashboard view page.
def got_it(wait):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='top']/div/nav/div/div/div[4]/a[4]")))
        element.click()
    finally:
        pass


# %%
# Get into the dashboard by clicking on the first parent in the list
def goto_dashboard(wait):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class,'brand-navigation')]")))
        element.click()
        searchbar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'locations-list-wrapper')][2]//div[contains(@class,'brand-item')][1]")))
        searchbar.click()
    except ElementClickInterceptedException:
        got_it()
        goto_dashboard()
    finally:
        pass


# %%
# once at dashboard page. Go to My Team
def goto_myteam(wait):
    try:
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='header-links-nav']//a[contains(.,'My Team')]")))
        element.click()
    except ElementClickInterceptedException:
        got_it()
        goto_myteam()
    finally:
        pass


# %%
# click forecasting
def goto_forecasting(wait):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']//li[contains(.,'Forecasting')]/div/button")))

        while (element.get_attribute("innerText")) != "Forecasting":

            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header-links-nav']//li[contains(.,'Forecasting')]/div/button")))

        element.click()
        print(element.get_attribute("innerText"))  # should be Forecasting
    except ElementClickInterceptedException:
        click_ignore()
        goto_forecasting()
    finally:
        pass


# %%
def goto_historicaldata(wait):
    try:  # click the Historical Data
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='header-links-nav']//a[contains(.,'Historical Data')]")))
        element.click()
    finally:
        pass


# %%
def upload_modal(wait):
    try:  # click the "Upload Historical data" popup window
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='manage-template-modal']/div/div/div[1]/h4/span")))
        print(element.get_attribute("innerText"))  # should be modal window
        element.click()
    finally:
        pass


# %%
def click_uploadhistoricaldata(wait,attempts=0):
    attempts += 1
    try:  # check if the upload button is pressed otherwise click on the
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//*[@id='manage-template-modal']/div/div")))
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='upload_data']/a")))
        element.click()
    except ElementClickInterceptedException:
        click_ignore()
        click_uploadhistoricaldata(attempts)
    except StaleElementReferenceException:
        click_uploadhistoricaldata(attempts)
    except TimeoutException:
        attempts = 100        
    finally:
        if attempts>2:print(f"attempts: {attempts}'\n'")
        return attempts


# %%
def hsearch(wait,driver,clientID, clickit=True):
    try:  # click somewhere on the page
        element_s = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[1]")))
        element_s.click()
    finally:
        pass

    try:  # click on the top right search
        element_s = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/a/div/div[2]/div[1]")))
        element_s.click()
    finally:
        pass
    try:  # search for the site
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[1]/div/input")))
        element.send_keys(clientID)
    finally:
        pass
    if clickit:
        try:  # Click on the first search result
            time.sleep(1)
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]/div/div[2]")))
            element.click()
        finally:
            pass

        try:  # click on the top right search
            element_s = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/a/div/div[2]/div[1]")))
            element_s.click()
        finally:
            pass
    else:
        elems = driver.find_elements(
            By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]")
        companies = ""
        for x in elems:
            companies += x.get_attribute('innerText')+'|'
        return companies[:-1], len(elems)

# %%
def click_upload(wait):
    click_uploadhistoricaldata()
    try:
        element = wait.until(AnyEc(EC.element_to_be_clickable((By.XPATH, "//forecasts-historical-data-component//button[contains(.,'Upload')]")),EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'modal-footer')]//button[contains(.,'Ignore')]"))))
        if element.get_attribute('innerText') == 'Ignore':
            element.click()
            click_uploadhistoricaldata()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//forecasts-historical-data-component//button[contains(.,'Upload')]")))
    except NoSuchElementException:
        click_uploadhistoricaldata()
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[2]/button[2]")))
    finally:
        element.click()


# %%
def hbrowse(fpath,wait):
    try:  # click the "Browse" popup window
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='manage-template-modal']/div/div/div[2]/div/div[3]/div[2]/button")))
        element.click()
    finally:
        pass
    time.sleep(1)
    subprocess.Popen(f'''fileupload/fileupload.exe "{fpath}"''')
    time.sleep(2)


# %%
def final_upload(wait,upload=True):
    try:  # click the Upload button in the popup window
        if upload:
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='manage-template-modal']//button[contains(.,'Upload')]")))  # upload
        else:
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='manage-template-modal']//button[contains(.,'Cancel')]")))  # cancel
        element.click()
    except ElementClickInterceptedException:
        click_ignore()
        element.click()
    finally:
        pass


# %%
def click_ignore(driver):
    try:
        ignore_btn = driver.find_element(By.XPATH, "//div[contains(@class,'modal-footer')]//button[contains(.,'Ignore')]")
        ignore_btn.click()
    except NoSuchElementException:
        pass
    finally:
        pass


# %%
def status_write(wait,driver):
    attempts = click_uploadhistoricaldata(0)
    status = "Took too Long. Attempts: "+ str(attempts)
    
    try:  # Locate the presence of the table after upload and find the status in the last row
        result = wait.until(AnyEc(EC.visibility_of_element_located((By.XPATH, "//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table")), EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'upload-historical-data-component')]//div[contains(.,'No uploaded files')]"))))
        if result.get_attribute('innerText') != 'No uploaded files':
            rows = driver.find_elements_by_xpath(
                "//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr")
            status = driver.find_element(
                By.XPATH, f"//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr[{len(rows)}]").get_attribute("innerText")
        else:
            status = 'No Uploaded Files'
    finally:
        print(status)
        return status


# %%
def validate_search(driver):
    df = pd.DataFrame(os.listdir(
        'C:\\Users\\arulr\\harri\\historicals'), columns=['historicals'])
    clist = []
    nlist = []
    search_terms = []
    for row in df.itertuples():
        clientid = row.historicals[:-4]
        hsearch(clientid, False)
        elemtn = driver.find_elements(
            By.XPATH, "//div[contains(@class,'locations-list-wrapper')][2]//div[contains(@class,'brand-name')]")
        if len(elemtn) != 1:
            # try to split the file name and do a search for each
            sterms = clientid.split(' ')
            for x in sterms:
                companies, tin = hsearch(x.strip(), False)
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



# %%
# make sure you are on the dashboard page
def get_list_of_sites(wait,driver):
    driver.get('http://harristaging.com/dashboard')
    element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='top']/div/nav/ul[3]/li[6]/a/i")))
    element.click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='top']/div[2]/h-brands-list/div/div/div[1]")))
    element_blk = driver.find_elements(
        By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[@class='location-map-block']/following::div[1]")
    for ele in element_blk:
        driver.execute_script("""
        var ele = arguments[0];
        ele.parentNode.removeChild(ele);
        """, ele)
#    element_blk = driver.find_elements(By.XPATH,"//h-brands-list//div[@class='locations-list-wrapper'][2]//div[@class='location-map-block']")
#    for ele in element_blk:
#        driver.execute_script("""
#        var ele = arguments[0];
#        ele.parentNode.removeChild(ele);
#        """, ele)

    elems = driver.find_elements(
        By.XPATH, "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]")
    print(len(elems))
    sites = []
    for ele in elems:
        print(f"{ele.get_attribute('innerText')}")
        sites.extend(f"{ele.get_attribute('innerText')}".split('\n'))
    print(sites)

def main():
    print('this is my function')

if __name__ == "__main__":
    main()
