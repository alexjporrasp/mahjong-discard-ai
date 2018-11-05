class Player:
    def __init__(self, initial_hand, wind):
        self.closed_hand = list(map(int, initial_hand))
        self.closed_hand.sort()

        self.discards = []
        self.melds = []
        self.declared_riichi = 0
        self.wind = wind # 0 : East; 1: South, 2: West, 3: North

    def draw_tile(self, tile):
        self.closed_hand.append(int(tile))
        self.closed_hand.sort()
        
    def discard_tile(self, tile):
        self.closed_hand.remove(int(tile))
        self.discards.append(int(tile))
        
    
    def meld(self, meld_list):
        self.melds.append(list(map(int, meld_list)))
        self.melds = list(filter(lambda x: not(set(x) < set(meld_list)), self.melds)) # Ankan
        self.closed_hand = list(set(self.closed_hand) - set(meld_list))

        if(len(self.melds) > 4):  
            print(self.closed_hand, self.melds, meld_list)

    def declare_riichi(self):
        self.declared_riichi = 1