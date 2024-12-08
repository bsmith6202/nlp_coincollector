import sys
import random
import argparse
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import textworld_express as twx
from textworld_express import TextWorldExpressEnv

# Import ask_openai from the parent directory
from ask_openai import *


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


def queryLLM(obs, infos):
    return coinMove(obs, infos)

    # return "move east"

def runGame(args):
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
    gameSeed = args['seed']
    gameParams = args['game_params']  # e.g. "numLocations=5, includeDoors=1"
    generateGoldPath = True
    env.load(gameName, gameParams)

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
    numTrials = 25
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
        userInputStr = queryLLM(obs, infos)

        # Take action
        obs, reward, done, infos = env.step(userInputStr)
        # print("curr reward", reward)
        # print("curr done", done)
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
    parser.add_argument("--max-steps", type=int, default=25,
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

def initialize_environment(id):
    args = parse_args()
    random.seed(args["seed"])
    env = TextWorldExpressEnv(envStepLimit=50)

    gameName = "coin"  # Game name is "coin"
    gameFold = "train"
    #gameSeed = args['seed']  # Seed to ensure reproducibility
    gameParams = "numLocations=5, includeDoors=1"# Parameters for the game (e.g. numLocations=5, includeDoors=1)
    generateGoldPath = True

    # Load the game environment with the given parameters
    env.load(gameName, gameParams)
    obs, infos = env.reset(seed=id, gameFold=gameFold, generateGoldPath=generateGoldPath)

    return env, obs, infos

def runGameStep(game_state):
    
    # This function runs one step of the game
    print("THIS IS GAME STAGE OBS", game_state["obs"])
    userInputStr = queryLLM(game_state["obs"], game_state["infos"])
    print("step picked", userInputStr)

    obs, reward, done, infos = game_state["game"].step(userInputStr)
    # Take action
    # game_state["obs"], reward, done, game_state["infos"] = game_state["env"].step(userInputStr)
    game_state["obs"] = obs
    game_state["infos"] = infos

    if done:
        if game_state["infos"]["tasksuccess"]:
            return {"game_state": game_state, "done": True, "win": True}
        elif game_state["infos"]["taskfailure"]:
            return {"game_state": game_state, "done": True, "win": False}
    
    return {"game_state": game_state, "done": False, "win": False}

def main():
    print("TextWorldExpress 1.0 API Examples - Using Chat GPT")

    # Parse command line arguments
    args = parse_args()
    random.seed(args["seed"])
    runGame(args)

if __name__ == "__main__":
    main()
