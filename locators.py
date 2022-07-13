class Locator:
    oUsername_field = 'username' #by.Name
    oPassword_field = 'password' #by.Name
    # The Login button on the main login page
    oLogin = "//*[@id='harriApp']/div[1]/ui-view/registration-login-container/div[2]/div/div[2]/div[7]/button"
    #The got_it pop_up
    oGot_it = "//*[@id='top']/div/nav/div/div/div[4]/a[4]"
    #The 
    oMap_icon_on_dashboard = "//li[contains(@class,'brand-navigation')]"
    oFirst_result_of_first_block ="(//div[contains(@class,'locations-list-wrapper')][2]//div[contains(@class,'brand-item')])[1]"
    oMy_team_header = "//*[@id='header-links-nav']//a[contains(.,'My Team')]"
    oForecasting = "//*[@id='header-links-nav']//li[contains(.,'Forecasting')]/div/button"
    oHistorical_data_menu_item = "//*[@id='header-links-nav']//a[contains(.,'Historical Data')]"
    oUpload_modal_title = "//*[@id='manage-template-modal']/div/div/div[1]/h4/span"
    oUpload_modal_popup = "//*[@id='manage-template-modal']/div/div"
    oUpload_historical_data_table_title = "//*[@id='upload_data']/a"
    # click somewhere on the page
    oHistorical_data_below_team_live = "//*[@id='harriApp']/div[1]/div/div[3]/forecasts-historical-data-component/div/div[1]/div[1]"
    oTop_right_search = "//div[contains(@class,'brands-dropdown')]"    
    oSearchbox = "//*[@id='harriApp']/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/h-brands-list/div/div/div[1]/div/input"
    oSearch_group_brandnames ="//h-brands-list//div[@class='locations-list-wrapper'][2]//div[contains(@class,'brand-name')]"
    oUpload_button_below_brands_list = "//forecasts-historical-data-component//button[contains(.,'Upload')]"
    oIgnore_button = "//div[contains(@class,'modal-footer')]//button[contains(.,'Ignore')]"
    oUpload_button_final = "//*[@id='manage-template-modal']//button[contains(.,'Upload')]"
    oBrowse_button = "//*[@id='manage-template-modal']//button[contains(.,'Browse')]"
    oCancel_button_on_upload_modal = "//*[@id='manage-template-modal']//button[contains(.,'Cancel')]"
    oStatus_table ="//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table"
    oNo_uploaded_files = "//div[contains(@class,'upload-historical-data-component')]//div[contains(.,'No uploaded files')]"
    oRows_in_status_table = "//*[@id='upload_data']/div/div/ng-transclude/upload-historical-data-component/div/div[2]/div[2]/table/tbody/tr"
    oBrand_name_results = "//div[contains(@class,'locations-list-wrapper')][2]//div[contains(@class,'brand-name')]"
    oSpinner_brands_list = "//div/h-brands-list/div/div[2]/i"
    #this is used to check  if the right search menu is open or not.
    oTop_title_in_right_location_bar = "//*[@id='top']/div[2]/h-brands-list/div/div/div[1]"
    oFirst_result_of_everyblock = "//h-brands-list//div[@class='locations-list-wrapper'][2]//div[@class='location-map-block']/following::div[1]"
    #an alternate way to calculate first search result of everyblock
    #oFirst_result_of_everyblock ="//h-brands-list//div[@class='locations-list-wrapper'][2]/div/div[2]"
