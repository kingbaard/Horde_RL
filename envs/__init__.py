from gymnasium.envs.registration import register

register(
    id="hordeRL-v0",
    entry_point="envs:HordeEnv",
    max_episode_steps=10000,
    kwargs="render_mode='human'"
)