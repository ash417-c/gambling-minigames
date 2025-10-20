import random as ran
_CARD_VALUES = {
    'SA':11, 'S2':2, 'S3':3, 'S4':4, 'S5':5, 'S6':6, 'S7':7, 'S8':8, 'S9':9, 'S10':10, 'SJ':10, 'SQ':10, 'SK':10,
    'HA':11, 'H2':2, 'H3':3, 'H4':4, 'H5':5, 'H6':6, 'H7':7, 'H8':8, 'H9':9, 'H10':10, 'HJ':10, 'HQ':10, 'HK':10,
    'DA':11, 'D2':2, 'D3':3, 'D4':4, 'D5':5, 'D6':6, 'D7':7, 'D8':8, 'D9':9, 'D10':10, 'DJ':10, 'DQ':10, 'DK':10,
    'CA':11, 'C2':2, 'C3':3, 'C4':4, 'C5':5, 'C6':6, 'C7':7, 'C8':8, 'C9':9, 'C10':10, 'CJ':10, 'CQ':10, 'CK':10
}
_CARD_NAMES = {
    'SA':'Ace of Spades',   'S2':'Two of Spades',   'S3':'Three of Spades',   'S4':'Four of Spades',   'S5':'Five of Spades',  'S6':'Six of Spades',   'S7':'Seven of Spades',   'S8':'Eight of Spades',    'S9':'Nine of Spades',   'S10':'Ten of Spades',   'SJ':'Jack of Spades',   'SQ':'Queen of Spades',   'SK':'King of Spades',
    'HA':'Ace of Hearts',   'H2':'Two of Hearts',   'H3':'Three of Hearts',   'H4':'Four of Hearts',   'H5':'Five of Hearts',  'H6':'Six of Hearts',   'H7':'Seven of Hearts',   'H8':'Eight of Hearts',    'H9':'Nine of Hearts',   'H10':'Ten of Hearts',   'HJ':'Jack of Hearts',   'HQ':'Queen of Hearts',   'HK':'King of Hearts',
    'DA':'Ace of Diamonds', 'D2':'Two of Diamonds', 'D3':'Three of Diamonds', 'D4':'Four of Diamonds', 'D5':'Five of Diamonds','D6':'Six of Diamonds', 'D7':'Seven of Diamonds', 'D8':'Eight of Diamonds',  'D9':'Nine of Diamonds', 'D10':'Ten of Diamonds', 'DJ':'Jack of Diamonds', 'DQ':'Queen of Diamonds', 'DK':'King of Diamonds',
    'CA':'Ace of Clubs',    'C2':'Two of Clubs',    'C3':'Three of Clubs',    'C4':'Four of Clubs',    'C5':'Five of Clubs',   'C6':'Six of Clubs',    'C7':'Seven of Clubs',    'C8':'Eight of Clubs',     'C9':'Nine of Clubs',    'C10':'Ten of Clubs',    'CJ':'Jack of Clubs',    'CQ':'Queen of Clubs',    'CK':'King of Clubs',
    'Hidden Card':'Hidden Card',    'HC':'Hidden Card', 'JK': 'Joker'
}
_CARDS = [
    'SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK',
    'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
    'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK',
    'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK'
]

class testcase:
    def __init__(self, starting_list):
        self.starting_list = starting_list
    def draw(self):
        return self.starting_list.pop()
    
ACE_TESTCASE = testcase(['HA', 'H2', 'H3']*10)

