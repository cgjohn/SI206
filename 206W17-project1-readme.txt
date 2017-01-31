206 Project 1 - Code for playing cards
README

Your name:Connor Johnston
Anyone you worked with:Jonathan Bain

----- Add your README file content for the Project 1 code.
 

This code simulates the human card game: War! Which in this case is a 2-person game using only 52 cards, giving each player a hand of 26. When ran with ‘testing=False’ as a parameter to play_war_game, the code prints out step-by-step which player wins each card play. At the end of the function, the final scores are stated and a winner is declared. If the parameter ‘testing=True’ is passed in, the game only outputs the final results with a Winner, and the score. The code is sectioned off into three main classes and a driver function that plays the actual game of War. The class; Card, Deck, and Hand, allow for them to be reused with many card games without having to change their code. Methods may need to be added or not be used in some cases if the game were different, but the general structure would still be used. This modular code allows for their to be multiple driver functions that could play different games.

——————————
CARD CLASS
——————————

The card class allows the program to create an instance
of a playing card. These cards serve as the base components
that make up the other two classes: Deck and Hand. There
are four suits and 14 differently ranked cards of each suit to simulate all normal playing cards. 

CONSTRUCTOR 
	Input -The method has two optional inputs, suit and rank, that can be used to create a specific card that using numbers representing suits (0-3) and ranks (0-13). If no inputs are added, the default constructed card is Card(0,2) or the Two of Diamonds.
	
__STR__
	This method overrides the default way of an instance being printed and allows them to be printed as “Rank” of “Suit”.

———————————
DECK CLASS
———————————

The Deck class allows an instance of a deck of cards to be created. A deck contains 52 cards, which represents all 52 combinations of the 4 suits and 13 differently ranked cards in the Card Class. 

CONSTRUCTOR - 
	The Deck class constructor does not take in any input and relies on the Card class to function properly. The method creates a deck that is sorted in order.

__STR__ 
	Reformats the printed version of a Deck instance. Printing the variable would result in a multi-line string list each individual card in the same card.__str__ formate as above.

POP_CARD 
	This method removes a card from the deck and returns it to the call. It is like playing a card or dealing one.

SHUFFLE 
	The shuffle method does not take in any inputs. It simulates the shuffling of a deck by randomizing the order of the cards in the deck.

REPLACE_CARD
	The replace_card method takes in an input of an existing card instance. It then checks to see if that card exists in the deck already. If it does not, the method adds the card to the deck.

SORT_CARDS
	The sort_cards method does not take in any inputs. The method puts the deck back in the order that it would have been in when it was created.

——————————
HAND CLASS
——————————

An instance of the Hand class represents a players hand that is dealt from the Deck. These are the cards that a player would have access to when playing a game.

CONSTRUCTOR
	For the Hand class constructor a Deck instance is required. There is also an optional parameter to decide the size of the hand.The default size is set to 5 but can be specified to anything from 0 to 26.

PLACE_CARD
	The place_card method removes and returns a card from a hand. The method defaults to the card at index 0 but has an optional input to pass in the index of a card to be removed.

GET_SUITS_AVAILABLE
	The get_suits_available requires no input and has no optional inputs. The method returns a list of all of the suits that are in the hand instance. It does not alter the hand instance.

GET_RANKS_AVAILABLE
	The get_ranks_available method requires no input and has no optional inputs. The method returns a list of all of the ranks that are in the hand instance. It does not alter the hand instance.

SPECIFIC_CARD
	The specific_card method requires the input of a card rank and a card suit. The method searches the hand for the given card. If the card exists, the card is removed from the hand instance and returned from the method. If the card does not exist in the hand, the method returns the value of ‘None’.

ADD_CARD
	The add_card method has one required input of a card instance. The method checks the hand instance to see if the card already exists within it. If it does, the card is not added to the hand. Otherwise, the card is added to the hand instance.

__STR__
	The __str__ method has no optional or required inputs. The method overrides the default str operator and allows a hand to be printed as individual cards in the format of ‘rank’ of ‘suit’

