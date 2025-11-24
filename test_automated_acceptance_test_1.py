#Automated Acceptance test 1
#Feature to be tested
#   uploading an image
#Senario
#   A user would like to upload an image to have it be assed by the application
#Given that the user has an image they would like to upload
#And that the webservice is currently running
#When I connect to the website 
#and I select upload image
#and The image successfully gets recived by the webserive 
#then the image will have been uploaded and is ready for assessment

#Test steps
# 1. A user will connect to the webserive 
# 2. The user will select upload image
# 3. The user will select an image they would like to upload 

#Expected Results
# The website will recive the image, and display it back to the user, showing them what they have uploaded to be assessed
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import pytest


def test_Automated_Acceptance_Test_One():
    driver = setup()

    title = driver.title
    assert title == "Hand Sign Digit Recognition"

    file_input = driver.find_element(By.ID, "upload")

    image_path = os.path.abspath(r"test_images/4/Sign 4 (37).jpeg") 

    file_input.send_keys(image_path)

    time.sleep(2)

    image_preview = driver.find_element(By.ID, "imageResult")
    
    print("Preview src:", image_preview.get_attribute("src"))

    teardown(driver)




def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:9000/")
    return driver

def teardown(driver):
    driver.quit()