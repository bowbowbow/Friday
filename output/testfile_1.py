from selenium import webdriver

driver = webdriver.Chrome('./../dat/chromedriver')
driver.implicitly_wait(3)

driver.find_element_by_css_selector('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > div.LoginForm-input.LoginForm-username > input').send_keys('clsrn1581@gmail.com')
driver.find_element_by_css_selector('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > div.LoginForm-input.LoginForm-password > input').send_keys('qwer1234')

driver.find_element_by_css_selector('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > input.EdgeButton.EdgeButton--secondary.EdgeButton--medium.submit.js-submit').click()

assert "Notification" in driver.page_source

