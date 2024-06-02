import trans
import cul
import sys
import os


# try:
argv = sys.argv[1:]
#     try:
with open(argv[0]) as f:
    sentence = f.read()
    # except:
    #     if argv != []:
    #         sentence = ' '.join(argv)
    #     else:
    #         sentence = "To @ explore strange new worlds,\nTo seek out new life and new civilizations?"
m, w2n, n2w=trans.text2matrix(sentence)
# except:
#     m, w2n, n2w=trans.text2matrix()
G = trans.matrix2graph(n2w, m)
trans.showDirectedGraph(G)
mycul = cul.cul(G, m, w2n, n2w)
bridge = input('please enter two word to get word brideg\n')
try:
    word1,word2=bridge.split()
except:
    print('wrong Input!\nUse Default input:"new" and "and"')
    word1 = 'new'
    word2 = 'and'
finally:
    out = mycul.queryBridgeWords(word1, word2)
print(out)
origintext = input("Please enter a sentence:\n")
out2 = mycul.generateNewText(origintext)
print(out2)

wordlength = input("Please enter One or Two word(s) to calculate distance!\n")
# try:
#     length,path = mycul.calcShortestPath(wordlength.split())
#     print(length,path)
# except:
outsentence = mycul.calcShortestPath(wordlength.split())
print(outsentence)

# length,path = mycul.calcShortestPath('to')
# print(length,path)
out4 = mycul.randomWalk()
print(out4)