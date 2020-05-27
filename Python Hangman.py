import random
import os #os.system('cls') linux: os.system('clear') 
import time
import json
HANGMAN_ASCII_ART = """\
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/"""
print(HANGMAN_ASCII_ART)
def printStatus(mistakes): #Accepts mistakes number and prints the status of hangman.
	if mistakes == 1:
		print("""\
x-------x
			""")
		return;
	if mistakes == 2:
		print("""\
x-------x
|
|
|
|
|
""")
		return;
	if mistakes == 3:
		print("""\
x-------x
|       |
|       0
|
|
|
""")
		return;
	if mistakes == 4:
		print("""\
x-------x
|       |
|       0
|       |
|
|
			""")
		return;
	if mistakes == 5:
		print("""\
x-------x
|       |
|       0
|      /|\\
|
|

			""")
		return;
	if mistakes == 6:
		print("""\
x-------x
|       |
|       0
|      /|\\
|      / 
|
			""")
		return;
	if mistakes == 7:
		print("""\
x-------x
|       |
|       0
|      /|\\
|      / \\
|
			""")
		return;
def check_If_In_Word(guessed_letter): # Checks if guessed_letter exists in word.
	index = 0
	found = False
	global word
	global mistakes
	global hidden_word
	hidden_word_list = list(hidden_word)
	while index < len (word): 
		
		if word.find(guessed_letter,index) == -1:
			break
		else:
			if not found:
				print("Correct! :)")
				found = True
			hidden_word_list[word.find(guessed_letter,index)] = guessed_letter
			index += 1
	if not found:
		mistakes += 1
		print("False :( you now have " + str(mistakes) + " mistakes")

			
		
		
	return turn_list_to_string(hidden_word_list);
def turn_list_to_string(liststr):# Accepts a list and returns a string from that list.
	word = ""
	for item in liststr:
		word += "" + str(item)
	return word;
def print_word(word): #Prints the hidden word with spaces, more aesthetically.
	index = 0
	wordlist = list(word)
	while index<len(word):
		print(str(wordlist[index]) + " ", end='')
		index += 1 	
	print()
def game_set():
	os.system('cls')
	global words
	global word
	global play 
	global hidden_word
	global mistakes
	global tries
	global user_input
	word = words['data'][random.randrange(0,2465)]
	user_input = ""
	tries = []
	play = True
	hidden_word = ""
	mistakes = 0
	for chr in word:
		hidden_word += "_"
def is_guessed(hidden_word):
	if int(hidden_word.find('_',0)) == -1:
		return True
	else:
		return False
def resume_playing(user_input):
	global running 
	while user_input != "y" and user_input != "n":
		user_input = input("Please insert y/n")
	if user_input == "y":
		print("Game is restarting...")
	else:
		os.system('cls')
		print("Thanks for playing, Goodbye!")
		running = False
		time.sleep(1.5)
with open('words.json' , 'r') as f:
	words = json.load(f)

running = True
while running:
	time.sleep(0.5)
	game_set() 
	while play:
		time.sleep(1.5)
		os.system('cls')
		printStatus(mistakes)
		print("The word is: ")
		print_word(hidden_word)
		print("Your tries are: " +  str(tries))
		user_input = input("Guess a letter:")
		if user_input not in tries and user_input.isalpha() and len(user_input) == 1:
			guessed_letter = user_input
			hidden_word = check_If_In_Word(guessed_letter)
			tries.append(guessed_letter)
			if is_guessed(hidden_word):
				play = False
				os.system('cls')
				printStatus(mistakes)
				print("Win! The word is:")
				print("\"" + word + "\"")
				user_input = input("Replay? y/n")
				resume_playing(user_input)
			if mistakes == 7:
				os.system('cls')
				printStatus(mistakes)
				print("Hangman is dead :( the word was: \"" + word+ "\"")
				print("YOU LOSE!")
				play = False
				user_input = input("Replay? y/n")
				resume_playing(user_input)

		else:
			print("Invalid input, please try again. (Remmember: You cannot guess the same letter twice!)")








