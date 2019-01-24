import random
import time
import user_agent


def delay():
    timeDelay = random.random()
    time.sleep(timeDelay)


def set_user_agent() :
    user_agent.user_agent = random.choice(user_agent.user_agent_list)
    header = {'User-Agent': user_agent.user_agent}
    return header
