import random
from TextWorldExpress.examples import chat_kani

def main():
    win_count = 0

    for i in range(20):
        print(f"Running game {i + 1}...")
        sln = chat_kani.main()
        print("sln", sln)
        if (sln):
            win_count += 1
     
    print("This version of coin collector won", win_count, " out of 20 times")

if __name__ == "__main__":
    main()