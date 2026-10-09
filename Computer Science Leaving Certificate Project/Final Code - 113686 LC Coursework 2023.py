import random
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import os.path

"""
Import all of the libraries to be used within the code of the project.
"""

response = requests.get('https://random-word-api.herokuapp.com/word?number=100') #fetches 100 different words already sorted into an array for JavaScript
words = response.json() # .json() changes the array to a Python list
wordsList = [word.lower() for word in words] #iteratees through each word and adds it to a Python list
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
filename = "hangmanData.csv" #determine the name of the .csv file for the lines below

if not os.path.isfile(filename): #if there is not a file already present in the computer named hangmanData.csv
    with open('hangmanData.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Game Mode", "Hangman Word", "Word Length", "Total Incorrect Guesses", "Result"])
        file.close() #the file will be created, headings added and closed
else: 
    print('CSV file: \'hangmanData.csv\' already exists') #else if the file already exists on the computer
    resetPrompt = False
    while resetPrompt == False: #validates input
        reset = input('Do you want to reset the file? (Yes/No): ').lower()
        if reset == 'yes':
            with open('hangmanData.csv','w', newline='') as file: #'w' clears the file and enters the headings again 
                writer = csv.writer(file)
                writer.writerow(["Game Mode", "Hangman Word", "Word Length", "Total Incorrect Guesses", "Result"])
                file.close()
            resetPrompt = True
            
        elif reset == "no":
            resetPrompt = True #skips over the while loop
        
        else:
            print(reset, "is an invalid input.") #yes or no wasn't inputted


def mean(numbers): #function for calculating mean
    return sum(numbers) / len(numbers) 

def median(numbers): #function for calculating median
    n = len(numbers)
    sorted_numbers = sorted(numbers)
    if n % 2 == 0:
        # If the list has an even number of elements, the median is the average of the two middle elements
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        # If the list has an odd number of elements, the median is the middle element
        return sorted_numbers[n//2]
    
def find_mode(numbers): #function for calculating mode
    counts = {}

    for num in numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

    mode = max(counts, key=counts.get)

    return mode

def count_letter_frequency(letter, strings): #function for calculating frequency
    frequency = 0
    for string in strings:
        frequency += string.count(letter)
    return frequency


def singleplayer(totalGuessesIn, wordsListIn): #function for playing singleplayer Hangman
    hangmanWord = random.choice(wordsListIn) #determines a word at random from the 100 fetched list of words
    hangmanWord = hangmanWord.lower() # converts it to all lowercase
    hyphenatedWord = "-" * len(hangmanWord) # creats a hyphenated word with a hyphen for each letter in the word
    wrongGuesses = 0 # initialises the number of wrong guesses to be allowed
    usedLetters = [] # initialises the list to track used letters

    while wrongGuesses != totalGuessesIn and hyphenatedWord != hangmanWord: # makes sure the game is incomplete
        print("You currently have", totalGuessesIn-wrongGuesses, "incorrect guesses left.") # how many guesses are left
        print("You have used the letters", usedLetters) # letters already used
        print("Time to guess!")
        print("")
        print(hyphenatedWord) # prints the current progression of the Hangman word
       
        guess = input("Please enter your guess: ") # take in letter input
        guess = guess.lower() # to account for the input of a capital letter, perhaps by accident
        print("")
       
        if guess not in letters:# use not in to determine if the inputted guess is an actual letter or invalid guess
            while guess not in letters: # creates a loop until the user enters a valid letter
                print(guess, "is not a letter.")
                guess = input("Please re-enter your guess: ")
                guess = guess.lower()
                print("")
                if guess in letters:
                    break
           
       
        if guess in usedLetters: # creates a loop until the user enters a letter that is valid and hasn't been used
            while guess in usedLetters or guess not in letters:
                print(guess, "cannot be guessed.")
                guess = input("Please re-enter your guess: ")
                guess = guess.lower()
                print("")
                if guess.isalpha() and guess not in usedLetters and len(guess) == 1:
                    break
           
        usedLetters.append(guess) # append the letter to used letters list
        
        if guess in hangmanWord:
            print(guess, "is in the word!")
            
            temporary = "" #create a temporary word to create the new progression of word
            
            for i in range(len(hangmanWord)): # loop for length of Hangman word
                if guess == hangmanWord[i]: # if the letter was in the word
                    temporary += guess # add the letter to the current progression of word
                
                else:
                    temporary += hyphenatedWord[i] # add a hyphen
            
            hyphenatedWord = temporary # set current progression to new progression
            
        
        else:
            print(guess, "is not in the word.") # letter wasn't present, add wrong guess to total
            wrongGuesses += 1
            
        if wrongGuesses == totalGuessesIn: # if maximum amount of guesses have been used, game is over
            print("")
            print("You have run out of guesses!\nThe word was", hangmanWord, "\nGAME OVER")
            print("")
            result = "Lose" # written to .csv file
    
        elif hyphenatedWord == hangmanWord: # if the progression of word is complete (same as Hangman word)
            print("You have successfully guessed the word!")
            print("The word was", hangmanWord)
            result = "Win" # written to .csv file
        
        else:
            print("The game continues!")
            
    with open('hangmanData.csv', 'a', newline='') as file: # after the game finishes, write the results of the game to .csv file under relvant headings
        writer = csv.writer(file)
        writer.writerow(["Singleplayer", hangmanWord, len(hangmanWord), wrongGuesses, result]) # writes the mode, the Hangman word, length of word, total amount of wrong guesses and result of game
        file.close()
            

def multiplayer(totalGuessesIn):
    hangmanWord = input("Player 1, please enter the word to be guessed: ") # Player 1 is allowed to set the Hangman word
    hangmanWord = hangmanWord.lower() # accounts for capital letters
    if hangmanWord.isalpha() == False or len(hangmanWord) < 3:
        validWord = False
        while validWord == False:
            print(hangmanWord, "is not a valid word. There must only be letters present, at a minimum length of 3 letters.")
            hangmanWord = input("Please re-enter the word: ")
            hangmanWord = hangmanWord.lower()
            print("")
            if hangmanWord.isalpha() and len(hangmanWord) > 2:
                validWord = True
    
    hyphenatedWord = "-" * len(hangmanWord) # creates the hyphenated word with same length of Hangman word
    wrongGuesses = 0
    usedLetters = []
   
    while wrongGuesses != totalGuessesIn and hyphenatedWord != hangmanWord: # Player 2 gets to play the game to completion after Player 1 sets the word
        print("Player 2, you currently have", totalGuessesIn-wrongGuesses, "incorrect guesses left.")
        print("You have used the letters", usedLetters)
        print("Time to guess!")
        print("")
        print(hyphenatedWord)
       
        guess = input("Player 2, please enter your guess: ")
        guess = guess.lower() # to account for the input of a capital letter
        print("")
       
        if guess not in letters:# use not in to determine if the inputted guess is an actual letter or invalid guess
            while guess not in letters: # creates a loop until the user enters a valid letter
                print(guess, "is not a letter.")
                guess = input("Please re-enter your guess: ")
                guess = guess.lower()
                print("")
                if guess in letters:
                    break
           
       
        if guess in usedLetters: # creates a loop until the user enters a letter that is valid and hasn't been used
            while guess in usedLetters or guess not in letters:
                print(guess, "cannot be guessed.")
                guess = input("Please re-enter your guess: ")
                guess = guess.lower()
                print("")
                if guess.isalpha() and guess not in usedLetters and len(guess) == 1:
                    break
           
        usedLetters.append(guess)
        
        if guess in hangmanWord:
            print(guess, "is in the word!")
            
            temporary = ""
            
            for i in range(len(hangmanWord)):
                if guess == hangmanWord[i]:
                    temporary += guess
                
                else:
                    temporary += hyphenatedWord[i]
            
            hyphenatedWord = temporary
            
        
        else:
            print(guess, "is not in the word.")
            wrongGuesses += 1
            
        if wrongGuesses == totalGuessesIn:
            print("")
            print("Player 2, you have run out of guesses!\nThe word was", hangmanWord, "\nGAME OVER")
            print("")
            result = "Lose"
    
        elif hyphenatedWord == hangmanWord:
            print("Player 2, you have successfully guessed the word!")
            print("The word was", hangmanWord)
            result = "Win"
        
        else:
            print("The game continues!")
            
    with open('hangmanData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Multiplayer", hangmanWord, len(hangmanWord), wrongGuesses, result]) # Writes results to .csv file, in this case with Multiplayer under gamemode
        file.close()


def simulation(totalGuessesIn, wordsListIn, whatifListIn): # takes in arguments for total guesses allowed, the list of words to choose from and the what if hypothesis to be asked
    hangmanWord = random.choice(wordsListIn) # selects random word
    hangmanWord = hangmanWord.lower() # sets to lower case
    hyphenatedWord = "-" * len(hangmanWord) # creates hyphenated word to be displayed
    wrongGuesses = 0
    usedLetters = []
    guessItem = 0 # sets number to be used for iterating through list of letters to be guessed
    wordLength = len(hangmanWord) # initialises wordLength to be used when automatically guessing word

    while wrongGuesses != totalGuessesIn and hyphenatedWord != hangmanWord:
        print("The simulation has", totalGuessesIn-wrongGuesses, "incorrect guesses left.")
        print("It has used the letters", usedLetters)
        print("It is now guessing...")
        print("")
        print(hyphenatedWord)

        if hyphenatedWord.count("-") <= 2 and wordLength <= 6 or hyphenatedWord.count("-") <= 3 and wordLength > 6:
        #if the word is 6 or less letters in length and 2 or less unknown letters remain, or if the word is more than 6 in length and 3 or less unknown letters remain
            print("The simulation has automatically guessed the word!")
            print("The word was", hangmanWord)
            result = "Win"
            break # break out of the while loop, moving on to writing the results to .csv
        
        guess = whatifListIn[guessItem] # guess item increases for each letter guessed from list of letters from hypothesis
        guessItem += 1 # increments guess item so that it guesses next letter in list on next run of loop
        guess = guess.lower() # to account for the input of a capital letter
        print("")


        usedLetters.append(guess)

        if guess in hangmanWord:
            print(guess, "is in the word!")

            temporary = ""

            for i in range(len(hangmanWord)):
                if guess == hangmanWord[i]:
                    temporary += guess

                else:
                    temporary += hyphenatedWord[i]

            hyphenatedWord = temporary


        else:
            print(guess, "is not in the word.")
            wrongGuesses += 1

        if wrongGuesses == totalGuessesIn:
            print("")
            print("The simulation has run out of guesses!\nThe word was", hangmanWord, "\nGAME OVER")
            print("")
            result = "Lose"

        elif hyphenatedWord == hangmanWord:
            print("The simulation has successfully guessed the word!")
            print("The word was", hangmanWord)
            result = "Win"

        else:
            print("Still guessing...")
            print("")
            
    with open('hangmanData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Simulation", hangmanWord, len(hangmanWord), wrongGuesses, result])
        file.close()


# -----------------------------------------------------------------------------------------------------------------------------
"""
Below is the initialisation of the what if hypotheses and the gamemode selection. The line above marks the gap between functions and the below code for clarity.
"""
print("")
#The lists below will be iterated through, with each iteration using the relevant list item as letter to be guessed in simulation.
whatifMostFrequent = ["e", "t", "a", "o", "n", "r", "i", "s", "h", "d", "l", "f", "c", "m", "u", "g", "y", "p", "w", "b", "v", "k", "j", "x", "z", "q"] #based on Herbert S. Zim's "Codes and Secret Writing".
whatifVowels = ["a", "e", "i", "o", "u", "t", "n", "r", "s", "h", "d", "l", "f", "c", "m", "g", "y", "p", "w", "b", "v", "k", "j", "x", "z", "q"] # what if we began with all 5 vowels, then the most frequent letters. 
whatifLeastFrequent = ["q", "z", "x", "j", "k", "v", "b", "w", "p", "y", "g", "u", "m", "c", "f", "l", "d", "h", "s", "i", "r", "n", "o", "a", "t", "e"] #based on Herbert S. Zim's "Codes and Secret Writing", reversing the most frequent letters list.

validGamemode = False

while validGamemode == False: # used to validate gamemode input, causes the gamemode selection to be prompted again upon game completion
    gamemode = input("Would you like to play singleplayer (s), multiplayer (m), simulation (sim), or move on to analysis (a)?: ")
    gamemode = gamemode.lower() # to account for capital letter(s) entered
    
    if gamemode == "s":
        
        validGuesses = False # used to validate the input of guesses to be allowed as integers
        while validGuesses == False:
            print("")
            totalGuesses = input("How many wrong guesses would you like to allow yourself?: ")
            if totalGuesses.isnumeric() == True: # if the input is a number, regardless of being a string or integer.
                totalGuesses = int(totalGuesses)# set the string to an integer
                if totalGuesses > 0:
                    singleplayer(totalGuesses, wordsList) # use the new integer as guesses to be allowed
                    validGuesses = True # exits the allowed guesses input while loop
                print("")
            else:
                print(totalGuesses, "is an invalid input.") # loops back to gamemode input
                print("")
                       
    elif gamemode == "m":
        
        validGuesses = False
        while validGuesses == False:
            totalGuesses = input("How many wrong guesses would you like to allow?: ")
            if totalGuesses.isnumeric() == True:
                totalGuesses = int(totalGuesses)
                if totalGuesses > 0:
                    multiplayer(totalGuesses)
                    validGuesses = True
            else:
                print(totalGuesses, "is an invalid input.")
                print("")

    elif gamemode == "sim":
                       
        validGuesses = False
        while validGuesses == False:
            print("")
            totalGuesses = input("How many wrong guesses would you like to allow the simulation?: ")
            if totalGuesses.isnumeric() == True:
                totalGuesses = int(totalGuesses)
                if totalGuesses > 0:
                    totalGuesses = int(totalGuesses)
                    validGuesses = True
            else:
                print(totalGuesses, "is an invalid input.")
                print("")
        
        validWhatif = False
        while validWhatif == False: # while loop used to check if a valid input has been entered for what if hypothesis
            print("")
            desiredWhatif = input("Which what-if question would you like answered?\nFor guessing by the most frequent letters, type 1.\nFor guessing with the 5 vowels then letter frequency, type 2.\nFor guessing by the least frequent letters, type 3.\n: ")
            if desiredWhatif == "1":
                whatifList = whatifMostFrequent
                validWhatif = True
            elif desiredWhatif == "2":
                whatifList = whatifVowels
                validWhatif = True
            elif desiredWhatif == "3":
                whatifList = whatifLeastFrequent
                validWhatif = True
            else:
                print(desiredWhatif, "is an invalid input.")
        
        print("")
        validSimulations = False
        while validSimulations == False: # while loop used to check if the amount of desired simulations entered is valid or not
            totalSimulations = input("How many times would you like the simulation to run?: ")
            if totalSimulations.isnumeric() == True:
                totalSimulations = int(totalSimulations) # changes string input to int if it is a valid number
                if totalSimulations > 0:
                    for i in range(totalSimulations): # loops amount of times that has been inputted
                        simulation(totalGuesses, wordsList, whatifList)
                    validSimulations = True # exits loop
                else:
                    print(totalSimulations, "is an invalid input.")
                    print("")
            else:
                print(totalSimulations, "is an invalid input.")
                print("")
    elif gamemode == "a": # if analysis is desired, breaks out of the while loop and moves on to analysis loop
        break
    
    else:
        print(gamemode, "is an invalid input.")
        print("")

# -----------------------------------------------------------------------------------------------------------------------------
"""
Below is the analysis section of my code. Plenty of print("") statements are used for clarity in my code not only when it is outputted, but also when writing my code.
"""
print("")
print("")
analysisDecision = False
while analysisDecision == False:
    viewAnalysis = input("Would you like to view the statistical analysis? (Yes/No): ") # if the user does not want to view analysis and exit the program, they can enter no
    viewAnalysis = viewAnalysis.lower()
    if viewAnalysis == "yes": # if input is yes, the true variable will enable a while loop below to execute
        promptAnalysis = True
        analysisDecision = True
    elif viewAnalysis == "no":
        promptAnalysis = False
        analysisDecision = True# skips analysis and ends program
    else:
        print(viewAnalysis, "is an invalid input.")

displayData = pd.read_csv('hangmanData.csv') # takes in the data from the data table and sets it to a variable

while promptAnalysis == True:
    whichAnalysis = input("Which statistical analysis would you like to view?:\nTo view the data table, type 1.\nTo view the 26 letter frequencies, type 2.\nTo view the Win/Loss pie chart, type 3.\nTo view the mean length of the Hangman word, type 4.\nTo view the most common length of the Hangman word, type 5.\nTo view the top 5 letter frequencies, type 6.\nIf you would like to exit the program, type DONE.\nPlease enter your choice here: ")
    whichAnalysis = whichAnalysis.lower()
    
    if whichAnalysis == "1":
        # Data Table is displayed

        print("")
        print(displayData.to_string()) # prints the .csv file in an easy to read format
        print("")

    elif whichAnalysis == "2":
        # The 26 letter frequencies in order of the alphabet
        
        print("")
        letterFrequencies = [] # list to append letter frequencies to
        correlatingLetters = [] # list to append correlating letter of letter frequecy at the same index position
        for i in range(len(letters)): # loops 26 times, one for each letter of alphabet
            frequency = count_letter_frequency(letters[i], wordsList) # use frequency function
            print("The letter", letters[i], "appears", frequency, "times in the list of words.") # prints the current letter and its frequency
            letterFrequencies.append(frequency) # adds to the letter frequencies, used further on to determine top 5 letter frequencies
            correlatingLetters.append(letters[i]) # adds letter to correlating index position of frequency

        print("")

    elif whichAnalysis == "3":
        # Win/Loss Pie Chart
        
        print("")
        resultsList =  list(displayData["Result"]) # sets a list of all results
        simulationTotal = len(resultsList) # sets total amount of simulations for percentage calculations
        totalWinPercentage = round((resultsList.count("Win")/simulationTotal) * 100, 1) # calculates the win percentage, rounded to 1 decimal place.
        totalLossPercentage = round((resultsList.count("Lose")/simulationTotal) * 100, 1) # calculates the loss percentage, rounded to 1 decimal place.
        print(totalWinPercentage,"% of simulated games ended with a win. Therefore", totalLossPercentage,"% of simulated games ended with a loss.") # prints results of calculations
        resultPieChart = np.array([totalWinPercentage, totalLossPercentage]) # initialises the pie chart
        labels = ["Win", "Loss"] # sets the labels for each slice of the pie chart

        plt.pie(resultPieChart, labels = labels, startangle = 90) # set the pie chart with relevant details
        plt.show() #displays the pie chart
        print("")

    elif whichAnalysis == "4":
        # Average length of a word that was in wordsList
        
        wordlengthList =  list(displayData["Word Length"])
        print("")
        print("The mean length of a word according to the data table of previously used Hangman words was", round(mean(wordlengthList), 0), "letters in length.") # use mean function to calculate average length of a word
        print("")
        
    elif whichAnalysis == "5":
        # Most common length of a word that was in wordsList
        
        wordlengthList =  list(displayData["Word Length"])
        print("")
        print("The most common length of a word according to the data table of previously used Hangman words was", find_mode(wordlengthList), "letters in length.") # use mode function to calculate most common length of a word
        print("")

    elif whichAnalysis == "6":
        # Top 5 Frequent Letters
         
        for i in range(5): # loop 5 times for top 5 letter frequencies
            topFrequency = max(letterFrequencies) # sets current top frequency to the variable topFrequency
            topfrequencyPosition = letterFrequencies.index(topFrequency) # sets the index position of the top frequency
            relevantLetter = correlatingLetters[topfrequencyPosition] # which is then used to find correlating letter with same index position
            print("")
            print("The letter", relevantLetter,"appears", topFrequency,"times in the list of words.") # print the results
            letterFrequencies.remove(topFrequency) # remove both the top frequency
            correlatingLetters.remove(relevantLetter) # and its relevant letter from both lists
            
        print("")

    elif whichAnalysis == "done":
        break # ends loop and finishes program
    
    else:
        print(whichAnalysis, "is an invalid input.") # loops back around for a valid input