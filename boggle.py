"""This file contains utilities related to Boggle game; providing utility functions for creating a random Boggle board, checking the validity of a word on the board, and finding a word on the board using a recursive approach."""

#import nessesary modules
    #The choice function from the random module is used to randomly select elements from a list.
    #The string module provides various constants and functions for working with strings.
from random import choice
import string


# define a class for boggle game
class Boggle():
 
    # define init function as constructor for boggle class
    #self method is used to initialize the Boggle instance
    def __init__(self):
    
        # Here we initialize the words attribute of the Boggle instance by calling the read_dict method with the path to a dictionary file ("words.txt").
        # The read_dict method reads and returns all the words from the dictionary file in a list.
            #Here, we use the self method to get all the words from the dictionary file and return them as a list

        self.words = self.read_dict("words.txt")
    # read_dict method is used to read the dictionary file and return a list of words.
        #self method is used to read the dictionary file and return a list of words.
        #dict_path is the full path to the dictionary file.
    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""
        
        #open the dictionary file and reads each line from list and remove leading and trailing spaces using strip method
        # for w in dict_file adds each word to the list of words
        #dict_file.close closes the file
        # returns the list of words
        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self):
        """Make and return a random boggle board."""
        #initialize an empty board list
        board = []
        # It iterates y from 0 to 4 to represent each row of the board.
        for y in range(5):
            #Within each row, it generates a list comprehension that selects a random uppercase letter from string.ascii_uppercase (which contains all uppercase letters) for each column (i) in the range 0 to 4.
            #the row is then appended to the board list.
            row = [choice(string.ascii_uppercase) for i in range(5)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""

        # checks if word exists in words list (dictionary) using the in operator.
        #also checks if word is a valid word in the boggle board by calling find, and passes the board and the uppercase version of the word.
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())
        #Depending on the results, it assigns the appropriate value to the result variable: "ok" if the word exists in the dictionary and is on the board, "not-on-board" if the word exists in the dictionary but is not on the board, and "not-word" if the word doesn't exist in the dictionary
        # Finally, it returns the result.
        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result
    #The find_from method is a recursive helper function used by the find method to find a word on the board:
        #It takes the board, the word to find, the current position (y and x), and a seen set (to keep track of visited positions).
        # It checks if the current position is out of bounds (greater than 4) and returns if so.
        # It has several bases (conditions that determine when to stop recursion) to check:
        # If the current letter on the board doesn't match the first letter of the word, it returns False.
        # If the current position has already been seen (in the current path), it returns False
        # If the length of the word is 1 (i.e., we have found the last letter of the word), it returns True.
    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""

        if x > 4 or y > 4:
            return

        # This is called recursively to find smaller and smaller words
        # until all tries are exhausted or until success.

        # Base case: this isn't the letter we're looking for.

        if board[y][x] != word[0]:
            return False

        # Base case: we've used this letter before in this current path

        if (y, x) in seen:
            return False

        # Base case: we are down to the last letter --- so we win!

        if len(word) == 1:
            return True

        # Otherwise, this letter is good, so note that we've seen it, and try of all of its neighbors for the first letter of the rest of the word
        # This next line is a bit tricky: we want to note that we've seen the letter at this location. However, we only want the child calls of this
        # to get that, and if we used `seen.add(...)` to add it to our set, *all* calls would get that, since the set is passed around. That would mean that once we try a letter in one call, it could never be tried again,even in a totally different path. Therefore, we want to create a *new* seen set that is equal to this set plus the new letter. Being a new object, rather than a mutated shared object, calls that don't descend from us won't have this `y,x` point in their seen.
        
        # To do this, we use the | (set-union) operator, read this line as "rebind seen to the union of the current seen and the set of point(y,x))."
        # (this could be written with an augmented operator as "seen |= {(y, x)}",
        # in the same way "x = x + 2" can be written as "x += 2", but that would seem harder to understand).

        seen = seen | {(y, x)}

        # adding diagonals

        if y > 0:
            if self.find_from(board, word[1:], y - 1, x, seen):
                return True

        if y < 4:
            if self.find_from(board, word[1:], y + 1, x, seen):
                return True

        if x > 0:
            if self.find_from(board, word[1:], y, x - 1, seen):
                return True

        if x < 4:
            if self.find_from(board, word[1:], y, x + 1, seen):
                return True

        # diagonals
        if y > 0 and x > 0:
            if self.find_from(board, word[1:], y - 1, x - 1, seen):
                return True

        if y < 4 and x < 4:
            if self.find_from(board, word[1:], y + 1, x + 1, seen):
                return True

        if x > 0 and y < 4:
            if self.find_from(board, word[1:], y + 1, x - 1, seen):
                return True

        if x < 4 and y > 0:
            if self.find_from(board, word[1:], y - 1, x + 1, seen):
                return True
        # Couldn't find the next letter, so this path is dead

        return False
    
    #The find method finds a word on the board by calling find_from for each position on the board:
        #It iterates over each position on the board using nested loops.
        # For each position, it calls find_from with the board, the word to find, the current position (y and x), and an empty seen set.
        # If find_from returns True (i.e., a valid word is found starting from that position), it immediately returns True.
        # If no valid word is found from any position, it returns False.
    def find(self, board, word):
        """Can word be found in board?"""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, 5):
            for x in range(0, 5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.

        return False
