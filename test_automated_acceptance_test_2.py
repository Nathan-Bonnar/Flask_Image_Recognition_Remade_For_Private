#Automated Acceptance test 2
#Feature to be tested
#   AI interpretation of image that was given
#Senario
#   After a user has finished uploading an image, the artifical intelegence assess the image and user gets response 
#Given that the user has uploaded an image
#and that image is a valid image
#and the artificial intelege is able to proccess the image
#then the image will be assessed and proper output will be given

#testing steps 
#1. User uploads an image
#2. User hits submit
#3. AI processes image

#expected result
#Response is given with proper output for the image that was given. IE if user submitted an image with a 4, 4 is the output
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pytest

def test_Automated_Acceptance_Test_Two():
   
    driver = setup()

    file_input = driver.find_element(By.ID, "upload")

    image_path = os.path.abspath(r"test_images/4/Sign 4 (37).jpeg") 

    file_input.send_keys(image_path)

    time.sleep(2)

    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
    submit_button.click()

    wait = WebDriverWait(driver, 10)

    prediction_element = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h2.display-4.text-dark.font-weight-bold")
        )
    )

    prediction_text = prediction_element.text
    assert prediction_text == "4", f"Expected prediction '4', but got '{prediction_text}'"






def setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
   
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
    driver.get("http://127.0.0.1:9000/")
    return driver

def teardown(driver):
    driver.quit()