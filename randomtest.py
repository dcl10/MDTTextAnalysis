file = open("cleaned.txt", "r")
text = file.read()
lines = text.split(sep="\n")

for line in lines:
    print(line)