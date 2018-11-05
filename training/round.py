from player import Player

class Round:
    def __init__(self, dora):
        self.dora = [int(dora)]
        self.player = []

    def init_player(self, hand, wind):
        self.player.append(Player(hand, wind))   

    def add_dora(self, new_dora):
        self.dora.append(int(new_dora))