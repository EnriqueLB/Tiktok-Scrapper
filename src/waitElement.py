from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def waitElement(driver, path, time, selector):
    time = time or 15
    try:
        return WebDriverWait(driver, time).until( #using explicit wait for 10 seconds
            EC.presence_of_element_located((selector, path)) #finding the element
        )
    except TimeoutException:
        print("tiempo agotado")
        return

def waitElements(driver, path, time, selector):
    time = time or 15
    try:
        return WebDriverWait(driver, time).until( #using explicit wait for 10 seconds
            EC.presence_of_all_elements_located((selector, path)) #finding the element
        )
    except TimeoutException:
        print("tiempo agotaddo")
        return