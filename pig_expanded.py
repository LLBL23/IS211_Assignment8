import random
import argparse
import time


class Die:
    def __init__(self, seed=None):
        random.seed(seed)

    def random_roll(self):
        """
        Generate a random number 1-6.

        :return: Generated random number
        """
        return random.randint(1,6)


class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.round_score = 0

    def player_turn(self, die):
        self.round_score = 0
        while True:
            turn = input('Would you like to roll (r) or hold (h)? ')
            if turn == 'r':
                value = die.random_roll()
                if value == 1:
                    self.round_score = 0
                    print(f'You rolled a 1. Your turn is over.')
                    print(f'Your current total is: {self.total_score}')
                    break
                else:
                    self.round_score += value
                    print(f'You rolled a {value}')
                    print(f'Your turn total is: {self.round_score}')
                    print(f'Your possible total score is: {self.total_score + self.round_score}')
            elif turn == 'h':
                self.total_score += self.round_score
                break
            else:
                print("Wrong input. Please enter 'r' or 'h'")


class ComputerPlayer(Player):
    #def __init__(self, name):
        #super().__init__(self, name)  # automatically inherit Player class methods and properties

    def player_turn(self, die):
        """Implement the strategy for the computer player"""
        score_min = 100 - self.total_score
        # play as a computer
        while True:
            value = die.random_roll()
            print(value)
            if value == 1:
                self.round_score = 0
                print(f'You rolled a 1. Your turn is over.')
                print(f'Your current total is: {self.total_score}')
                break
            else:
                self.round_score += value
                print(f'You rolled a {value}')
                print(f'Your turn total is: {self.round_score}')
                print(f'Your possible total score is: {self.total_score + self.round_score}')
            if score_min < 25 < self.round_score:
                self.total_score += self.round_score
                break







def make_player(name, type):
    """
    Player Factory function to create the correct Player class

    :param name: Player's name
    :param type: Player's type
    :return: A new player instance
    """
    if type == 'human':
        return Player(name)
    if type == 'computer':
        return ComputerPlayer(name)






class Game:
    """
    Tracks the players, their scores and the die.
    """
    def __init__(self, players):
        self.players = players
        self.max_score = 100
        self.current_score = 0
        self.winner = None

    def check_for_winners(self):
        """Returns True if there is a winner"""
        for player in self.players:
            if player.total_score >= self.max_score:
                self.winner = player
                return True
        return False

    def play(self):
        die = Die()
        idx_player = 0
        while not self.check_for_winners():
            current_player = self.players[idx_player]
            print(f"It's {current_player.name}'s turn. It's current total is {current_player.total_score}...")
            current_player.player_turn(die)
            print(f"{current_player.name}'s turn is over. It's total is {current_player.total_score}")

            idx_player += 1
            if idx_player == len(self.players):
                idx_player = 0

        print('There is a winner')
        print(f'{self.winner.name} won with {self.winner.total_score} points')

class TimedGameProxy:
    """
    Tracks the players, their scores and the die. Only allows one minute for entire game.
    """
    def __init__(self, players):
        self.players = players
        self.max_score = 100
        self.current_score = 0
        self.winner = None
        self.time_limit = 60

    def check_for_winners(self):
        """Returns True if there is a winner"""
        for player in self.players:
            if player.total_score >= self.max_score:
                self.winner = player
                return True
        return False

    def time_check(self):
        """Returns True if game time equals  60 seconds"""
        start_time = time.time()
        elapsed_time = time.time() - start_time
        if elapsed_time > self.time_limit:
            print('Time is up. Game over.')
            return True
        else:
            return False

    def play_timed(self):
        die = Die()
        idx_player = 0
        while not self.check_for_winners() and not self.time_check():
            current_player = self.players[idx_player]
            print(f"It's {current_player.name}'s turn. It's current total is {current_player.total_score}...")
            current_player.player_turn(die)
            print(f"{current_player.name}'s turn is over. It's total is {current_player.total_score}")

            idx_player += 1
            if idx_player == len(self.players):
                idx_player = 0

        print('There is a winner')
        print(f'{self.winner.name} won with {self.winner.total_score} points')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="kind of players: human/computer", type=str, required=True)
    parser.add_argument("--player2", help="kind of players: human/computer", type=str, required=True)
    parser.add_argument("--timed", help="timed version of game: timed", type=str, required=False)
    args = parser.parse_args()
    print(args.player1)
    print(args.player2)

    player1 = make_player("One", args.player1)
    player2 = make_player("Two", args.player2)
    timed_game = args.timed
    if timed_game:
        game = TimedGameProxy([player1, player2])
        game.play_timed()
    else:
        game = Game([player1, player2])
        game.play()
