import numpy as np

# Create Q-table
# Current Quad * 
num_states = 216
num_actions = 3 * 3 * 5
Q = np.zeros((num_states, num_actions))

class Agent():
    def __init__(self, learning_rate, gamma, epsilon):
        self.num_states = 216
        self.num_actions = 3 * 3 * 6
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
            action_index = np.argmax(self.Q[state])
        return self.decode_action(action_index)
    
    def learn(self, state, action, reward, next_state, next_action):
        action_index = self.encode_action(action)
        next_action_index = self.encode_action(next_action)
    
        predict = self.Q[state, action_index]
        target = reward + self.gamma * self.Q[next_state, next_action_index]
        self.Q[state, action_index] += self.learning_rate * (target - predict)
        
    def set_epsilon(self, new_value): 
        self.epsilon = new_value 
        
    def encode_action(self, action):
        index = action[0]
        index += action[1] * 3
        index += action[2] * 9

        return index
    
    def decode_action(self, index):
        shoot_dir = index // 9
        index = index % 9
    
        ver_dir = index // 3
        hor_dir = index % 3
    
        return (hor_dir, ver_dir, shoot_dir)