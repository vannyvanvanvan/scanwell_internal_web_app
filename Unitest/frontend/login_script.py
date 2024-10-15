from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    #================================================================
    
    driver.get("http://127.0.0.1:5000") 

    time.sleep(1)

    # Find the username field and type in the username
    username_input = driver.find_element(By.ID, "request_username")
    username_input.send_keys("admin@mail.com")

    # Find the password field and type in the password
    password_input = driver.find_element(By.ID, "request_password")
    password_input.send_keys("test1")

    # Find the "Remember me" checkbox and check it (optional)
    remember_me_checkbox = driver.find_element(By.ID, "remember_me")
    remember_me_checkbox.click()

    # Find the submit button and click it
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
    submit_button.click()

    print("Login admin successful!")
    
    #================================================================
    
    logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")  
    logout_button.click()

    print("Logout successful!")
    
    #================================================================
    
    # Find the username field and type in the username
    username_input = driver.find_element(By.ID, "request_username")
    username_input.send_keys("user@mail.com")

    # Find the password field and type in the password
    password_input = driver.find_element(By.ID, "request_password")
    password_input.send_keys("test2")

    # Find the "Remember me" checkbox and check it (optional)
    remember_me_checkbox = driver.find_element(By.ID, "remember_me")
    remember_me_checkbox.click()

    # Find the submit button and click it
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
    submit_button.click()

    print("Login user successful!")
    
    

except Exception as e:
    print(f"An error occurred: {e}")
          
          
finally:
    # Close the browser
    driver.quit()
