# --- Poker.py ---
# User Instructions
#
# Royal Flush:    This hand is the rarest in poker. 
#                 It’s when you make a ten-to-ace straight all in the same suit such as A♦K♦Q♦J♦T♦
# Straight Flush: Five consecutive cards of differing suits, like 8♠7♠6♠5♠4♠,
#                 then you have a straight flush.
# 4-of-a-Kind:    The name says it all! If you have all four of the same card,
#                 like A♠4♠4♣4♥4♦ then you have quads!
# Full House:     Also known as a “boat,” it’s when you have three of a kind along with a pair - 
#                 for example: A♦A♣A♥J♥J♠ (three of one, two of the other)
# Flush:          There are four suits in poker (diamonds, hearts, spades, and clubs). 
#                 When you have five cards all in the same suit, you have a flush. An example might be A♥J♥8♥4♥2♥
# Straight:       Five consecutive cards of differing suits, like 8♥7♣6♦5♦4♠ is a straight.
#                 An A-2-3-4-5 straight is known as a “wheel,” while 10-J-Q-K-A is called “Broadway.”
# 3-of-a-Kind:    Whenever you have three of the same cards (i.e. A♠K♥5♠5♦5♣) you have three-of-a-kind. 
#                 If you make three-of-a-kind with a pair in the hole and one on the board, it’s “a set.”
#                 If you make it with two on the board and one card in the hole, then it’s called “trips.”
#Two Pair:        Is when you have not one, but two pairs. The fifth card is your kicker. For instance,
#                 if you have A♣K♥5♥K♠5♦ you have kings and fives with an ace kicker.
#One Pair:        There are thirteen different cards of each suit. Whenever you match two,
#                 it’s called a pair. For example,A♦A♣7♠4♠2♣2 is a pair of aces.
#High Card:       If no one can make a ranked hand (different suits, non-connected, unpaired) 
#                 it comes down to your high card(s). If you have A♣Q♦9♥6♣3♦ then you have ace-queen high.


from ntpath import join
from random import shuffle
from re import X
from sys import flags
from matplotlib.pyplot import cla
from itertools import combinations

colors = ['hearts', 'diamonds', 'spades', 'clubs']
symbols = {"clubs":"♣", "diamonds" :"♦", "hearts":"♥", "spades":'♠'}
numbers = {"2":"Deuce", "3":"Trey", "4":"Four","5":"Five","6":"Sixe","7":"Seven","8":"Eight","9":"Nine","10":"Ten","11":"Jack","12":"Queen","13":"King","14":"Ace"}

class Card:
    """Representation of cards"""
    def __init__(self, value, color):
        self._value = value
        self._color = color

    def get_data(self):
        return[self._value, self._color]
    
    def get_card(self):
        num = ""
        if self._value == 1:
            num = "A"
        elif self._value == 11:
            num = "J"
        elif self._value == 12:
            num = "Q"
        elif self._value == 13:
            num = "K"
        else:
            num =str(self._value)

        return num + symbols[self._color]

    def __str__(self):
        return[self._value, self._color]
 

class Deck:
    """Deck (list) of cards"""
    def __init__(self):
        self._deck = [Card(value, color) for value in range(1, 14) for color in colors]

    def deck_shuffling(self):
        """Shuffle the cards"""
        shuffle (self._deck)

    def pop_card(self):
        """Remove card from the top of deck
        :return card"""
        return self._deck.pop()

    def print_deck(self):
        print("Deck:", [card.get_card() for card in self._deck])


