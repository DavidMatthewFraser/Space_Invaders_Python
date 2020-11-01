# Clone of https://www.youtube.com/watch?v=Q-__8Xw9KTM
# Left off 1:15:21

import pygame
import os
import time
import random

# Window Vars
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter");
# Font
pygame.font.init()
# Background Image
STARS = pygame.image.load(os.path.join("assets", "stars.png"))
STARS = pygame.transform.scale(STARS, (WIDTH, HEIGHT)) # stretch background image
# Enemy Images
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_laser.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "blue_ship.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "green_laser.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "green_ship.png"))
RED_SHIP = pygame.image.load(os.path.join("assets", "red_ship.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "red_laser.png"))
# Player Images
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "yellow_ship.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "yellow_laser.png"))

# Abstract ship class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        # Masks allow for pixel-perfect collision (image is not treated as a square)
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, speed):
        self.y += speed
    
# Abstract ship class
class Ship:
    def __init__(self, x, y, health=100): #constructor
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        # Masks allow for pixel-perfect collision (image is not treated as a square)
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # Masks allow for pixel-perfect collision (image is not treated as a square)
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self, speed):
        self.y += speed

def main():
    # setup vars
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 50)
    lost = False
    lost_count = 0
    # player vars
    level = 1
    lives = 5
    player_speed = 5
    player = Player(300, 650)
    # enemy vars
    enemies = []
    wave_length = 5
    enemy_speed = 5
    # level one setup
    for i in range(wave_length):
                random_x = random.randrange(50, WIDTH-50)
                random_y = random.randrange(-1500, -100)
                random_color = random.choice(["red", "blue", "green"])
                enemy = Enemy(random_x, random_y, random_color)
                enemies.append(enemy)
    def draw_window():
        # background
        WIN.blit(STARS, (0, 0))
        # text
        level_label = font.render(f"level: {level}", 1, (0, 255, 0))
        lives_label = font.render(f"lives: {lives}", 1, (255, 0, 0))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # draw enemies
        for enemy in enemies:
            enemy.draw(WIN)
        # draw player
        player.draw(WIN)
        # loosing screen
        if lost:
            lost_label = font.render("You Loose", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        # update window
        pygame.display.update()
    while run:
        # Refresh window
        draw_window()
        clock.tick(FPS)
        # check for game over
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            if lost_count  > 60:
                run = False
            else:
                continue
        # Check for window exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        # Initialize next Level
        if len(enemies) == 0:
            level += 1
            # wave_length += 5
            for i in range(wave_length):
                random_x = random.randrange(50, WIDTH-50)
                random_y = random.randrange(-1500, -100)
                random_color = random.choice(["red", "blue", "green"])
                enemy = Enemy(random_x, random_y, random_color)
                enemies.append(enemy)
        # Move player with WASD
        if keys[pygame.K_a] and player.x - player_speed > 0: # left
            player.x -= player_speed
        if keys[pygame.K_d] and player.x + player_speed + player.get_width() < WIDTH: # right
            player.x += player_speed
        if keys[pygame.K_w] and player.y - player_speed > 0: # up
            player.y -= player_speed
        if keys[pygame.K_s] and player.y + player_speed + player.get_height() < HEIGHT: # down
            player.y += player_speed
        # Move enemies
        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

main()