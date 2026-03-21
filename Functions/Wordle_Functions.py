import random
from collections import Counter
import re

Version = 6.1

# Imports file name as passed variable appending the Functions and .csv to the file.
def fImportList(file):
    wordlist = open(fr'Functions/{file}.csv', encoding='utf-8-sig')
    wl = wordlist.read().strip().upper()
    wl = wl.split('\n')
    for i in wl:
        if ' ' in i:
            wl.remove(i)        
    return wl

# This function as built specifically to load by the 'Word List' files.
# Dynamically building this based on the files in the directory is overkill for a list that hasn't been updated in years and has 2,317 words
def fCombinedLists():
    wl1 = fImportList('Word List')
    wl2 = fImportList('Word List_2')
    wlt = wl1 + wl2
    wl = list(set(wlt))
    print(f'Word lists loaded and cleaned')
    return wl

# This is the original vesion of the random word function.  It does not take the remaining list into account.
def fRandomWord(wl):
    # Handles the blank list logic
    if not wl:
        return wl    
    wl = list(wl)
    sw = random.randint(0,len(wl)-1)
    print(f'Next Word: {wl[sw]}')

# This only works with the 'Word List.csv' file and lines up with the puzzle number.  
# The puzzle nuber increments by 1 each day so technically you can find the curent and future puzzle answers knowing the previous date/s answer
def fPuzzleAnswer(puzzleNo):
    fl = fImportList('Word List')
    print(f'Answer: {fl[puzzleNo]}')

# This section takes the 'remove' list from the fRemoveBlackLetters and fRemoveYellowLetters functions
def fRemove_from_list(to_be_deleted, original):
    # converting the lists to a SET was for speed purposes
    new_list = list(set(to_be_deleted) ^ set(original))
    print(f'Removed: {len(set(to_be_deleted))} words\nWords Remaining: {len(new_list)}') 
    return new_list

# This section's logic is specific to the black letters. It loops through each letter and word removing all words containing the black letter from the list
def fRemoveBlackLetters(black_letters, word_list):
    # Handles the blank list logic
    if not black_letters:
        return word_list
    # SET conversion was done to speed up the process
    wordlist = set(word_list)
    wordlist_to_delete = []
    #Identifies the words with any of the identified black letter
    for word in wordlist:
        if any(letter in word for letter in black_letters.upper()):
            wordlist_to_delete.append(word)
    # Returns as new list with all the identified words removed.
    return fRemove_from_list(wordlist_to_delete, word_list)

# This section's logic is specific to the yellow letters. The first pass removes all words where the yellow letter and index matches the word. The second pass removes all the words that do not contain one of the yellow letters.  The third pass reduces the list to only words with all the yellow letters.
def fRemoveYellowLetters(yellow_letters, word_list):
    # Handles the blank list logic
    if not yellow_letters:
        return word_list
    # SET conversion was done to speed up the process
    wordlist = set(word_list)
    # The upper was added to normalize the data between the two list files and account for data entry in case users preferred to enter in lower case vs upper case
    # ISALPHA was used to remove the "index" number from the yellow_letters vaiable
    yllist = [c for c in yellow_letters.upper() if c.isalpha()]
    wordlist_to_delete = []
    # This section loops based on the length of the list and iterates by 2 each loop
    for ln in range(0,len(yellow_letters),2):
        yllwword = yellow_letters[0].upper()
        # The -1 is to offset the index for Python starting as 0 where users woudl naturally start at 1 when entering the data
        pos = int(yellow_letters[1])-1
        # This section loops through each word in the SET and to the ALPHA character and the index.  For example if the yllwword = 'A' and pos = '2' then all words with 'A' as the second character are added to the list to be removed.
        for word in wordlist:
            if yllwword == word[pos]:
                wordlist_to_delete.append(word)
        # This "resets" the list by remove the first two items.'a1b2c3' becomes 'b2c3'.  This simplifies the previous logic where alpha and number indexes remains the same for each loop without having to additional logic.
        yellow_letters = yellow_letters[2:]
    # This section identifies all words that do not contain the yellow letters to be removed.
    for word in wordlist:
        if not any(letter in word for letter in yllist):
            # Adds the identifed words to wordlist_to_delete list
            wordlist_to_delete.append(word)
    new_list = fRemove_from_list(wordlist_to_delete, word_list)
    # This section loops through the new list with all the previous words removed and idetifies only the words that contain ALL the yellow letters.
    def fValidWordsY(ltr, llist):
        words_to_return = []
        for word in llist:
            if ltr.upper() in word:
                words_to_return.append(word)
        return words_to_return
    for i in yllist:
        new_list = fValidWordsY(i,new_list)
    # Returns a list of words that contain ALL the yellow letters
    return new_list

