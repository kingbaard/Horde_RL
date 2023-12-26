
    
ACTIONS = [
    'move_left',
    'move_right',
    'move_up',
    'move_down',
    'shoot_left',
    'shoot_right',
    'shoot_up',
    'shoot_down',
]

HOR_DIR = [
    0, #left
    1, #right
    2, #no direction
]

VER_DIR = [
    0, #up
    1, #down
    2, #no direction
]

SHOOT_DIR = [
    0, #left
    1, #right
    2, #up
    3, #down
    4, #no shoot 
]

class Agent():
    def __init__(self, ):
        pass

    def observe(self, state):
        pass

    def decide_action(self):
        action = None
        return action
    
    def learn(self, reward):
        pass
    