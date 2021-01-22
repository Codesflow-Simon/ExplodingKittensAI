import random
import itertools
import math
# import ai

random.seed(123)
class Card():
    def use(self):
        return False

    def if_drawn(self):
        return False

class Cat(Card):
    def __init__(self, name):
        self.playable = False
        self.name = name
        self.type = 'cat'

class KittenBomb(Card):
    def __init__(self):
        self.playable = None
        self.type = 'bomb'
    def if_drawn(self):
        return True

class Defuse(Card):
    def __init__(self):
        self.playable = False
        self.type = 'defuse'

class Attack(Card):
    def __init__(self):
        self.playable = True
        self.type = 'attack'

class Skip(Card):
    def __init__(self):
        self.playable = True
        self.type = 'skip'

class Nope(Card):
    def __init__(self):
        self.playable = False
        self.type = 'nope'

class Shuffle(Card):
    def __init__(self):
        self.playable = True
        self.type = 'shuffle'

class Future(Card):
    def __init__(self):
        self.playable = True
        self.type = 'future'

class Favor(Card): 
    def __init__(self):
        self.playable = True
        self.type = 'favor'

class Player():
    def __init__(self):
        self.hand = set([])
        self.alive = True

    def place_bomb(self):
        return math.floor(random.random()*(len(deck)+1))

    def draw_card(self, card):
        print(f'player draws a {card.type}')
        if card.type == 'bomb':
            difuse = False
            index = None
            for check_card in self.hand:
                if check_card.type == 'defuse':
                    difuse = True
                    self.hand.remove(check_card)
                    break
            if difuse == True:
                index = self.place_bomb()
            else:
                self.alive = False 
            return index

        self.hand.add(card)
        return None

    def get_card(self, card):
        self.hand.add(card)
        return card

    def play_card(self):
        return self.play_card_random()

    def play_card_random(self):
        dist = [random.random() for _ in range(11)]
        while True:
            target = math.floor(random.random()*float(play_num))
            favoured = dist.index(max(dist))
            action = turn_number_inverse_mapping[favoured]
            if action == 'draw':
                return 'draw', None, None
            elif action [:2]!='2x':
                for card in self.hand:
                    if card.type == action:
                        return action, card, target
    
                dist[favoured] = -1
            else:
                cards=[]
                for card in self.hand:
                    if card.type == action[2:]:
                        cards.append(card)
                        if len(cards) == 2:
                            return action, cards, None
                dist[favoured] = -1

    def check_nope(self):
        has_nope = False
        for card in self.hand:
            if card.type == 'nope':
                has_nope = True
                break
        if has_nope == False:
            return None
        result = card if random.random() < 0.1 else None
        return result

    def give_favor(self):
        return random.sample(self.hand, 1)[0]

turn_number_mapping = {
    'draw':0,
    'attack':1,
    'skip':2,
    'shuffle':3,
    'future':4,
    'favor':5,
    '2xtaco_cat':6,
    '2xrainbow_cat':7,
    '2xbeard_cat':8,
    '2xcatermelon':9,
    '2xpotato_cat':10
}
turn_number_inverse_mapping = {v: k for k, v in turn_number_mapping.items()}

def construct_deck(play_num):
    deck = []

    for _ in range(4):
        deck.append(Cat('taco_cat'))
        deck.append(Cat('rainbow_cat'))
        deck.append(Cat('beard_cat'))
        deck.append(Cat('catermelon'))
        deck.append(Cat('potato_cat'))
        deck.append(Attack())
        deck.append(Shuffle())
        deck.append(Favor())
        deck.append(Skip())
    for _ in range(5):
        deck.append(Nope())
        deck.append(Future())

    random.shuffle(deck)

    for player in players:
        player.get_card(Defuse())
        for _ in range(7):
            card = deck.pop()
            player.draw_card(card)

    for _ in range(2):
        deck.append(Defuse())
    for _ in range(play_num-1):
        deck.append(KittenBomb())

    random.shuffle(deck)
    return deck

def play():
    def nope_phase(current_player):
        for num, player in enumerate(players):
            if player == current_player:
                continue
            nope = player.check_nope()
            if nope:
                assert nope.type == 'nope'
                player.hand.remove(nope)
                print(f'player {num} nopes player {players.index(current_player)}')
                if not nope_phase(player):
                    return True
                else: break
        return False

    def turn(current_player):
        while True:
            result, cards, target = current_player.play_card()

            print(f'player {current_player_idx} plays a {result}')
            if result == 'draw':
                return result, None

            if type(cards)==list:
                for card in cards:
                    current_player.hand.remove(card)
            else:
                current_player.hand.remove(cards)

            if not nope_phase(current_player):
                return result, target
    current_player_idx = 0
    crashed = False
    attack = False
    print('\n')
    while not crashed:
        current_player = players[current_player_idx]
        if not current_player.alive:
            current_player_idx = (current_player_idx+1)%(play_num)
            continue
        result, target = turn(current_player)

        if result == 'draw':
            card = deck.pop()
            index = current_player.draw_card(card)
            if index:
                deck.insert(index, card)
            if attack:
                attack = False
            else:
                current_player_idx = (current_player_idx+1)%(play_num)

        elif result == 'attack':
            attack = True
            current_player_idx = (current_player_idx+1)%(play_num)

        elif result =='skip':
            if attack:
                attack = False
            else:
                current_player_idx = (current_player_idx+1)%(play_num)

        elif result == 'shuffle':
            random.shuffle(deck)

        elif result == 'future':
            cards = deck[-3:]

        elif result == 'favor':
            card = players[target].give_favor()
            print(f'player {current_player_idx} takes a {card.type} from {target}')
            players[target].hand.remove(card)
            current_player.hand.add(card)

        elif result[:2] == '2x':
            card_idx = math.floor(random.random()*len(players[target].hand))
            card = players[target].hand[card_idx]
            print(f'player {current_player_idx} takes a {card.type} from {target}')
            players[target].hand.remove(card)
            current_player.hand.add(card)

        players_in = 0
        winner = None
        for num, player in enumerate(players):
            if player.alive:
                winner = num
                players_in += 1
        if players_in == 1: 
            print(f'Player {winner} wins!!')
            return

play_num = 5
players = tuple([Player() for _ in range(play_num)])
deck = construct_deck(play_num)

play()

    