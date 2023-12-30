import math
import numpy as np
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

        self.is_alive = True
        self.last_shoot_tick = 0
        self.last_spawn_tick = 0
        self.enemy_spawn_timer = 10
        self.player = Player(WIDTH-WIDTH/2, HEIGHT-HEIGHT/2, 20, 20)
        self.enemies = []
        self.spawn_enemies(10)
        self.bullets = []
        self.kill_count = 0
        self.spawn_count = 1
        self.spawn_cooldown = 10000

        self.enemy_eliminated = False

        self.delete_queue = []
        self.render_mode = 'human'

    def step(self, action):
        # move logic for updating agents, etc.
        hor_dir, ver_dir, shoot_dir = action
        self.handle_player_movement(hor_dir=hor_dir, ver_dir=ver_dir)
        self.handle_bullets()
        self.handle_enemies()
        self.handle_shoot(shoot_dir=shoot_dir)
        self.enemy_spawn_check()
        self.delete_objects()
        # print(f"self.spawn_cooldown: {self.spawn_cooldown}")

        if self.render_mode == 'human':
            self.render()
        
        self.clock.tick(FPS)
        observation = self.get_state()
        reward = self.get_reward()
        is_done = not self.is_alive
        info = {}
        return observation, reward, is_done, info

    def reset(self):
        pygame.init()
        pygame.display.set_caption("Horde RL")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.last_shoot_tick = 0 
        self.player = Player(WIDTH-WIDTH / 2, HEIGHT-HEIGHT / 2, 20, 20)
        self.enemies = []
        self.spawn_enemies(10)
        self.bullets = []

        self.spawn_count = 0

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
                player_dy = 0 if self.player.y > (HEIGHT - self.player.height) else PLAYER_SPEED
            case _:
                player_dy = 0 

        self.player.slide(player_dx, player_dy)

    def enemy_spawn_check(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.last_spawn_tick >= self.spawn_cooldown:
            self.spawn_count += 1
            print(f"Spawning enemy: {self.spawn_count}")
            self.spawn_enemies(self.spawn_count)
            self.last_spawn_tick = current_tick

    def set_difficulty(self):
        # print(f"Kill count: {self.kill_count}")
        match self.kill_count:
            case 3:
                self.spawn_cooldown = 9000
            case 6:
                self.spawn_cooldown = 8000
            case 9:
                self.spawn_cooldown = 7000
            case 12:
                self.spawn_cooldown = 6000
            case 15:
                self.spawn_cooldown = 5000
            case 18:
                self.spawn_cooldown = 10000
                self.spawn_count = 2
            case 21:
                self.spawn_cooldown = 9000
            case 24:
                self.spawn_cooldown = 8000
            case 27:
                self.spawn_cooldown = 7000
            case 30:
                self.spawn_count = 3
                self.spawn_cooldown = 10000

    def spawn_enemies(self, count):
        for _ in range(count):
            # print("enemy_spawned")
            self.spawn_enemy()

    def spawn_enemy(self):
        point_on_border = random.randint(0, WIDTH*2 + HEIGHT*2)
        spawn_pos_x, spawn_pos_y = get_spawn_location(point_on_border=point_on_border)
        self.enemies.append(Enemy(spawn_pos_x, spawn_pos_y, 10, 10))

    def handle_enemies(self):
        for e in self.enemies:
            e.chase(self.player)
            if e.rect.colliderect(self.player.rect):
                print("Enemy collide")
                self.player.is_alive == False
                self.is_alive = False
            e.render(self.screen)

    def handle_bullets(self):
        for b in self.bullets:
            b.move()
            for e in self.enemies:
                if b.rect.colliderect(e.rect):
                    self.delete_queue.append((b, e))
                    self.enemy_eliminated = True
                    self.kill_count += 1
                    self.set_difficulty()
                    print("enemy killed!")
            b.render(self.screen)

    def handle_shoot(self, shoot_dir):
        can_shoot = pygame.time.get_ticks() - self.last_shoot_tick >= GUN_COOLDOWN
        # print(can_shoot)
        if shoot_dir != 4 and can_shoot:
            match shoot_dir:
                case 0:
                    # print("shoot left")
                    self.bullets.append(Bullet(self.player.x, self.player.y + (self.player.height / 2), LEFT))
                case 1:
                    # print("shoot right")
                    self.bullets.append(Bullet(self.player.x + self.player.width, self.player.y + (self.player.height / 2), RIGHT))
                case 2:
                    # print("shoot up")
                    self.bullets.append(Bullet(self.player.x + (self.player.width /2), self.player.y, UP))
                case 3:
                    # print("shoot down")
                    self.bullets.append(Bullet(self.player.x  + (self.player.width /2), self.player.y, DOWN))
                case _:
                    pass
            self.last_shoot_tick = pygame.time.get_ticks()

    def delete_objects(self):
        for b, e in self.delete_queue:
            if b in self.bullets:
                self.bullets.remove(b)
            if e in self.enemies:
                self.enemies.remove(e)
            self.delete_queue.remove((b, e))

    def close(self):
        pygame.quit()

    def get_state(self):
        # What zone is player in, closest enemy theta zone and distance number
        vertical_index = self.player.y // (HEIGHT // 3)
        horizontal_index = self.player.x // (WIDTH // 3)
        player_zone = vertical_index * 3 + horizontal_index

        # get closest enemy info
        min_distance = 9999
        player_pos = (self.player.x, self.player.y)
        for e in self.enemies:
            e_distance = math.dist(player_pos, (e.x, e.y))
            if e_distance < min_distance:
                min_distance = e_distance
                closest_e = e
        
        #Find E theta zone
        # N -> 0, NE -> 1, W -> 2, SE -> 3, S -> 4, SW -> 5, W -> 6, NW-> 7
        dx = player_pos[0] - closest_e.x
        dy = player_pos[1] - closest_e.y
        e_theta = np.arctan2(dy, dx)
        enemy_theta_zone = 0

        #TODO: categorize e_distance between near, medium, and and far  

        if 0 <= e_theta < math.pi/2:
            enemy_theta_zone = 1
        elif  math.pi/2 <= e_theta < math.pi:
            enemy_theta_zone = 3
        elif (math.pi/2) * 3 <= e_theta < (math.pi/2) * 4:
            enemy_theta_zone = 5
        elif (math.pi/2) * 4 <= e_theta < (math.pi/2) * 5:
            enemy_theta_zone = 7

        if player_pos[0] < e.x < player_pos[0] + 20:
            if e.y < player_pos[1]:
                enemy_theta_zone = 0
            elif e.y > player_pos[1]:
                enemy_theta_zone = 2
        elif player_pos[1] < e.y < player_pos[1] + 20: 
            if e.x < player_pos[0]:
                enemy_theta_zone = 4
            elif e.x > player_pos[0]:
                enemy_theta_zone = 6

        state = [player_zone, enemy_theta_zone, min_distance]
        return state
    
    def get_reward(self):
        reward = 0
        # Reward for being alive this tick
        reward += 5

        # Distance from enemies, higher the better
        player_pos = (self.player.x, self.player.y)
        min_distance = min([math.dist((player_pos), (e.x, e.y)) for e in self.enemies])
        reward += min_distance / 10

        # Enemy elimination
        reward += 10 * self.enemy_eliminated
        self.enemy_eliminated = False

        if not self.player.is_alive:
            reward = -500
        
        # print(reward)
        return reward

def get_spawn_location(point_on_border):
    if point_on_border < WIDTH: # Top edge
            return (point_on_border, 0)
    point_on_border -= WIDTH 

    if point_on_border < HEIGHT: # Right edge
        return (WIDTH, point_on_border)
    point_on_border -= HEIGHT 

    if point_on_border < WIDTH: # Bottom edge
        return (WIDTH - point_on_border, HEIGHT)
    point_on_border -= WIDTH

    return (0, HEIGHT - point_on_border) # Left edge