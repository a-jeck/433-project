URL = "https://x.com"
# URL = "https://www.google.com/search?q=dogs"
AUTH_COOKIE = {"name": "auth_token", "value": "99c11c5cec133b84f242e1728b79f83e50720780", "domain": ".x.com"}

# Navigation
SCROLL_PAUSE_RANGE = (2, 5) # range of how long we'll pause while scrolling, seconds
PAUSE_FREQUENCY = 0.001 # How often we pause
SCROLL_AMOUNT = (0.4, 0.6) # How much we scroll each time we scroll
INERTIA_FACTOR = 0.3 # inertia of scrolling velocity
SCROLL_STEP_TIME = (0.00005, 0.00015) # how long we wait between each scroll, seconds
MAX_LOADING_WAIT = 20
