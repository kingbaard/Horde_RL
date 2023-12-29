import numpy as np

# Create Q-table
# Current Quad * 
num_states = 216
num_actions = 3 * 3 * 5
Q = np.zeros((num_states, num_actions))
    
def epsilon_greedy_policy(state, Q, epsilon);
    if np.random.rand() < epsilon:
        hor_dir = np.random.choice(HOR_DIR)
        ver_dir = np.random.choice(VER_DIR)
        shoot_dir = np.random.choice(SHOOT_DIR)
        return (hor_dir, ver_dir, shoot_dir)
    else:
        return np.argmax(Q[state])

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

    def decide_action(self):
        action = None
        return action
    
    def learn(self, reward):
        pass
        
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