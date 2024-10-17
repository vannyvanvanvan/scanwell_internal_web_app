from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    #================================================================
    
    ''' Log in to the account first '''
    
    
    driver.get("http://127.0.0.1:5000") 

    time.sleep(1)

    # Find the username field and type in the username
    username_input = driver.find_element(By.ID, "request_username")
    username_input.send_keys("admin@mail.com")

    # Find the password field and type in the password
    password_input = driver.find_element(By.ID, "request_password")
    password_input.send_keys("test1")

    # Find the "Remember me" checkbox and check it
    remember_me_checkbox = driver.find_element(By.ID, "remember_me")
    remember_me_checkbox.click()

    # Find the submit button and click it
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
    submit_button.click()

    print("Login admin successful!")
    
    #================================================================
    
    ''' Click on add shipping schedule link '''
    
    add_shipping_link = driver.find_element(By.XPATH, "//a[@href='/admin/add_shipping_schedule']")
    add_shipping_link.click()
    
    carrier_input = driver.find_element(By.ID, "carrier")
    carrier_input.send_keys("test_carrier")
    
    service_input = driver.find_element(By.ID, "service")
    service_input.send_keys("test_only_will_delete")

    routing_input = driver.find_element(By.ID, "routing")
    routing_input.send_keys("test_only_will_delete")

    mv_input = driver.find_element(By.ID, "MV")
    mv_input.send_keys("test_only_will_delete")

    pol_input = driver.find_element(By.ID, "POL")
    pol_input.send_keys("test_only_will_delete")

    pod_input = driver.find_element(By.ID, "POD")
    pod_input.send_keys("test_only_will_delete")
    
    #===
    
    cy_open_input = driver.find_element(By.ID, "CY_Open")
    cy_open_input.send_keys("09302024")

    etd_input = driver.find_element(By.ID, "ETD")
    etd_input.send_keys("09302024")

    eta_input = driver.find_element(By.ID, "ETA")
    eta_input.send_keys("09302024")

    #===
    
    si_cut_off_input = driver.find_element(By.ID, "SI_Cut_Off")
    si_cut_off_input.send_keys("09302024")

    cy_cy_cls_input = driver.find_element(By.ID, "CY_CY_CLS")
    cy_cy_cls_input.send_keys("09302024")

    si_cut_off_time_input = driver.find_element(By.ID, "SI_Cut_Off_Time")
    si_cut_off_time_input.send_keys("0120A")
    
    si_cut_off_time_input = driver.find_element(By.ID, "CY_CY_CLS_Time")
    si_cut_off_time_input.send_keys("1020P")
    
    submit_shipping_schedule_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Submit']"))
    )


    driver.execute_script("arguments[0].scrollIntoView();", submit_shipping_schedule_button)
    time.sleep(1) 

    submit_shipping_schedule_button.click()
    
    #================================================================
    
    ''' Scoll Down and search for the latest shipping schedule that we just added, press the latest collapse id and press add booking order '''
    
        
    driver.execute_script("document.body.style.zoom='0.5';") 
    
    collapse_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'btn-outline-primary')]"))
    )
    
    # Select the last collapse button
    latest_collapse_button = collapse_buttons[-1] 
    
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    driver.execute_script("arguments[0].scrollIntoView(true);", latest_collapse_button)
    time.sleep(1) 

    latest_collapse_button.click()
    
    # Clicking the add button
    add_booking_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'btn-outline-primary') and contains(@href, '/admin/add_booking/')]"))
    )
    
    latest_booking_link = add_booking_links[-1]
    
    driver.execute_script("arguments[0].scrollIntoView(true);", latest_booking_link)
    time.sleep(1) 

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(latest_booking_link))
    
    driver.execute_script("arguments[0].click();", latest_booking_link)
    print("Clicked the latest booking link")
    
    #================================================================
    
    CS_input = driver.find_element(By.ID, "CS")
    CS_input.send_keys("test_only_will_delete")

    size_input = driver.find_element(By.ID, "size")
    size_input.send_keys("test_only_will_delete")

    Final_Destination_input = driver.find_element(By.ID, "Final_Destination")
    Final_Destination_input.send_keys("test_only_will_delete")
    
    Contract_or_Coloader_input = driver.find_element(By.ID, "Contract_or_Coloader")
    Contract_or_Coloader_input.send_keys("test_only_will_delete")
    
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Submit']"))
    )
    
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    time.sleep(1) 

    submit_button.click()
    
    #================================================================    
        
    ''' Same as the above scoll all the way down and press add confirm order button '''
    
    
    driver.execute_script("document.body.style.zoom='0.5';") 
    
    collapse_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'btn-outline-primary')]"))
    )
    
    # Select the last collapse button
    latest_collapse_button = collapse_buttons[-1] 
    
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    driver.execute_script("arguments[0].scrollIntoView(true);", latest_collapse_button)
    time.sleep(1) 

    latest_collapse_button.click()
    
    # Clicking the add button
    add_confirm_order = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'btn-outline-primary') and contains(@href, '/admin/add_confirm_order/')]"))
    )
    
    latest_confirm_order_link = add_confirm_order[-1]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(latest_confirm_order_link))
    
    driver.execute_script("arguments[0].click();", latest_confirm_order_link)
    print("Clicked the latest booking link")
    
    #================================================================
    
    shipper_input = driver.find_element(By.ID, "shipper")
    shipper_input.send_keys("test_shipper")
    
    consignee_input = driver.find_element(By.ID, "consignee")
    consignee_input.send_keys("test_only_will_delete")

    term_input = driver.find_element(By.ID, "term")
    term_input.send_keys("test_only_will_delete")
    
    salesman_input = driver.find_element(By.ID, "salesman")
    salesman_input.send_keys("test_only_will_delete")
    
    driver.find_element(By.ID, "SR").clear()

    SR_input = driver.find_element(By.ID, "SR")
    SR_input.send_keys("10")
    
    remark_input = driver.find_element(By.ID, "remark")
    remark_input.send_keys("test_only_will_delete")
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Submit']"))
    )
    
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    time.sleep(1) 

    submit_button.click()
    
except Exception as e:
    print(f"An error occurred: {e}")
          
          
finally:
    # Close the browser
    driver.quit()
