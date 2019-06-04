from selenium import webdriver

Input = 'Open the "https://google.com" and Enter the "Iron man" in #1 and click the #2. Wait the "3 seconds" and Check if "Robert Downey" is on the page.'

driver_path = "./../dat/chromedriver"
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(1)

# open the "https://google.com" .
driver.get('https://google.com')

# enter the "Iron man" in #1 .
driver.find_element_by_css_selector('.gLFyf').send_keys('Iron man')

# click the #2 .
driver.find_element_by_css_selector("center:nth-child(1) > .gNO89b").click()

# wait the "3 seconds" .
import time
time.sleep(3)

# check if "Robert Downey" is on the page .
assert "Robert Downey" in driver.page_source