class Poker():
    """Poker Game"""
    def __init__(self,nHands) -> None:
        if nHands > 14 or nHands < 2:
            print("poker suitable to any number of players from 2 to 14")
            nHands = int(input("plese enter legal number: "))

        self._deck = Deck()
        self._deck.deck_shuffling ()
        self._hands = {}
        self._table = []
        self._tlist = [] 
        self._pot= {}
        nCards = 2

        for i in range(nHands):
            curent_hand = []
            for j in range(nCards):
                curent_hand.append(self._deck.pop_card())
            self._hands[str(i)] = {"hand":curent_hand, "balnce" : 1000, "gimble":0}
            print(i+1, "Hand:", [card.get_card() for card in curent_hand])

    def play(self):
        nTable = 5
        for i in range(nTable):
            self._table.append(self._deck.pop_card())
        print("On the table:", [card.get_card() for card in self._table])

        max = {"best_hand":[],"max_score":0}
        max_list = []

        for cunter, hand in enumerate(self._hands.keys()):
            x = self.best_cards_in_hand(self._hands[hand]["hand"]+self._table)
            self._tlist.append(x)

            if max["max_score"] < x["max_score"]:
                x["num"]= cunter+1
                max = x
                max_list = []

            elif max["max_score"] == x["max_score"]:
                flag = True
                for c in range(len(x["max_list_n"])):
                    if max["max_list_n"][c] < x["max_list_n"][c] and flag:
                        flag = False
                        x["num"]= cunter+1
                        max = x
                        max["max_str"] += ", " +  numbers[str(max["max_list_n"][c])]+ " Kicker"
                    elif max["max_list_n"][c] > x["max_list_n"][c] and flag:
                        flag = False  

                if flag:
                    x["num"]= cunter+1
                    curnt = x
                    max_list.append(curnt)

        if max_list == []:
    #       print("Player ", max["num"], "Wins!, hand:", [card.get_card() for card in max["best_hand"]], "scure:", max["max_str"])
            print("Player", max["num"], "Wins! |", max["max_str"])
        else:
            print("Split Pot - Player "+ str(max["num"])+", Player " + ", Player ".join([str(x["num"]) for x in max_list]) + " | " + max_list[0]["max_str"])
