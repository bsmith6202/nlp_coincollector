import random
from TextWorldExpress.examples import entirely_chat


# using batching
def main():
    games= []
    win_count = 0
    
    total_steps = 50
    num_steps = 0
    max_steps = 10
    
    # create batch array
    for i in range(50):
        env, obs, infos = entirely_chat.initialize_environment(i)
        games.append({
            "id": i + 1,
            "game": env,
            "infos": infos,
            "obs": obs,
            "done": False,
            "steps": 0
        })
        
        while len(games) > 0:
            games_over = [] 
            for game in games:
                print("ON RUN ", i)
                print(f"Running game {game['id']}...")
                if game["done"]:
                    continue
                
                if game["steps"] >= max_steps:
                    print(f"Game {game['id']} reached the step limit of {max_steps}. Ending game.")
                    games_over.append(game)
                    continue  # Skip the game if it reached the step limit
                    
                curr_inst = entirely_chat.runGameStep(game)
                game["steps"] += 1 
                print("adding a num step. now on game step", game["steps"])
                # {"game_state": game_state, "done": False, "win": False}
                if (curr_inst["done"]):
                    print(f"Game {game['id']} finished")
                    if curr_inst["win"]:
                        win_count += 1
                    games_over.append(game)
                    
            for game in games_over:
                print("game over is", game['id'], "with info and obs", game['infos'], game['obs'])
                games.remove(game)
            

                
    print("This version of Coin Collector won", win_count, "out of 100 times")

if __name__ == "__main__":
    main()