# This section's logic is speific to the green letters.  
def fRemoveGreeLetters(green_letters, word_list):
    # Handles the blank list logic
    if not green_letters:
        return word_list
    wordlist = set(word_list)
    def fValidWords(ltr, indx, llist):
        words_to_return = []
        # This function check the ALPHA and INDEX from the grren_letters against the word.  If it matches the word is added to words_to_return
        for word in llist:
            if ltr.upper() == word[indx]:
                words_to_return.append(word)
        return words_to_return
    # This section loops based on the length of the list and iterates by 2 each loop
    for ln in range(0,len(green_letters),2):
        grnwords = green_letters[0].upper()
        pos = int(green_letters[1])-1
        wordlist = fValidWords(grnwords, pos, wordlist)
        # This "resets" the list by remove the first two items.'a1b2c3' becomes 'b2c3'.  This simplifies the previous logic where alpha and number indexes remains the same for each loop without having to additional logic.
        green_letters = green_letters[2:]
    print(f'Words Remaining: {len(wordlist)}') 
    # Returns all words with the matching letter/index 
    return wordlist

# This is the 6.1 version of the random word.
# This section takes the current list of words.  Creates a Counter based on the instances of each letter in the words and then chooses a random for from a new list of words containing the most_common letter.
# The goal of this is to find a random word that will maximize the effectiveness of the guess.
def fGetRandom(wordlist):
    if not wordlist:
        return wordlist
    # Converts to LIST when the passed variable had previously been converted to a SET when running through the Letter Color functions
    wordlist = list(wordlist)
    # Creates list of each letter in each word
    alpha = [ltr for word in wordlist for ltr in word]
    # Counts the number of instances of each letter asn sorts them in descending order via .most_common()
    counter = dict(Counter(alpha).most_common())
    # Pulls the first instance/row in the dictionary which would be the letter with the highest number of instances remaining in the list
    focus_letter = str(next(iter(counter.keys())))
    # Creates a list of words containing the focus_letter
    for_random = [word for word in wordlist if focus_letter in word]
    # Updates the list to focus on words with a LEN of 5 effectively removing any words with repeated letters.
    # TODO retool this section to prioritze LEN of 5, but drop to LEN 4 if 5 is not available.
    for_random = [word for word in for_random if len(set(word)) >= 5]
    if not for_random:
        for_random = wordlist  # fallback if filter is too aggressive
    print(f'Next Word: {random.choice(for_random)}')

# This section cleans the BlackLetter variable removing all letter that appears in the Yellow or Red string
def fPassVariables(b, y, g):
    # Removes letter indexes
    y = [l for l in y if l.isalpha()]
    g = [l for l in g if l.isalpha()]
    if not g:
        return b
    # Combines Yellow and Green strings into SET and uses RE.SUB to loop through the LIST SET and substitutes it with a '' in the b variable
    b = re.sub(f"[{''.join(set(y + g))}]", '', b)
    return str(b)

# This cleans the variables and scrubs the list
def fLoop(black, yellow, green, word_list):
    black = fPassVariables(black, yellow, green)
    word_list = fRemoveBlackLetters(black, word_list)
    word_list = fRemoveYellowLetters(yellow, word_list)
    word_list = fRemoveGreeLetters(green, word_list)
    return word_list