#            for _max in max_list:
  #              print("Best hand numnber", _max[num], ", hand:", [card.get_card() for card in _max["best_hand"]], "scure:", _max["max_str"])

    def best_cards_in_hand(self, hand8table):
        """Return the best hand for player
        :param hand8table
        :return [best_hand, max_score, max_list_n, max_str]"""
        list_h8t = (list(combinations(hand8table, 5)))
        best_hand = []
        flag = True
        max_score, max_list_n, max_str = self.win(list_h8t[0])
        for hand in list_h8t:
            flag = True
            data = self.win(hand)
            score, list_n, str = data
            if max_score == score:
                for c in range(len(list_n)):
                    if max_list_n[c] < list_n[c] and flag:
                        flag = False
                        max_list_n = list_n
                        max_str = str
                        best_hand = hand
                    elif max_list_n[c] > list_n[c] and flag:
                        flag = False       
            if max_score < score:
                max_score = score
                max_list_n = list_n
                max_str = str
                best_hand = hand
        return {"best_hand":best_hand,"max_score":max_score,"max_list_n":max_list_n,"max_str":max_str}

    def win(self, hand):
        return  self.straight_flush_and_royal_flush(hand)
    
    def is_flush(self, hand):
        for color in colors:
            if self.get_colors(hand).count(color) == 5:
                return True
        return False

    def get_numbers(self, hand):
        """Return list of values in hand
        :param hand
        :return nums"""
        nums = sorted([card.get_data()[0] for card in hand])
        for i in range(nums.count(1)):
            nums.remove(1)
            nums.append(14)
        nums = list(reversed(nums))
        return(nums)

    def get_colors(self, hand):
        """Return list of colors in hand
        :param hand
        :return color_list"""
        color_list = [card.get_data()[1] for card in hand]
        return color_list

    def straight_flush_and_royal_flush(self, hand):
        """Check if there is straight flush or royal flush
        :param hand
        :return scure, data, str-output"""
        list1 = self.get_numbers(hand)
        list2 = []
        for num in range(2,11):

            list2 = [num, num+1, num+2, num+3, num+4]
            if all(item in list1 for item in list2) and self.is_flush(hand):
                st = "Straight Flush, "+numbers[str(num+4)]+"-High"
                if num+4 == 14:
                    st = "Royal Flush"
                return 14*8+num+4, [], st

        list2 = [14,2,3,4,5]
        if all(item in list1 for item in list2) and self.is_flush(hand):
            return 14*8+5, [], "Straight Flush, "+numbers[str(5)]+"-High"
        else:
            return self.four_of_a_kind(hand)
            
    def four_of_a_kind(self, hand):
        """Check if there are four of the same type
        :param hand
        :return scure, data, str-output"""
        for num in self.get_numbers(hand):
            if self.get_numbers(hand).count(num)==4:
                return 14*7 + num, [i for i in self.get_numbers(hand) if i != num], "Four Of A Kind, " + numbers[str(num)]+"s"
        return self.full_house(hand)

    def full_house(self, hand):
        """Check if there is full house
        :param hand
        :return scure, data, str-output"""
        pairs1 = []
        for num in self.get_numbers(hand):
            if self.get_numbers(hand).count(num) == 3:
                pairs1.append(num)
        pairs2 = []
        for num in self.get_numbers(hand):
            if self.get_numbers(hand).count(num) == 2 and num not in pairs1:
                pairs2.append(num)
        if pairs1 != [] and pairs2 != []:
            return 14*6 +  pairs1[0], [pairs2[0]], "Full House "+numbers[str(pairs1[0])]+"s Full Of "+ numbers[str(pairs2[0])]+"s"
        return self.flush(hand)

    def flush(self, hand):
        """Check if there is flush
        :param hand
        :return scure, data, str-output"""
        for color in colors:
            if self.get_colors(hand).count(color) == 5:
                return 14*5, self.get_numbers(hand), "Flush"
        return self.straight(hand)
            
    def straight(self, hand):
        """Check if there is straight
        :param hand
        :return scure, data, str-output"""
        list1 = self.get_numbers(hand)
        list2 = []
        for num in range(2,11):
            list2 = [num, num+1, num+2, num+3, num+4]
            if all(item in list1 for item in list2):
                return 14*4 + num +4, [0], "Straight, " + numbers[str(num+4)] + " High"

        list2 = [14,2,3,4,5]
        if all(item in list1 for item in list2) :
            return 14*4 + 5, [0], "Straight, "+numbers["5"]+" High"
        else:
            return self.three_of_a_kind(hand)

    def three_of_a_kind(self, hand):
        """Check if there are three of the same type
        :param hand
        :return scure, data, str-output"""
        for num in self.get_numbers(hand):
            if self.get_numbers(hand).count(num)==3:
                return 14*3 + num, [i for i in self.get_numbers(hand) if i != num], "Three Of A Kind, " + numbers[str(num)]+"s"
        return self.two_pair_and_pair(hand)

    def two_pair_and_pair(self,hand):
        """Check if there is two pairs or a pair
        :param hand
        :return scure, data, str-output"""
        pairs = []

        for num in self.get_numbers(hand):
            if self.get_numbers(hand).count(num) == 2 and num not in pairs:
                pairs.append(num)
        
        if len(pairs) == 2:
            for num in self.get_numbers(hand):
                if self.get_numbers(hand).count(num) == 1:
                    y = [min(pairs), num]
            x = 14*2 + max(pairs)
            z = "Two Pairs " + numbers[str(max(pairs))] + "s And " + numbers[str(min(pairs))]+"s"
            return x,y , z
        elif len(pairs) == 1:
            return 14*1+ pairs[0], [i for i in self.get_numbers(hand) if i != max(pairs)], "Pair Of " + numbers[str(pairs[0])]+"s"
        else:
            return self.high_card(hand)

    def high_card(self,hand):
        """Check the highest card
        :param hand
        :return scure, data, str-output"""
        return self.get_numbers(hand)[0], self.get_numbers(hand), numbers[str(self.get_numbers(hand)[0])]+"-High"


def main():
    while(input("To quit enter 'q' or type enter to play: ") != "q"):
        nHands = int(input("Please enter number of hand: "))
        if nHands > 14 or nHands < 2:
            print("poker suitable to any number of players from 2 to 14")
            nHands = int(input("plese enter legal number: "))
        P = Poker(nHands).play()

if __name__ == "__main__":
    main()
