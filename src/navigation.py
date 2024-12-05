import time
import random
from selenium.webdriver.common.action_chains import ActionChains

def scroll(driver, pause_range=(2, 5), pause_frequency=0.001, scroll_amount=(0.4, 0.6)):
    action = ActionChains(driver)
    current_position = 0
    end_of_page = False

    while not end_of_page:
        # add random pauses to mimic a real person scrolling
        if random.uniform(0, 1) < pause_frequency:
            print("Pausing")
            time.sleep(random.uniform(*pause_range))
        else: 
            print("Scrolling")
        # scroll
        current_position += random.uniform(*scroll_amount)
        driver.execute_script(f"window.scrollTo(0, {current_position});")

        # add some mouse movement noise to mimic a real person scrolling
        # if random.uniform(0, 1) < 0.3:  # 30% chance to move the mouse
        #     action.move_by_offset(random.uniform(-3, 3), random.uniform(-3, 3)).perform()

        # check if end of page
        end_of_page = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight")
        time.sleep(random.uniform(0.00005, 0.00015))

