x = [91, 56, 50, 44, 32, 49, 48, 49, 44, 32, 57, 57, 44, 32, 49, 48, 49, 44, 32, 49, 49, 50, 44, 32, 49, 49, 54, 44, 32,
     49, 48, 53, 44, 32, 49, 49, 49, 44, 32, 49, 49, 48, 93]


chred = map(chr, x)

result = []
print chred
chred = eval("".join(chred))
print chred
print map(chr, chred)

