import math
import pygame
import random

from Constants import *
from GameObjects import Player, Enemy, Bullet
from Agent import Agent

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

be_delete_queue = []

class GameEnv():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Horde RL")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()

        self.last_shoot_tick = 0
        self.enemy_spawn_timer = 
        self.player = Player(WIDTH-WIDTH/2, HEIGHT-HEIGHT/2, 20, 20)
        self.enemies = []
        self.spawn_enemies(10)
        self.bullets = []

        self.enemy_eliminated = False

        self.delete_queue = []

    def step(self, hor_dir, ver_dir, shoot_dir):
        # move logic for updating agents, etc.
        self.clock.tick()
        observation = self.get_state()
        reward = self.get_reward()
        is_done = self.is_done()
        info = {}

        self.handle_bullets()
        self.handle_enemies()
        self.handle_player_movement(hor_dir=hor_dir, ver_dir=ver_dir)
        self.handle_shoot(shoot_dir=shoot_dir)

        if self.render_mode == 'human':
            self.render()

        

        return observation, reward, is_done, info

    def reset(self):
        pygame.init()
        pygame.display.set_caption("Horde RL")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()

        self.last_shoot_tick = 0 
        self.player = Player(WIDTH-WIDTH/2, HEIGHT-HEIGHT/2, 20, 20)
        self.enemies = []
        self.spawn_enemies(10)
        self.bullets = []

        self.delete_queue = []

    def render(self):
        if self.render_mode == 'human':
            self.screen.fill(BLACK)
            self.player.render(self.screen)

            for e in self.enemies:
                e.render(self.screen)

            for b in self.bullets:
                b.render(self.screen)

            pygame.display.flip()

    def handle_player_movement(self, hor_dir, ver_dir):
        # Player
        player_dx = 0
        player_dy = 0
        match hor_dir:
            case 0: 
                player_dx = 0 if self.player.x < 0 else -PLAYER_SPEED
            case 1:
                player_dx = 0 if self.player.x > (WIDTH - self.player.width) else PLAYER_SPEED
            case _:
                player_dx = 0 
        
        match ver_dir:
            case 0: 
                player_dy = 0 if self.player.y < 0 else -PLAYER_SPEED
            case 1:
                player_dy = 0 if self.player.y < (HEIGHT - self.player.height) else PLAYER_SPEED
            case _:
                player_dy = 0 

        self.player.slide(player_dx, player_dy)

    def spawn_enemies(self, count):
        for _ in count:
            self.spawn_enemy()

    def spawn_enemy(self):
        spawn_pos = (0, 0)
        point_on_border = random.randint(0, WIDTH*2 + HEIGHT*2)
        if point_on_border < WIDTH: # Top edge
            spawn_pos = (point_on_border, 0)
        point_on_border -= WIDTH 

        if point_on_border < HEIGHT: # Right edge
            spawn_pos = (WIDTH, point_on_border)
        point_on_border -= HEIGHT 

        if point_on_border < WIDTH: # Bottom edge
            spawn_pos = (WIDTH - point_on_border, HEIGHT)
        point_on_border -= WIDTH

        spawn_pos = (0, HEIGHT - point_on_border) # Left edge

        self.enemies.append(Enemy(spawn_pos[0], spawn_pos[0], 10, 10))
        

    def handle_enemies(self):
        for e in self.enemies:
            e.chase(self.player)
            if e.rect.colliderect(self.player.rect):
                self.player.is_alive == False
            e.render(self.screen)

    def handle_bullets(self):
        for b in self.bullets:
            b.move()
            for e in self.enemies:
                if b.rect.colliderect(e.rect):
                    self.delete_queue.append((b, e))
                    self.enemy_eliminated = True
            b.render(self.screen)

    def handle_shoot(self, shoot_dir):
        can_shoot = pygame.time.get_ticks() - self.last_shoot_tick >= GUN_COOLDOWN
        if shoot_dir != 4 and can_shoot:
            match shoot_dir:
                case 0:
                    self.bullets.append(Bullet(self.player.x, self.player.y + (self.player.height / 2), LEFT))
                case 1:
                    self.bullets.append(Bullet(self.player.x + self.player.width, self.player.y + (self.player.height / 2), RIGHT))
                case 2:
                    self.bullets.append(Bullet(self.player.x + (self.player.width /2), self.player.y, UP))
                case 3:
                    self.bullets.append(Bullet(self.player.x  + (self.player.width /2), self.player.y, DOWN))
                case _:
                    pass
            self.last_shoot_tick = pygame.time.get_ticks()

    def close(self):
        pygame.quit()

    def get_state(self):
        # [[player_posX, player_posY], [enemy pos]]
        state = [
            [self.player.x, self.player.y],
            [[e.x, e.y] for e in self.enemies]
        ]
        return state
    
    def get_reward(self):
        reward 
        # Reward for being alive this tick
        reward += 1

        # Distance from enemies, higher the better
        min_distance = min([math.dist(e.x, e.y) for e in self.enemies])

        # Enemy elimination
        reward += 10 * self.enemy_eliminated
        self.enemy_eliminated = False

        if not self.player.is_alive:
            reward = -50

        return reward


## Game loop
running = True
while running:
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

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

pygame.quit()