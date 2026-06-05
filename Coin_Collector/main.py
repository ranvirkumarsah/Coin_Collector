from tkinter import messagebox as mb
import pygame
import pygame_menu
import random
import json
import math
import time
import sys
import os

pygame.init()

IS_ANDROID = 'ANDROID_ARGUMENT' in os.environ or sys.platform == 'android'
BASE_DIR = os.path.dirname(os.fspath(__file__))

width = 800
height = 600

score = 0
coins = 0
limit = 30
rate = 60
mode = 2
speed = 2
gain = 50
fox_x = 5
fox_y = 60
coin_x = random.randint(5, 335)
coin_y = random.randint(5, 315)
username = "Player1"
password = ""
filename = os.path.join(BASE_DIR, "save_data.json")
clock = pygame.time.Clock()
speed_power_ups = 0
joy_base_center = (60, 340)
stick_x, stick_y = joy_base_center
joystick_vector_x = 0.0
joystick_vector_y = 0.0
is_dragging = False
running = True

if IS_ANDROID:
    info = pygame.display.Info()
    play_width, play_height = info.current_w, info.current_h
    joy_base_center = (80, play_height - 80)
else:
    play_width, play_height = 400, 400
    joy_base_center = (60, 340)

stick_x, stick_y = joy_base_center

screen = pygame.display.set_mode((play_width, play_height)) if IS_ANDROID else pygame.display.set_mode((width, height))
pygame.display.set_caption('Coin Collector')
font = pygame.font.SysFont("Calibri", 36)

coin = pygame.image.load(os.path.join(BASE_DIR, 'Assets', 'coin.png'))
fox = pygame.image.load(os.path.join(BASE_DIR, 'Assets', 'fox.png'))

if IS_ANDROID:
    joysick_check = True
    arrow_key_check = False
else:
    joysick_check = False
    arrow_key_check = True

my_theme = pygame_menu.themes.Theme(
    background_color=(20, 20, 20),
    title_background_color=(120, 0, 0),
    title_font_color=(255, 255, 255),
    widget_font_color=(200, 200, 200),
    widget_font_shadow_color=(255, 0, 0)
)

