from selenium import webdriver

Input = 'Wait the "3 seconds".'

driver_path = "./../dat/chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)
driver.get('https://google.com')

# wait the "3 seconds" .
import time
time.sleep(3)
