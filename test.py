import random as r
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

number = r.randint(0, 9)
character = r.choice(["~","!","@","#","$","%","^","&","*","(",")","-","+"])
letter = r.choice(alphabet).upper()

print(str(number) + character + letter)
