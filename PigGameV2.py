import random
import argparse
import time


class Dice:
    
    def __init__(self):
        self.sides = 6
    
    #Roll function to get a random int between 1 and the number of sides(6)
    def roll(self):
        return random.randint(1, self.sides)

class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0
        self.dice = Dice()


class ComputerPlayer(Player):

    def computer_turn(self):
        threshold = min(25, 100 - self.score)
        while self.turn_score < threshold:
            roll = self.dice.roll()
            if roll == 1:
                self.turn_score = 0
                print(f"{self.name} rolled a 1 and lost their turn.")
                return 0
            else:
                self.turn_score += roll
                print(f"{self.name} rolled a {roll}. Turn score {self.current_player.turn_score}")
        print(f"{self.name} Holds and banks points.")
        return self.turn_score

class PlayerFactory:
    
    @staticmethod
    def create_player(name, player_type):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Invalid player type: {player_type}")

class Game:
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.turn_score = 0
        
        # Function to advance to next player and initialize current score for the turn as 0
    def next_player(self):
        self.current_player, self.other_player = self.other_player, self.current_player
        self.turn_score = 0

    def play(self):
        while True:
            print("\n" + "=" * 20)
            print(f"\nIt's {self.current_player.name}'s turn.")
            self.current_player.turn_score = 0
            while self.current_player.score < 100:
                print("\n" + "=" * 20)
                if isinstance(self.current_player, ComputerPlayer):
                    choice = "r"
                else:
                    choice = input("Press r to roll, h to hold and bank your score: ")
                if choice.lower() == "r":
                    roll = self.current_player.dice.roll()
                    if roll == 1:
                        print(f"{self.current_player.name} rolled a 1. Your score is 0 this turn.")
                        self.current_player.turn_score = 0
                        break
                    else:
                        self.current_player.turn_score += roll
                        print(f"{self.current_player.name} rolled a {roll}.")
                elif choice.lower() == "h":
                    break
                else:
                    print("Invalid input. Please enter 'r' or 'h'.")
            self.current_player.score += self.current_player.turn_score
            print(f"{self.current_player.name}'s score is {self.current_player.score}.")
            if self.current_player.score >= 100:
                print(f"{self.current_player.name} wins!")
                return
            self.next_player()


class TimedGameProxy:
    
    def __init__(self, player1, player2):
        self.game = Game(player1, player2)
        self.start_time = 0

    def timed_play(self):
        print("Running a timed game")
        self.start_time = time.time()
        while True:
            if time.time() - self.start_time > 60:
                if self.game.player1.score > self.game.player2.score:
                    print(f"Time's up! {self.game.player1.name} wins with a score of {self.game.player1.score}!")
                elif self.game.player1.score < self.game.player2.score:
                    print(f"Time's up! {self.game.player2.name} wins with a score of {self.game.player2.score}!")
                else:
                    print("It's a tie!")
                    return
            if self.game.player1.score >= 100 or self.game.player2.score >= 100:
                return
            self.game.play()
            
# TODO: Timed game broke, need to fix this

def main():
    parser = argparse.ArgumentParser(description="Play a game of Pig.")
    parser.add_argument("--player1", type=str, choices=["human", "computer"], help="Type of player 1", default = "human")
    parser.add_argument("--player2", type=str, choices=["human", "computer"], help="Type of player 2", default = "computer")
    parser.add_argument("--timed", action="store_true", help="Play a timed game")

    args = parser.parse_args()

    player1 = PlayerFactory.create_player("Player 1", args.player1)
    player2 = PlayerFactory.create_player("Player 2", args.player2)

    if args.timed:
        game = TimedGameProxy(player1, player2)
        game.timed_play()
    else:
        game = Game(player1, player2)

    game.play()

if __name__ == "__main__":
    main()