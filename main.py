#Tasks:
#Place ships on the field
#Make an empty 7*7 field displayed on the console
from os import system
import time
import random
import sys

a = input("Please enter your name ")

m = 7
n = 7
a = [["o"] * m] * n
for row in a:
    print(' '.join([str(elem) for elem in row]))

coordinate1 = input("Enter the 1st coordinate")
print(coordinate1)
coordinate2 = input("Enter the 2nd coordinate ")
print(coordinate2)
