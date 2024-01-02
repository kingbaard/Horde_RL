import math
import numpy as np
import pygame
import random
import cv2

from Constants import *
from GameObjects import Player, Enemy, Bullet


# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

be_delete_queue = []

class GameEnv():
    def __init__(self, render_mode) -> None:
        self.render_mode = render_mode
        self.reset()

    def step(self, action):
        # move logic for updating agents, etc.
        hor_dir, ver_dir, shoot_dir = action
        self.handle_player_movement(hor_dir=hor_dir, ver_dir=ver_dir)
        self.handle_bullets()
        self.handle_enemies()
        self.handle_shoot(shoot_dir=shoot_dir)
        # self.enemy_spawn_check()
        image = self.get_screenshot()
        self.delete_objects()
        # print(f"self.spawn_cooldown: {self.spawn_cooldown}")

        if self.render_mode == 'human':
            self.render()
            # self.clock.tick(30)

        observation = self.get_state()
        reward = self.get_reward(observation)
        is_done = not self.is_alive
        info = {}
        return observation, reward, is_done, info

    def reset(self):
        pygame.init()
        if self.render_mode == 'human':
            pygame.display.set_caption("Horde RL")
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.is_done = False
        self.is_alive = True
        self.last_shoot_tick = 0
        self.last_spawn_tick = 0
        self.enemy_spawn_timer = 10
        self.player = Player(WIDTH-WIDTH/2, HEIGHT-HEIGHT/2, 20, 20)
        self.enemies = []
        self.spawn_enemies(5)
        self.bullets = []
        self.kill_count = 0
        self.spawn_count = 1
        self.spawn_cooldown = 10000
        self.closest_enemy = None

        self.enemy_eliminated = False

        self.delete_queue = []

        return self.get_state()

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

    def respawn_enemy(self, e):
        point_on_border = random.randint(0, WIDTH*2 + HEIGHT*2)
        spawn_pos_x, spawn_pos_y = get_spawn_location(point_on_border=point_on_border)
        e.x = spawn_pos_x
        e.y = spawn_pos_y


    def handle_enemies(self):
        for e in self.enemies:
            e.chase(self.player)
            if e.rect.colliderect(self.player.rect):
                # print("Enemy collide")
                self.player.is_alive == False
                self.is_alive = False
                self.enemies = []

    def handle_bullets(self):
        for b in self.bullets:
            b.move()
            for e in self.enemies:
                if b.rect.colliderect(e.rect):
                    self.delete_queue.append(b)
                    self.enemy_eliminated = True
                    self.kill_count += 1
                    self.respawn_enemy(e)
                    # self.set_difficulty()
                    print("enemy killed!")

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
        for b in self.delete_queue:
            if b in self.bullets:
                self.bullets.remove(b)
            self.delete_queue.remove(b)

    def close(self):
        pygame.quit()

    def get_state(self):
        if not self.enemies:
            return [4, [(0, 2) for _ in range(5)]] 
        # What zone is player in, closest enemy theta zone and distance number
        vertical_index = self.player.y // (HEIGHT // 3)
        horizontal_index = self.player.x // (WIDTH // 3)
        player_zone = vertical_index * 3 + horizontal_index

        all_enemy_data = []
        # get enemy
        for e in self.enemies:
            player_pos = (self.player.x, self.player.y)
            dx = player_pos[0] - e.x
            dy = player_pos[1] - e.y
            distance_sq = dx **2 + dy**2
            
            #Find E theta zone
            # N -> 0, NE -> 1, W -> 2, SE -> 3, S -> 4, SW -> 5, W -> 6, NW-> 7
            e_theta = 0 
            dx = player_pos[0] - e.x
            dy = player_pos[1] - e.y
            e_theta = np.arctan2(dy, dx)
            enemy_theta_zone = 0

            if math.pi/2 <= e_theta < math.pi:
                enemy_theta_zone = 1
            elif  -math.pi <= e_theta < -math.pi/2:
                enemy_theta_zone = 3
            elif -math.pi/2 <= e_theta < 0:
                enemy_theta_zone = 5
            elif 0 <= e_theta < math.pi/2:
                enemy_theta_zone = 7

            if player_pos[0] < e.x < player_pos[0] + 20:
                if e.y < player_pos[1]:
                    enemy_theta_zone = 0
                elif e.y > player_pos[1]:
                    enemy_theta_zone = 4
            elif player_pos[1] < e.y < player_pos[1] + 20: 
                if e.x < player_pos[0]:
                    enemy_theta_zone = 6
                elif e.x > player_pos[0]:
                    enemy_theta_zone = 2

            #Categorize e_distance between near, medium, and and far 
            e_distance_category = None
            match distance_sq:
                case  _ if distance_sq > 50000:
                    e_distance_category = 2 # Far
                case _ if distance_sq > 10000:
                    e_distance_category = 1 # Med
                case _:
                    e_distance_category = 0 # Close
            
            all_enemy_data.append((enemy_theta_zone, e_distance_category))

        # print(f"distance: {min_distance_sq}")
        # print(f'player_zone: {player_zone}\nenemy_theta_zone: {enemy_theta_zone}\ne_distance_category: {e_distance_category}')

        state = [int(player_zone), all_enemy_data]
        return state
    
    def get_reward(self, state):
        reward = 0
        # Reward for being alive this tick
        reward += 5

        # Distance from enemies, higher the better
        for e_zone, e_distance in state[1]:
            reward += e_distance * 10

            # Enemy is in shoot zone
            if e_zone in [0, 2, 4, 6]:
                reward += 5

        # Enemy elimination
        reward += 100 * self.enemy_eliminated
        self.enemy_eliminated = False

        if not self.player.is_alive:
            reward = -5000
        
        # print(reward)
        return reward
    
    def get_nearby_enemies(self):
        vertical_index = self.player.y // (HEIGHT // 3)
        horizontal_index = self.player.x // (WIDTH // 3)
        player_zone = vertical_index * 3 + horizontal_index

    def get_screenshot(self):
        pygame_surface = pygame.display.get_surface()
        surface_data = pygame.image.tostring(pygame_surface, 'RGB')
        cv_image = np.fromstring(surface_data, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        
        return cv_image

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