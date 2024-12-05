import time
import random
from selenium.webdriver.common.action_chains import ActionChains

def scroll(driver, pause_range=(2, 5), pause_frequency=0.001, scroll_amount=(0.4, 0.6), inertia_factor = 0.3):
    action = ActionChains(driver)
    current_position = 0
    end_of_page = False
    velocity = 0
    max_velocity = random.uniform(*scroll_amount)

    while not end_of_page:
        # simulate inertia-based scrolling
        if velocity < max_velocity:
            velocity += random.uniform(0, inertia_factor)

        # add random pauses to mimic a real person scrolling
        if random.uniform(0, 1) < pause_frequency:
            print("Pausing")
            time.sleep(random.uniform(*pause_range))
            velocity = random.uniform(0, max_velocity * inertia_factor)
        else: 
            print("Scrolling")
        # scroll
        current_position += velocity
        driver.execute_script(f"window.scrollTo(0, {current_position});")

        #decelerate slighly, with a little noise, without getting too extreme
        velocity *= (1 - inertia_factor/2)
        velocity += random.uniform(-inertia_factor/4, inertia_factor/4)
        velocity = max(min(velocity, max_velocity), -max_velocity)

        # add some mouse movement noise to mimic a real person scrolling
        # if random.uniform(0, 1) < 0.3:  # 30% chance to move the mouse
        #     action.move_by_offset(random.uniform(-3, 3), random.uniform(-3, 3)).perform()

        # check if end of page
        end_of_page = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight")
        time.sleep(random.uniform(0.00005, 0.00015))

