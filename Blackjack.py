import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
			'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
		self.value = values[rank]

	def __str__(self):
		return self.rank + " of " + self.suit

class Deck:

	def __init__(self):
		self.deck = []

		for suit in suits:
			for rank in ranks:
				created_card = Card(suit,rank)
				self.deck.append(created_card)

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + card.__str__()
		return "The deck has: " + deck_comp

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return self.deck.pop()

class Hand:

	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0

	def add_card(self,card):
		self.cards.append(card)
		self.value += values[card.rank]

		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_ace(self):
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

class Chips:

	def __init__(self):
		self.total = 100
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet

def take_bet(chips):

	while True:

		try:
			chips.bet = int(input('How many chips would you like to bet? '))
		except ValueError:
			print("Please try again. Bet must be an integer")

		else:
			if chips.bet > chips.total:
				print("Not enough funds! You have {}".format(chips.total))
			else:
				break

def hit(deck,hand):

	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def hit_or_stand(deck,hand):
	global playing

	while True:

		player_call = input("Hit or stand? ")

		if player_call == 'Hit' or player_call == 'hit' or player_call == 'h':
			hit(deck,hand)

		elif player_call == 'Stand' or player_call == 'stand' or player_call == 's':
			print("Player stands. Dealer's turn")
			playing = False
		
		else:
			print("Please try again")
			continue
		break

def show_some(player,dealer):

	print("\n Dealer's Hand: ")
	print(" <card hidden> ", dealer.cards[1])
	print("\n Player's Hand: ")
	print(*player.cards, sep='\n')

def show_all(player,dealer):

	print("\n Dealer's Hand: ")
	print(*dealer.cards, sep = '\n')
	print("\n Dealer's Hand value: ", dealer.value)
	print("\n Player's Hand: ")
	print(*player.cards, sep = '\n')
	print("\n Player's Hand value: ", player.value)

def player_busts(player,dealer,chips):

	print("Bust! Dealer wins!")
	chips.lose_bet()

def player_wins(player,dealer,chips):

	print("Player wins!")
	chips.win_bet()

def dealer_wins(player,dealer,chips):

	print("Dealer wins!")
	chips.lose_bet()

def dealer_busts(player,dealer,chips):

	print("Dealer bust! Player wins!")
	chips.win_bet()

def push(player,dealer,chips):

	print("Dealer and Player tie! Push!")

while True:

	print("Welcome to Blackjack!")

	game_deck = Deck()
	game_deck.shuffle()

	player_hand = Hand()
	player_hand.add_card(game_deck.deal())
	player_hand.add_card(game_deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(game_deck.deal())
	dealer_hand.add_card(game_deck.deal())

	player_chips = Chips()

	take_bet(player_chips)

	show_some(player_hand,dealer_hand)

	while playing:

		hit_or_stand(game_deck,player_hand)

		show_some(player_hand,dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand,dealer_hand,player_chips)
			break

	if player_hand.value <= 21:

		while dealer_hand.value < player_hand.value:
			hit(game_deck,dealer_hand)

		show_all(player_hand,dealer_hand)

		if dealer_hand.value > 21:
			dealer_busts(player_hand,dealer_hand,player_chips)

		elif dealer_hand.value > player_hand.value:
			dealer_wins(player_hand,dealer_hand,player_chips)

		elif dealer_hand.value < player_hand.value:
			player_wins(player_hand,dealer_hand,player_chips)

		else:
			push(player_hand,dealer_hand,player_chips)

	print("Your total so far: {}".format(player_chips.total))

	play_again = input("Would you like to play again? ")

	if play_again == 'Yes' or play_again == 'yes' or play_again == 'y':
		playing = True
		continue

	else:
		print("Thanks for playing!")
		break

