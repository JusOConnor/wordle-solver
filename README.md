## Wordle Solver
This originally started as project to learn how to work with data in Python.  The 'Word List.csv' file was scrapped from the official Wordle site a few years ago.  The 'Word List_2.csv' was added later on the chance additional words were added to the list.  At the bottom of the 'Wordle.ipynb' file there is a function that loads both files into a new list, this hasn't been necessary yet as all tested words from the main site and archive have appeared in theme original 'Word List.csv'

**Wordle.ipynb Usage:**
1. **Import Function.** \
    This imports the function from the Function/Wordle_Functions.py file. 

2. **Generate list of words from the main 'Word List.csv' file.** \
    There are two list that can be loaded.  'Word List.csv' is the original that was scraped from the official webiste.  There is another cell that will load an additional list that contains additional words in case they're added later. 

3. **Get random word from list of remaining possibilities.** \
    This finds the most common letter in the available words and then randomly selects a word with 5 unique letters.  This is meant to maximize each guess. 

***The loop:*** 

4. **Enter your guess.** \
    This is the section where you plug in the results of the guess.  Once the variables have been populated ren the cell. 

        Black = 'like' | Enter the letters that appear black.  Make sure the letters do not also appear Yellow or Green as this will be removing them from the list. 

        Yellow = 't1h2i3s4 | Enter the letters and position for each one.  You do not need to enter these in a specific order beside (letter_number). | 's4i3h2t1' will have the same results. 

        Green = 'w1a2y3 | Enter the letters and position for each one.  You do not need to enter these in a specific order beside (letter_number). | 'y3a2w1' will have the same results. 

    *Note:* \
        You do not need to clear each variable between guesses. \
        If you run out of words before the puzzle is solved, it's possible you may have entered the wrong letters.  Double check the Black letters don't appear Yellow or Red anywhere else. \
    At this point make another guess or utilize the 'Get random word' function.

5. **print(word)** \
    This section is intended for you to see the contents of the list.  It's helpful for validating the remaining words in cases where the Random Word function keeps returning the same word/s or if you accidently plugged the wrong information into the variable. 

6. **Generate list of words from combined list** \
    This loads both word lists into the word_list variable.  Please note, this will override the previously generated word_list