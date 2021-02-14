"""
Author: Muhammet Rezan Icgil
"""

import re
from time import sleep
import imutils as imutils
import cv2
import pytesseract as tess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Please don't forget to type your own parameters  at which are given with IMPORTANT message as below,  to use the program correctly.

# _____________________________________________________________________________IMPORTANT

username = "Enter your username here: "
password = "Enter your password here:"
url = "Paste the login page url here: "
FIREFOXDRIVER_PATH = "Past your geckodriver.exe path here: "

# ____________________________________________________________________________ IMPORTANT

usernameItemId = "Type the username item id in page source here"
passwordItemId = "Type the password item id in page source here"
secureCodItemId = "Type the secure code item id in page source here"
loginButtonItemId = "Type the login button item id in page source here"

# ____________________________________________________________________________ IMPORTANT


driver = webdriver.Firefox(executable_path=FIREFOXDRIVER_PATH)
driver.get(url)

list = []


def imageProcessing():
    sleep(2)
    driver.refresh()
    driver.find_element_by_id("imgCaptchaImg").screenshot("saved.png")
    tess.pytesseract.tesseract_cmd = r'Type your own tesseract.exe file path here'
    img = cv2.imread('saved.png')
    img = imutils.resize(img, width=150, height=130)
    gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gri = cv2.bilateralFilter(gri, 11, 17, 17)
    adaptive_threshold = cv2.adaptiveThreshold(gri, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 69)
    text = tess.image_to_string(adaptive_threshold)
    return text


def enterKeys():
    driver.find_element_by_id(usernameItemId).send_keys(username)
    driver.find_element_by_id(passwordItemId).send_keys(password)
    driver.find_element_by_id(secureCodItemId).send_keys(sum)
    driver.find_element_by_id(loginButtonItemId).click()


while (True):
    try:
        driver.get(driver.current_url)

        list = re.findall(r'\b\d+\b', imageProcessing())
        number1 = int(list[0])
        number2 = int(list[1])

        # Recaptcha calculation
        sum = number1 + number2

        # Entering data
        enterKeys()

        if (
                "Type your login pages message in the page source for wrong recaptcha try" in driver.page_source):  # ____ IMPORTANT_____
            driver.find_element_by_id(usernameItemId).send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id(usernameItemId).send_keys(Keys.DELETE)
            driver.find_element_by_id(passwordItemId).send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id(passwordItemId).send_keys(Keys.DELETE)
            driver.find_element_by_id(secureCodItemId).send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id(secureCodItemId).send_keys(Keys.DELETE)
        else:
            break
    except IndexError:
        pass

getSource = driver.page_source
driver.quit()
print(getSource)  # Result
