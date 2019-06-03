from selenium import webdriver

Input = 'Refresh the website and move to "https://www.naver.com/".'

driver_path = "./../dat/chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)
driver.get('https://google.com')

# refresh the website .
driver.refresh()

# move to "https://www.naver.com/" .
driver.get('https://www.naver.com/')
