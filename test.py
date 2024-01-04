import random
from environment import HordeEnv

# Initialize your environment
env = HordeEnv()

# Reset the environment
state = env.reset()
done = False

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

while not done:
    # Take a random action from the environment's action space
    hor_dir = random.choice(HOR_DIR)
    ver_dir = random.choice(VER_DIR)
    shoot_dir = random.choice(SHOOT_DIR)
    action = hor_dir, ver_dir, shoot_dir

    # Step the environment forward and print out the results
    state, reward, done, _ = env.step(action)
    # print(f"Action: {action} - State: {state} - Reward: {reward} - Done: {done}")

    # Optionally render the environment
    env.render()
