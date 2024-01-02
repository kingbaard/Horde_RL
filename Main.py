

from environment import GameEnv
from Agent import Agent

import matplotlib.pyplot as plt

agent = Agent(0.1, 0.9, 0.99)
env = GameEnv('human')

minimum_epsilon = 0.01 
decay_factor = 0.995
epsilon = 0.95

reward_history = []

def main():
    for episode in range(1000):
        # print(f"episode #{episode}")
        state = env.reset()
        action = agent.choose_action(state)
        done = False
        env.is_done == False 

        reward_total = 0
        while not done:
            next_state, reward, done, _ = env.step(action)
            # print(f'next_state: {next_state}')
            next_action = agent.choose_action(next_state)
            agent.learn(state, action, reward, next_state, next_action)
            reward_total += reward
            state = next_state
            action = next_action

            if agent.epsilon > minimum_epsilon:
                agent.epsilon *= decay_factor

        print(f"Reward: {reward_total}")
        reward_history.append(reward_total)

    plt.plot(reward_history)
    plt.show()

if __name__ == '__main__':

    main()