def load_json():
    global filename
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_json():
    global filename, username, password, coins, speed_power_ups
    data = load_json()
    data[username] = {
        "password": password,
        "coins": coins,
        "powerups": speed_power_ups
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def submit_login():
    global username, password, coins, speed_power_ups
    data = load_json()

    if data == {}:
        mb.showerror("Error", "Username not found. Please sign up.")
        return

    if username in data:
        if data[username]["password"] == password:
            coins = data[username]["coins"]
            speed_power_ups = data[username]["powerups"]
        else:
            mb.showerror("Error", "Incorrect password")
            return
    else:
        mb.showerror("Error", "Username not found. Please sign up.")
        return

    username_label.set_title(f"Username: {username}")
    coin_label.set_title(f"Coins: {coins}")
    powerup_label.set_title(f"Powerups: {speed_power_ups}")

    login_menu.disable()

def sign_up():
    global username, password
    data = load_json()

    if username in data:
        mb.showerror("Error", "Username already exists; choose another one.")
        return
    elif len(password) < 5:
        mb.showerror("Error", "Password must be at least 5 characters.")
    else:
        save_json()
        submit_login()

def close_app():
    save_json()
    pygame.quit()
    sys.exit()

def set_username(name):
    global username
    username = name

def set_password(key):
    global password
    password = key

def set_mode(selected_tuple, value):
    global mode
    mode = value

def set_joystick_or_arrow_keys(selected_tuple, value):
    global joysick_check, arrow_key_check
    MODE = value
    if MODE == 1:
        arrow_key_check = True
        joysick_check = False
    if MODE == 2:
        joysick_check = True
        arrow_key_check = False


def get_speed_powerup():
    global speed_power_ups, coins
    if coins >= 1000:
        speed_power_ups += 1
        coins -= 1000
        coin_label.set_title(f"Coins: {coins}")
        powerup_label.set_title(f"Powerups: {speed_power_ups}")

    save_json()

def play():
    global running, mode, speed_power_ups, clock, score, speed, limit, screen, coin, fox, fox_x, fox_y,coin_x, coin_y, coins, gain, joy_base_center, stick_y, stick_x, is_dragging, joysick_check, arrow_key_check, stick_x, stick_y, joystick_vector_y, joystick_vector_x, play_width, play_height
    score = 0
    if mode == 10:
        gain = 10
        limit = 10
    elif mode == 30:
        gain = 5
        limit = 30
    elif mode == 60:
        gain = 1
        limit = 60
    else:
        gain = 5
        limit = 30

    if speed_power_ups >= 1:
        speed_power_ups -= 1
        speed = 4
        powerup_label.set_title(f"Powerups: {speed_power_ups}")
        save_json()
    else:
        speed = 2

    screen = pygame.display.set_mode((play_width, play_height))
    start_ticks = pygame.time.get_ticks()
    limit_in_ms = limit * 1000

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_AC_BACK):
                running = False

        msp = pygame.time.get_ticks() - start_ticks
        time_left = (limit_in_ms - msp) // 1000
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        joysick_vector_x = 0.0
        joysick_vector_y = 0.0

        if msp > limit_in_ms:
            time.sleep(1)
            running = False

        screen.fill((0, 255, 0))
        screen.blit(fox, (fox_x, fox_y))
        screen.blit(coin, (coin_x, coin_y))

        if joysick_check:
            pygame.draw.circle(screen, (40, 40, 40), joy_base_center, 45, width=8)
            pygame.draw.circle(screen, (50, 50, 50), (int(stick_x), int(stick_y)), 15)

        if arrow_key_check:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                fox_x -= speed
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                fox_x += speed
            if pygame.key.get_pressed()[pygame.K_UP]:
                fox_y -= speed
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                fox_y += speed

        if joysick_check:
            if left_click:
                dx = mouse_pos[0] - joy_base_center[0]
                dy = mouse_pos[1] - joy_base_center[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if not is_dragging and distance <= 60:
                    is_dragging = True

                if is_dragging:
                    if distance <= 45:
                        stick_x = mouse_pos[0]
                        stick_y = mouse_pos[1]
                    else:
                        angle = math.atan2(dy, dx)
                        stick_x = joy_base_center[0] + math.cos(angle) * 45
                        stick_y = joy_base_center[1] + math.sin(angle) * 45

                    joystick_vector_x = (stick_x - joy_base_center[0]) / 45
                    joystick_vector_y = (stick_y - joy_base_center[1]) / 45
            else:
                is_dragging = False
                stick_x, stick_y = joy_base_center

            fox_x += joystick_vector_x * speed
            fox_y += joystick_vector_y * speed

        if fox_x >= play_width - 65:
            fox_x = play_width - 65
        if fox_x < 5:
            fox_x = 5
        if fox_y >= play_height - 85:
            fox_y = play_height - 85
        if fox_y < 5:
            fox_y = 5

        scoreboard = font.render(f"Score: {score}", True, (0, 0, 0))
        timer = font.render(f"Time left: {time_left}", True, (0, 0, 0))
        screen.blit(scoreboard, (0, 0))
        screen.blit(timer, (0, 30))

        fox_rect = fox.get_rect(topleft=(fox_x, fox_y))
        coin_rect = coin.get_rect(topleft=(coin_x, coin_y))

        if fox_rect.colliderect(coin_rect):
            score += gain
            coin_x = random.randint(5, 335)
            coin_y = random.randint(5, 315)

        pygame.display.flip()
        clock.tick(rate)

    screen = pygame.display.set_mode((width, height)) if not IS_ANDROID else pygame.display.set_mode((play_width, play_height))
    coins += score
    coin_label.set_title(f"Coins: {coins}")
    menu.resize(width, height)
    running = True
    save_json()

login_menu = pygame_menu.Menu(width=play_width, height=play_height, theme=my_theme, title='Login') if IS_ANDROID else pygame_menu.Menu(width=width, height=height, theme=my_theme, title='Login')
username_input = login_menu.add.text_input("Username: ", default="Player1", onchange=set_username)
password_input = login_menu.add.text_input("Password(min 5 chars): ", default="", onchange=set_password, password=True)
login_menu.add.button(title="Login", action=submit_login)
login_menu.add.button(title="Sign Up", action=sign_up)

menu = pygame_menu.Menu(width=play_width, height=play_height, title='Coin Collector', theme=my_theme, center_content=False) if IS_ANDROID else pygame_menu.Menu(width=width, height=height, theme=my_theme, center_content=False, title='Coin Collector')
menu.add.vertical_margin(20)
username_label = menu.add.label(title=f"Username: {username}", font_size=40, align=pygame_menu.locals.ALIGN_LEFT)
coin_label = menu.add.label(title=f"Coins: {coins}", font_size=40, align=pygame_menu.locals.ALIGN_LEFT)
powerup_label = menu.add.label(title=f"Powerups: {speed_power_ups}", font_size=40, align=pygame_menu.locals.ALIGN_LEFT)
menu.add.vertical_margin(50)
menu.add.selector('Mode: ', [('Leisure (60s)', 60), ('Normal (30s)', 30), ('Speedrun (10s)', 10)], onchange=set_mode, default=1)
menu.add.selector('Controls: ', [('Arrow Keys', 1), ('Mousepad Joystick', 2)], onchange=set_joystick_or_arrow_keys, default=0)
menu.add.button(title="Extra Speed (1000 coins)", action=get_speed_powerup)
menu.add.vertical_margin(10)
play_button = menu.add.button(title="Play", action=play)
play_button.resize(width=120, height=80)

login_menu.mainloop(screen)
menu.mainloop(screen)
close_app()