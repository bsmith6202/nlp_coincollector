import sys
import random
import argparse
import os
import asyncio

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import textworld_express as twx
from textworld_express import TextWorldExpressEnv

# Import ask_openai from the parent directory
from asking_kani import *


prompt_toolkit_available = False
try:
    # For command line history and autocompletion.
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import InMemoryHistory
    prompt_toolkit_available = sys.stdout.isatty()
except ImportError:
    pass

try:
    # For command line history when prompt_toolkit is not available.
    import readline  # noqa: F401
except ImportError:
    pass


async def queryLLM(obs, infos):
    print("getting move")
    return await get_move(obs, infos)
    # return "move east"

async def runGame(args):
    """ Example user input console, to play through a game. """
    history = None
    if prompt_toolkit_available:
        history = InMemoryHistory()

    exitCommands = ["quit", "exit"]

    gameName = "coin"

    # Initialize environment
    env = TextWorldExpressEnv(args['jar_path'], envStepLimit=30)
    gameNames = env.getGameNames()
    print("Supported Game Names: " + str(gameNames))

    # Load the task
    gameFold = "train"
    gameSeed = random.randint(1, 10000) 
    gameParams = "numLocations=5, includeDoors=1" # e.g. "numLocations=5, includeDoors=1"
    generateGoldPath = True
    env.load(gameName, gameParams)

    print("Selected Game: " + str(gameName))
    print("Selected Seed: " + str(gameSeed))
    print("Generation properties: " + str(env.getGenerationProperties()) )

    # Task description
    print("Task Description: " + env.getTaskDescription())
    print("")

    # Initialize a random `gameName` game.
    obs, infos = env.reset(seed=gameSeed, gameFold=gameFold, generateGoldPath=generateGoldPath)

    if (generateGoldPath == True):
        print("Gold path: " + str(env.getGoldActionSequence()))
        
    createJSON()

    # Take action
    curIter = 0
    numTrials = 30
    # only go up to numTrials times
    while (curIter < numTrials):
        userInputStr = ""
        print("\nType 'exit' to quit.\n")
        count = 0

        if (infos['tasksuccess'] == True):
            print("Task Success!")
        if (infos['taskfailure'] == True):
            print("Task Failure!")

        # query LLM
        userInputStr = await queryLLM(obs, infos)
        print("answer returned", userInputStr)
        # Take action
        obs, reward, done, infos = env.step(userInputStr)
        print("curr reward", reward)
        print("curr done", done)
        if (done):
            print("COIN FOUND! CONGRATS!")
            return True

        curIter += 1

    print("ran out of time womp womp")
    return False

#
#   Parse command line arguments
#
def parse_args():
    desc = "Run a model that chooses random actions until successfully reaching the goal."
    parser = argparse.ArgumentParser(desc)
    parser.add_argument("--jar_path", type=str,
                        help="Path to the TextWorldExpress jar file. Default: use builtin.")
    parser.add_argument("--game-name", type=str, choices=twx.GAME_NAMES, default='coin',
                        help="Specify the game to play. Default: %(default)s")
    parser.add_argument("--game-params", type=str, default='',
                        help="Change game generation properties, e.g. 'numLocations=5, includeDoors=1'.")
    parser.add_argument("--game-fold", type=str, choices=['train', 'dev', 'test'], default='train',
                        help="Specify the game set to use (train, dev, test). Default: %(default)s")
    parser.add_argument("--max-steps", type=int, default=50,
                        help="Maximum number of steps per episode. Default: %(default)s")
    parser.add_argument("--seed", type=int, default=0,
                        help="Seed the generator for used in generating the game")

    args = parser.parse_args()
    params = vars(args)
    return params

def run():
    print("TextWorldExpress 1.0 API Examples - Using Chat GPT")

    # Parse command line arguments
    args = parse_args()
    random.seed(args["seed"])
    return runGame(args)

def main():
    print("TextWorldExpress 1.0 API Examples - Using Chat GPT")

    # Parse command line arguments
    args = parse_args()
    random.seed()
    return asyncio.run(runGame(args))

if __name__ == "__main__":
    main()
