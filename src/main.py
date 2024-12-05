from selenium import webdriver
from navigation import scroll
from constants import URL
from keys import AUTH_COOKIE

# Launch Chrome, go to URL, login
driver = webdriver.Chrome()
driver.get(URL)
driver.add_cookie(AUTH_COOKIE)
driver.refresh()

# scroll 
scroll(driver)


input("Press Enter to close the browser...")  # Keeps the window open until you press Enter
driver.quit() 