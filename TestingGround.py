import pandas as pd

print(pd. __version__)




"""
Working with Files 
You are given a books.txt file, which includes book titles, each on a separate line.

Create a program to output how many words each title contains, in the following format:
Line 1: 3 words
Line 2: 5 words
...

Make sure to match the above mentioned format in the output.
To count the number of words in a given string, you can use the split() function, or, alternatively, count the number of spaces (for example, if a string contains 2 spaces, then it contains 3 words).
"""

with open("/usercode/files/books.txt") as f:
   #your code goes here
   # .split() or .isspace()
   # The readlines() method returns a list containing each line
   # in the file as a list item.
   temp = f.readlines()
   for i in range(len(temp)):
    print("Line", str(i+1) + ":", len(temp[i].split()), "words")