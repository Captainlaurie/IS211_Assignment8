import random
import argparse
import time

WinningScore = 100

class Dice:
    
    def __init__(self):
        self.sides = 6
    
    #Roll function to get a random int between 1 and the number of sides(6)
    def roll(self):
        return random.randint(1, self.sides)

class PlayerFactory:
    
    @staticmethod
    def create_player(name, player_type):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Invalid player type: {player_type}")

class Player:
    
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.turn_score = 0
        self.dice = Dice()
        #self.player
        
    def get_total(self):
        return self.total_score

    def get_name(self):
        return self.name

    def show_score(self):
        print(f"{self.name} has {self.total_score} points")
    
    def player_turn(self):
        #reset turn score
        self.turn_score = 0
        while True:
            choice = input("Press r to roll, h to hold and bank your score: ")
            if choice.lower() == "r":
                roll = self.dice.roll()
                if roll == 1:
                    print(f"{self.name} rolled a 1! Your score is 0 this turn.")
                    self.turn_score = 0
                    break
                else:
                    self.turn_score += roll
                    print(f"{self.name} rolled a {roll}. Current turn score {self.turn_score}")
            elif choice.lower() == "h":
                self.total_score += self.turn_score
                break
            else:
                print("Invalid input. Please enter 'r' or 'h'.")

class ComputerPlayer(Player):

    def computer_turn(self):
        # Roll the dice
        while True:
            roll = self.dice.roll()

            if roll == 1:
                # Player scores nothing for the turn and turn ends
                self.turn_score = 0
                print(f"Computer {self.name} rolled a 1! 0 points. Turn over.")
                return

            else:
                # Add the roll to the turn score
                self.turn_score += roll
                print(f"Computer {self.name} rolled a {roll}. Roll again. Turn score: {self.turn_score}.")

                # Check if the turn score meets the hold threshold
                if self.turn_score >= min(25, 100 - self.total_score):
                    # Add turn score to overall score and end turn
                    self.total_score += self.turn_score

                    #reset turn score
                    self.turn_score = 0
                    print(f"Computer {self.name} holds and banks {self.turn_score} points.")
                    return

class Game:
    
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = player1
        self.winner = None
        self.turn_score = 0 

    def check_winner(self):
        for player in self.players:
            if player.get_total() >= WinningScore:
                self.winner = player
                return True

    def play(self):
        player_idx = 0
        current_player = self.players[player_idx]
        # Play until there is a winner
        while not self.check_winner():
            print(f"It's {current_player.get_name()}'s turn...")
            if isinstance(current_player, ComputerPlayer):
                current_player.computer_turn()
            else:
                current_player.player_turn()
            
            current_player.show_score()

            if player_idx == 0:
                player_idx = 1
            else:
                player_idx = 0
            current_player = self.players[player_idx]
            print("\n" + "=" * 40)

        print(f"{self.winner.get_name()} wins!")
        self.winner.show_score()
        
class TimedGameProxy(Game):
    def __init__(self, player1, player2, time_limit=60):
        super().__init__(player1, player2)
        self.player_idx = 0
        self.time_limit = time_limit
        self.start_time = None
        self.current_time = None

    def check_time(self):
        self.current_time = time.time()
        if self.start_time is not None and self.current_time - self.start_time >= self.time_limit:
            print("Time's up!")
            return True
        return False
    
    def check_winner(self):
        for player in self.players:
            if player.get_total() >= WinningScore:
                self.winner = player
                return True

    def timed_play(self):
        self.start_time = time.time()
        while not self.check_time() and not self.check_winner():
            print(f"It's {self.current_player.get_name()}'s turn...")
            if isinstance(self.current_player, ComputerPlayer):
                self.current_player.computer_turn()
            else:
                self.current_player.player_turn()

            self.current_player.show_score()

            if self.player_idx == 0:
                self.player_idx = 1
            else:
                self.player_idx = 0
            self.current_player = self.players[self.player_idx]
            print("\n" + "=" * 40)

        if self.check_time():
            print("Time's up!")
            if self.players[0].get_total() > self.players[1].get_total():
                print(f"{self.players[0].get_name()} wins!")
                
            elif self.players[1].get_total() > self.players[0].get_total():
                    print(f"{self.players[1].get_name()} wins!")
            else:
                print("It's a tie!")
            
        else:
            print(f"{self.winner.get_name()} wins!")
            self.winner.show_score()

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