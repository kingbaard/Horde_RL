from environment import GameEnv
from Agent import Agent

agent = Agent(0.1, 0.9, 0.1)
env = GameEnv()

minimum_epsilon = 0.01 
decay_factor = 0.995
epsilon = 0.95

def main():
    for episode in range(1000):
        print(f"episode #{episode}")
        state = env.reset()
        action = agent.choose_action(state)
        done = False
        env.is_done == False 

        while not done:
            next_state, reward, done, _ = env.step(action)
            # print(f'next_state: {next_state}')
            next_action = agent.choose_action(next_state)
            agent.learn(state, action, reward, next_state, next_action)

            state = next_state
            action = next_action

            if agent.epsilon > minimum_epsilon:
                agent.epsilon *= decay_factor

        print(f"Reward: {reward}")

if __name__ == '__main__':
    main()