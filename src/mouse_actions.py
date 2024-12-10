import random

def click(bot, target):
    x_offset = random.uniform(0.1, 0.9)
    y_offset = random.uniform(0.1, 0.9)
    click_duration = random.uniform(0.04, 0.08)
    bot.cursor.click_on(target, relative_position=[x_offset, y_offset], click_duration = click_duration)
    return

def randomMouseMovement(bot):
    x_offset = random.uniform(10, 100)
    y_offset = random.uniform(10, 100)
    bot.cursor.move_to([x_offset, y_offset], absolute_offset=True)
    return

def randomClick(bot):
    click_duration = random.uniform(0.04, 0.08)
    bot.cursor.click(click_duration = click_duration)
    return