import sys
import random
import argparse
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import textworld_express as twx
from textworld_express import TextWorldExpressEnv

# Import ask_openai from the parent directory
from pddl_query import *


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
    # return coinMove(obs, infos)
    # update_pf(obs, infos)
    return get_next_moves(obs, infos)
    # return "move east"

def runGame(id):
    """ Example user input console, to play through a game. """
    history = None
    if prompt_toolkit_available:
        history = InMemoryHistory()

    exitCommands = ["quit", "exit"]
    
    args = parse_args()
    env = TextWorldExpressEnv(envStepLimit=5)

    gameName = "coin"  # Game name is "coin"
    gameFold = "train"
    #gameSeed = args['seed']  # Seed to ensure reproducibility
    gameParams = "numLocations=5, includeDoors=1"# Parameters for the game (e.g. numLocations=5, includeDoors=1)
    generateGoldPath = True

    # Load the game environment with the given parameters
    env.load(gameName, gameParams)
    obs, infos = env.reset(seed=id, gameFold=gameFold, generateGoldPath=generateGoldPath)


    if (generateGoldPath == True):
        print("Gold path: " + str(env.getGoldActionSequence()))
        

    initialize_pf(obs, infos)
    
    obs, reward, done, infos = env.step("look around")
 
    # Take action
    curIter = 0
    numTrials = 15
    currMoves = []
    
    
    # only go up to numTrials times
    while (curIter < numTrials):
        userInputStr = ""
        print("\nType 'exit' to quit.\n")
        count = 0

        if (infos['tasksuccess'] == True):
            print("Task Success!")
        if (infos['taskfailure'] == True):
            print("Task Failure!")
            
        # print("currobs", obs)

        # query LLM
        if not currMoves:
            # need to get new action plan
            # validActions = infos['validActions']
            print("no more moves, need to get some from llm")
            currMoves = queryLLM(obs, infos)
            if (currMoves == "invalid" or not currMoves):
                print("invalid ansewr from solver")
                return False
            
        userInputStr = currMoves.pop(0)
        print("next move from inside the loop", userInputStr)

        # Take action
        obs, reward, done, infos = env.step(userInputStr)
        
        print("reward and done", reward, done)
        print("curr environment", obs)

        if (done):
            print("COIN FOUND! CONGRATS!")
            return True
        
        update_pf(obs, infos, userInputStr)

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
    # args = parse_args()
    # random.seed(args["seed"])
    return runGame()

def main(id):
    print("TextWorldExpress 1.0 API Examples - Using Chat GPT")

    # # Parse command line arguments
    # args = parse_args()
    # random.seed(args["seed"])
    runGame(id)

if __name__ == "__main__":
    main()
