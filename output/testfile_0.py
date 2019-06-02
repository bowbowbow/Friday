from selenium import webdriver

Input = 'Enter the "KAIST" in "SearchBox" and click the "Search" button'

driver_path = "./../dat/chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)
driver.get('https://google.com')

# enter the "KAIST" in "SearchBox" .
driver.find_element_by_name('q').send_keys('KAIST')

# click the "Search" button .
driver.find_element_by_name("btnK").click()
