import numpy as np

# Create Q-table
# Current Quad * 
num_states = 216
num_actions = 3 * 3 * 5
Q = np.zeros((num_states, num_actions))

class Agent():
    def __init__(self, learning_rate, gamma, epsilon):
        self.num_states = 216
        self.num_actions = 3 * 3 * 5
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros((self.num_states, num_actions))

    def observe(self, state):
        pass

    #Epsilon greedy policy
    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(self.num_actions)
        else:
            encoded_state = self.encode_state(state)
            action_index = np.argmax(self.Q[encoded_state])
        return self.decode_action(action_index)
    
    def learn(self, state, action, reward, next_state, next_action):
        action_index = self.encode_action(action)
        state_index = self.encode_state(state)
        next_action_index = self.encode_action(next_action)
        next_state_index = self.encode_state(next_state)
    
        predict = self.Q[state_index , action_index]
        target = reward + self.gamma * self.Q[next_state_index, next_action_index]
        self.Q[state, action_index] += self.learning_rate * (target - predict)
        
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

    def encode_state(self, state):
        index = state[0]
        for e_zone, e_distance in state[1]: 
            index += e_zone * 8
            index += e_distance * 3

        return int(index)

    def decode_state(self, index):
        enemy_distance = index // 3
        index = index % 3

        enemy_data = []
        for i in range(5):
            e_zone = index // 8
            e_distance = index // 3 if i != 4 else index % 8
            enemy_data.append(e_zone, e_distance)

        return (player_zone, enemy_data)