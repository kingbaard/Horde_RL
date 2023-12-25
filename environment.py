import pygame
import random

from Constants import *
from GameObjects import Player, Enemy, Bullet
from agent import Agent
PLAYER_SPEED = 3

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horde")
clock = pygame.time.Clock()     ## For syncing the FPS

## initilize gameobjects
player = Player(WIDTH-WIDTH/2, HEIGHT-HEIGHT/2, 20, 20)
enemies = [Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT), 10, 10) for _ in range(10)]
bullets = []

be_delete_queue = []

last_shoot_tick = 0

agent = Agent()

## Game loop
running = True
while running:
    state = get_game_state()

    agent.observe(state)
    action = agent.decide_action()

    implement_action(action)

    reward = get_reward(state, action)

    agent.learn(reward)
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        # player.x = 0 if player.x < 0 else player.x - PLAYER_SPEED
        player.slide(0 if player.x < 0 else -PLAYER_SPEED, 0)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        # player.x = (WIDTH - player.width) if player.x > (WIDTH - player.width) else player.x + PLAYER_SPEED
        player.slide(0 if player.x > (WIDTH - player.width) else PLAYER_SPEED, 0)
    if pygame.key.get_pressed()[pygame.K_UP]:
        # player.y = 0 if player.y < 0 else player.y - PLAYER_SPEED
        player.slide(0, 0 if player.y < 0 else -PLAYER_SPEED)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        player.y = (HEIGHT - player.height) if player.y > (HEIGHT - player.height) else player.y + PLAYER_SPEED
        player.slide(0, 0 if player.y > (HEIGHT - player.height) else PLAYER_SPEED)
    
    # Handle gun input
    current_time = pygame.time.get_ticks()
    if current_time - last_shoot_tick >= GUN_COOLDOWN and player.is_alive:
        if pygame.key.get_pressed()[pygame.K_w]:
            bullets.append(Bullet(player.x + (player.width /2), player.y, UP))
        elif pygame.key.get_pressed()[pygame.K_d]:
            bullets.append(Bullet(player.x + player.width, player.y + (player.height / 2), RIGHT))
        elif pygame.key.get_pressed()[pygame.K_s]:
            bullets.append(Bullet(player.x  + (player.width /2), player.y, DOWN))
        elif pygame.key.get_pressed()[pygame.K_a]:
            bullets.append(Bullet(player.x, player.y + (player.height / 2), LEFT))
        last_shoot_tick = current_time

    #2 Update
    for e in enemies:
        e.chase(player)
        if e.rect.colliderect(player.rect):
            print(f"Player rect: ({player.rect.centerx},{player.rect.centery})")
            player.is_alive == False

    for b in bullets:
        b.move()
        for e in enemies:
            if b.rect.colliderect(e.rect):
                be_delete_queue.append((b, e))

    #3 Draw/render
    screen.fill(BLACK)
    # if player.slash_rect:

    for e in enemies:
        if e.is_delete_queued:
            enemies.remove(e)
        e.render(screen)
    for b in bullets:
        b.render(screen)

    if player.is_alive:
        player.render(screen)

    # Delete
    for b, e in be_delete_queue:
        print(b)
        print(e)
        if b in bullets:
            bullets.remove(b)
        if e in enemies:
            enemies.remove(e)
        be_delete_queue.remove((b, e))

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()