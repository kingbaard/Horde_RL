import numpy as np
from HordeGame.HordeGame.Constants import *
import random

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque

from gym import spaces

class Agent():
    def __init__(self, learning_rate, gamma, epsilon):
        # self.observation_space = spaces.Box(low=0, high=3, shape=(60, 75), dtype=int )
        self.num_states = 71663616
        self.num_actions = 3 * 3 * 5
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        self.batch_size = 64
        self.memory = deque(maxlen=2000)
        self.model = self.build_model()
        self.Q = np.zeros((self.num_states, self.num_actions), dtype=np.int8)

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.num_states, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.num_actions, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(self.learning_rate))
        return model
    
    def train_model(self):
        if len(self.memory) < self.batch_size:
            return
        
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                state_index = self.encode_state(state)
                next_state_index = np.array([[self.encode_state(next_state)]])
                target = (reward + self.gamma * np.amax(self.model.predict([next_state_index])))
                target_f = self.model.predict(state_index)
                target_f[0][action] = target
                self.model.fit(state_index, target_f, epochs=1, verbose=0)
            
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def observe(self, state):
        pass

    #Epsilon greedy policy
    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(self.num_actions)
        else:
            action_index = np.argmax(self.Q[self.encode_state(state)])
        return self.decode_action(action_index)
    
    def choose_action_DQN(self, state):
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(self.num_actions)
        else:
            encoded_action = self.encode_state(state)
            print(encoded_action)
            action_index = np.argmax(self.model.predict([encoded_action]))
        return self.decode_action(action_index)
    
    def learn(self, state, action, reward, next_state, next_action):
        state_index = self.encode_state(state)
        action_index = self.encode_action(action)
        next_state_index = self.encode_state(next_state)
        next_action_index = self.encode_action(next_action)

    
        predict = self.Q[state , action_index]
        target = reward + self.gamma * self.Q[next_state_index, next_action_index]
        self.Q[state_index, action_index] += self.learning_rate * (target - predict)
        
    def set_epsilon(self, new_value): 
        self.epsilon = new_value 
        
    def encode_action(self, action):
        index = action[0]
        index += action[1] * 3
        index += action[2] * 5
        if index >= 45: 
            print(f'Action index is too great: {index}')
        return index
    
    def decode_action(self, index):
        shoot_dir = index // 5
        index = index % 5
    
        ver_dir = index // 3
        hor_dir = index % 3
    
        return (hor_dir, ver_dir, shoot_dir)
    
    # def encode_state(self, state):
    #     flattened_state = state.flatten()
    #     index = 0

    #     for i, val in enumerate(flattened_state):
    #         index += val * (4 * i)

    #     return index

    # def decode_state(self, index):
    #     shape = (WIDTH, HEIGHT)
    #     base4_digits = []

    #     while index > 0:
    #         base4_digits.append(index % 4)
    #         index = index // 4

    #     if len(base4_digits) < WIDTH * HEIGHT:
    #         base4_digits += [0] * (WIDTH * HEIGHT - len(base4_digits))

    #     img_1d = np.array(base4_digits)
    #     img_2d = img_1d.reshape(shape)
        
    #     return img_2d

    def encode_state(self, state):
        index = state[0]
        for e_zone, e_distance in state[1]: 
            index += e_zone * 8
            index += e_distance * 3

        return int(index)

    def decode_state(self, index):
        enemy_data = []
        for _ in range(5):
            e_distance = index // 3
            index = index % 3

            e_zone = index // 8
            index = index % 8
            enemy_data.append(e_zone, e_distance)

        return (index, enemy_data)