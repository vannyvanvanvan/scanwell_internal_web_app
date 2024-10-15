from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Make sure the path is correct if not in PATH)
driver = webdriver.Chrome()  # You can use webdriver.Firefox() for Firefox

try:
    # Navigate to the login page
    driver.get("http://127.0.0.1:5000")  # Adjust this URL based on your setup

    # Wait for the page to load
    time.sleep(2)  # You can use WebDriverWait for better practice

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

    # Wait for the next page to load (adjust based on your application's behavior)
    time.sleep(2)

    print("Login successful!")

except Exception as e:
    print(f"An error occurred: {e}")
          
          
finally:
    # Close the browser
    driver.quit()
