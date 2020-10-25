import string

f = open("locations.txt", "w")
alphabet = string.ascii_uppercase[0:8]

for x in range(8,0,-1):
    for letter in alphabet:
        f.write(letter+str(x)+"\n")
