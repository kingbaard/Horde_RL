

from environment import HordeEnv
from Agent import Agent

import matplotlib.pyplot as plt

agent = Agent(0.1, 0.9, 0.99)
env = HordeEnv('human')

minimum_epsilon = 0.01 
decay_factor = 0.995
epsilon = 0.95

reward_history = []

def main():
    for episode in range(1000):
        print(f"episode #{episode}")
        state = env.reset()
        action = agent.choose_action(state)
        done = False
        env.is_done == False 

        reward_total = 0
        while not done:
            next_state, reward, done, _ = env.step(action)

            action = agent.choose_action_DQN(state)

            # next_action = agent.choose_action(next_state)
            # agent.learn(state, action, reward, next_state, next_action)
            reward_total += reward
            state = next_state
            agent.memory.append((state, action, reward, next_state, done))
            # if agent.epsilon > minimum_epsilon:
            #     agent.epsilon *= decay_factor
            agent.train_model()

        print(f"Reward: {reward_total}")
        reward_history.append(reward_total)

    plt.plot(reward_history)
    plt.show()

if __name__ == '__main__':

    main()