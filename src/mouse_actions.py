import random
from constants import CLICK_OFFSET_RANGE, CLICK_DURATION_RANGE, MOUSE_MOVEMENT_OFFSET_RANGE

def click(bot, target):
    x_offset = random.uniform(*CLICK_OFFSET_RANGE)
    y_offset = random.uniform(*CLICK_OFFSET_RANGE)
    click_duration = random.uniform(*CLICK_DURATION_RANGE)
    bot.cursor.click_on(target, relative_position=[x_offset, y_offset], click_duration = click_duration)
    return

def randomMouseMovement(bot):
    x_offset = random.uniform(*MOUSE_MOVEMENT_OFFSET_RANGE)
    y_offset = random.uniform(*MOUSE_MOVEMENT_OFFSET_RANGE)
    bot.cursor.move_to([x_offset, y_offset], absolute_offset=True)
    return

def randomClick(bot):
    click_duration = random.uniform(*CLICK_DURATION_RANGE)
    bot.cursor.click(click_duration = click_duration)
    return