class Hand:
    def __init__(self, name):
        self.name = name
        self.held_cards = []
        self.total = 0
        self.aces = 0
        self.split_possible = False

    def clear(self):
        self.held_cards = []
        self.total = 0
        self.aces = 0
        self.split_possible = False

    def get_card(self, index):
        return self._convert_to_img_type(self.held_cards[index])

    def _convert_to_img_type(self, card_inate):
        return card_inate[1:] + '-' + card_inate[0] if not card_inate[0] == 'S' else card_inate[1:] + '-P'

    def cards(self, hide_first=False):
        start = 0
        if hide_first:
            start+=1
            yield 'BACK'
        for card in self.held_cards[start:]:
            yield self._convert_to_img_type(card)

    def set_name(self, name_new):
        self.name = name_new

    def split_hand(self):
        if self.name[-1].isnumeric():
            sec_name = self.name[:-1] + str(int(self.name[-1])+1)
        else:
            sec_name=self.name+'2'
        second_hand = Hand(sec_name)
        second_hand.add(self.held_cards.pop())
        self._reset_internals()
        return second_hand

    def add(self, card):
        self.held_cards.append(card)
        self.total += _CARD_VALUES[card]
        if card[1] == 'A':
            self.aces += 1
        self.split_possible =  len(self.held_cards) == 2 and self.held_cards[0] == self.held_cards[1]
        if self.total > 21:
            self.ace_retry()

    def _reset_internals(self):
        self.total = 0
        self.aces = 0
        for card in self.held_cards:
            self.total += _CARD_VALUES[card]
            if card[1] == 'A':
                self.aces +=1
    
    def reveal(self, Hide_first=False):
        print('\n'+self.name)
        for card, i in zip(self.held_cards, range(len(self.held_cards))):
            if Hide_first and i == 0:
                card = "HC"
            print(f"{i+1}) {_CARD_NAMES[card]}")
        out = 'No Total' if Hide_first else f'Total: {self.total}'
        print(out)
    
    def value(self):
        return self.total
    
    def split(self):
        return self.split_possible
    
    def ace_retry(self):
        if self.aces > 0:
            self.total-=10
            self.aces-=1
    
    def __len__(self):
        return len(self.held_cards)
    

class Deck:
    def __init__(self, number_of_decks:int=1):
        self.shoe = number_of_decks
        self.cards = []
        self.initiate_deck(self.shoe)
        
    def initiate_deck(self, num):
        self.cards = _CARDS*num
        self.shuffle()

    def draw(self):
        if self.cards:
            return self.cards.pop()
        self.initiate_deck(self.shoe)
        return self.cards.pop()
    
    def shuffle(self):
        ran.shuffle(self.cards)

class BlackJack:
    def __init__(self, forceStand:bool=False):
        self.dealers_hand = Hand("Dealer's Hand")
        self.players_hand = Hand("Player's Hand")
        self.deck = Deck()
        self.player_bust = False
        self.player_io_end = False
        self.won = False
        self.result = 'not over'

        self.initial_deal()
        if forceStand:
            self.stand()

    def get_dealers_hidden(self):
        return self.dealers_hand.get_card(0)

    def get_result(self):
        return self.result
    
    def reset(self):
        self.players_hand.clear()
        self.dealers_hand.clear()
        self.player_bust = False
        self.player_io_end = False
        self.won = False
        self.result = 'not over'

        self.initial_deal()

    def get_players_hand(self):
        return self.players_hand
    
    def get_dealers_hand(self):
        return self.dealers_hand

    def game_end(self):
        self.dealer_turn()
        self.final_display()

    def initial_deal(self):
        #initial deal
        for i in range(2):
            self.dealers_hand.add(self.deck.draw())
            self.players_hand.add(self.deck.draw())
        self.dealers_hand.reveal(Hide_first=True)
        self.players_hand.reveal()
        if self.dealers_hand.value() == 21: #push
            print('Dealer 21: stand')
            #raise RuntimeError('Dealer 21: stand')
        if self.players_hand.value() == 21: #stand
            self.won = True
            self.stand()

    def hit(self):#check if can hit
        if not self.player_bust and not self.player_io_end:
            self._hit()

    def _hit(self):
        self.players_hand.add(self.deck.draw())
        if self.players_hand.value() == 21:
            self.stand()

        if self.players_hand.value() >21: #bust condition
            self.player_bust, self.player_io_end = True, True
        self.players_hand.reveal()

    def bust(self):
        return self.player_bust

    def player_turn_over(self):
        return self.player_io_end or self.player_bust

    def stand(self):
        self.player_io_end = True
    
    def dealer_turn(self):
        #dealer turn
        while(self.dealers_hand.value() < 17 and not self.player_bust and not self.won):
            self.dealers_hand.add(self.deck.draw())
            self.dealers_hand.reveal()
    
    def final_display(self):
        #final display to console
        p_val = self.players_hand.value()
        d_val = self.dealers_hand.value()
        out = f'Player bust at {p_val}' if self.player_bust else f"Dealer's {d_val} vs Player's {p_val}" 
        print('\n'+out)
        if self.player_bust:
            self.result = 'bust'
        elif p_val == d_val or (d_val == 21 and len(self.get_dealers_hand()) == 2):
            self.result = 'push'
        elif p_val > d_val or d_val > 21:
            self.result = 'win'
        else:
            self.result = 'lost'
