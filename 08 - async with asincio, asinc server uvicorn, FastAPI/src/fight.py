import asyncio

from enum import Enum, auto
from random import choice, uniform


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


async def fight_agent(agent_: Agent, turns_, i):
    async for action in agent_:
        await asyncio.sleep(uniform(0.1, 0.5))
        if action == Action.HIGHKICK:
            turns_.append((Action.HIGHKICK, Action.HIGHBLOCK, agent_.health, i))
        elif action == Action.HIGHBLOCK:
            agent_.health -= 1
            turns_.append((Action.HIGHBLOCK, Action.LOWKICK, agent_.health, i))
        elif action == Action.LOWKICK:
            turns_.append((Action.LOWKICK, Action.LOWBLOCK, agent_.health, i))
        elif action == Action.LOWBLOCK:
            agent_.health -= 1
            turns_.append((Action.LOWBLOCK, Action.HIGHKICK, agent_.health, i))
        if agent_.health <= 0:
            break


async def fight():
    turns = []
    agent = Agent()
    await fight_agent(agent, turns, 0)
    for agent_a, neo_a, agent_hp, agent_i in turns:
        print(f"Agent: {agent_a}, Neo: {neo_a}, Agent Health: {agent_hp}")
    print('Neo wins!')


async def fightmany(n):
    turns = []
    agents = [Agent() for _ in range(n)]

    async with asyncio.TaskGroup() as tg:
        for i, agent in enumerate(agents, start=1):
            tg.create_task(fight_agent(agent, turns, i))

    for agent_a, neo_a, agent_hp, agent_i in turns:
        print(f"Agent {agent_i}: {agent_a}, Neo: {neo_a}, Agent Health: {agent_hp}")
    print('Neo wins!')


def main():
    asyncio.run(fightmany(5))


if __name__ == '__main__':
    main()
