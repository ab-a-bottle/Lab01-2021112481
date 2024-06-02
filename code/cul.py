import re
import networkx as nx
import numpy as np
import random
import heapq
from pyparsing import Word


class cul(object):
    def __init__(self, G, Adj_Mat, word2node, node2word):
        super(cul, self).__init__()
        self.G = G
        self.M = Adj_Mat
        self.w2n = word2node
        self.n2m = node2word

    # find brdge word list,suppose that word1 and word2 are in the node list
    def queryBridgeWordList(self, word1: str, word2: str):
        wordlist=[]
        node1 = self.w2n[word1]
        node2 = self.w2n[word2]
        for i in range(len(self.w2n)):
            if self.M[node1][i]!=0 and self.M[i][node2]!=0:
                wordlist.append(self.n2m[i])
        return wordlist

    # String queryBridgeWords(String word1, String word2)：查询桥接词
    def queryBridgeWords(self, word1: str, word2: str):
        # turn query words into lower case
        Word1 = word1.lower()
        Word2 = word2.lower()
        # Case:Not in the node list
        if Word1 not in self.w2n or Word2 not in self.w2n:
            return f'No "{word1}" or "{word2}" in the graph!'
        # init bridge word list
        wordlist = self.queryBridgeWordList(Word1,Word2)
        #Case:no bridge word
        if len(wordlist)==0:
            return f'No bridge words from "{word1}" to "{word2}"!'
        #Cases:got bridge word
        elif len(wordlist)==1:
            return f'The bridge words from "{word1}" to "{word2}" is:{wordlist[0]}.'
        else:
            return f'The bridge words from "{word1}" to "{word2}" are:' + ' ,'.join(wordlist[:-1]) + f'and {wordlist[-1]}.'
    # String generateNewText(String inputText)：根据bridge word生成新文本

    def generateNewText(self, inputText: str):
        # In order to handel any possible cases, we use Try...except...finally structure
        try:
            # get all the word pair and find bridge word.if found add it into finally output
            words = inputText.lower().split()
            Words = inputText.split()
            out = ''
            i = 0
            # find the first word in our nodes
            while words[i] not in self.w2n:
                out += Words[i]
                out += ' '
                i += 1
            # find last words
            out += Words[i]
            out += ' '
            i += 1
            last =1
            while i in range(len(words)):
                if words[i] in self.w2n and last == 1:
                    wordlist = self.queryBridgeWordList(words[i-1],words[i])
                    if wordlist != []:
                        out += random.choice(wordlist)
                        out += ' '
                elif words[i] in self.w2n and last == 0:
                    last = 1
                elif words[i] not in self.w2n:
                    last = 0
                out += Words[i]
                out += ' '
                i += 1
            return out[:-1]
        except:
            pass
        finally:
            return out


    def Dijkstra(self, s):
        n = nx.number_of_nodes(self.G)
        dis = [100000] * n
        path = [[] for _ in range(n)]  # 添加路径存储
        vis = set()
        dis[s] = 0
        path[s].append(s)  # 路径初始化
        # priority_queue
        q = []
        heapq.heappush(q, (0, s))
        while q:
            dis_k, k = heapq.heappop(q)
            if k in vis:
                continue
            vis.add(k)
            for v in self.G.successors(k):
                weight = self.G.get_edge_data(k, v)['weight']
                if dis[v] > dis[k] + weight:
                    dis[v] = dis[k] + weight
                    path[v] = path[k] + [v]  # 更新路径
                if v not in vis:
                    heapq.heappush(q, (dis[v], v))
        return dis, path  # 返回距离和路径

    # String calcShortestPath(String word1, String word2)：计算两个单词之间的最短路径
    def calcShortestPath(self, word:str):
        if len(word) == 1:
            word1 = word[0].lower()
            if word1 not in self.w2n:
                return 'No word1 in the graph!'
            node1 = self.w2n[word1]
            dis, path = self.Dijkstra(node1)
            out = ''
            for i in range(len(path)):
                for j in range(len(path[i])):
                    path[i][j] = self.n2m[path[i][j]]
                out += f'Length:{dis[i]}\n' + '>'.join(path[i])+'\n'
            return out
        elif len(word) >= 3:
            return 'Too many words in the input'
        word1 = word[0].lower()
        word2 = word[1].lower()
        if word1 not in self.w2n or word2 not in self.w2n:
            return 'No word1 or word2 in the graph!'
        node1 = self.w2n[word1]
        node2 = self.w2n[word2]
        dis, path = self.Dijkstra(node1)
        for i in range(len(path)):
            for j in range(len(path[i])):
                path[i][j] = self.n2m[path[i][j]]
        out = f'Length:{dis[node2]}\n' + '>'.join(path[node2])+'\n'
        return out
    # String randomWalk()：随机游走
    def randomWalk(self):
        #赋初值
        nodes = list(self.G.nodes())
        edges = list(self.G.edges())
        ans_list = []
        vis = {edge: 0 for edge in edges}
        #随机一个点
        start_node = random.choice(nodes)
        ans_list.append(self.n2m[start_node])
        while True:
            #随机出边
            out_edges = list(self.G.out_edges(start_node))
            #没有出边
            if not out_edges:
                break
            random_edge = random.choice(out_edges)
            start_node = random_edge[1]
            ans_list.append(self.n2m[start_node])
            #该边被遍历过一次
            if vis[random_edge] == 1:
                break
            vis[random_edge] = 1
        return ' '.join(ans_list)