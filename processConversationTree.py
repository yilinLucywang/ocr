import json
import sys
class TreeNode:
    def __init__(self, input_utters, input_context):
        self.utters = input_utters
        #[0. Upper; 1. Lower]
        self.context = input_context
        self.compareKey = input_context[0] + input_utters + input_context[1]

    def minimumEditDistance(self, word1, word2): 
        n1 = len(word1)
        n2 = len(word2)
        dp1 = [0] * (n2 + 1)
        dp2 = [0] * (n2 + 1)
        dp1[0] = 0
        for j in range(1, n2 + 1):
            dp1[j] = j
        for i in range(1, n1 + 1):
            dp2[0] = i
            for j in range(1, n2 + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp2[j] = dp1[j - 1]
                else:
                    dp2[j] = min(dp1[j], dp2[j - 1], dp1[j - 1]) + 1
            dp1, dp2 = dp2, dp1
        return dp1[n2]

    #context 90% match,
    def nodeMatch(self, otherNode):
        isSame = True
        contentDiff = self.minimumEditDistance(otherNode.compareKey, self.compareKey)/len(self.compareKey)
        if(contentDiff > 0.3):
            isSame = False
        return isSame


#Note: bot starts and bot ends
#bot one sentence
#user one sentence
def makeBranch(words):
    #state 0 == no content no context
    #state 1 == prev content no content 
    #state 2 == prev content and content
    state = 0
    wordList = words.split("\n")
    curPrev = ''
    curPost = ''
    curContent = ''
    rootNode = TreeNode('root', ['root', 'root'])
    branch = [rootNode]
    for i in range(len(wordList)):
        #modify the state machine
        if(state == 0):
            curPrev = wordList[i]
            state = 1
        elif(state == 1):
            curContent = wordList[i]
            state = 2
        elif(state == 2): 
            curPost = wordList[i]
            state = 3
        elif(state == 3): 
            newNode = TreeNode(curContent, [curPrev, curPost])
            curPrev = wordList[i]
            state = 1
            branch.append(newNode)
    return branch

#root dictionary
#branch is just one list
def merge(root, branches):
    for branch in branches:
        current_level_ptr = root
        for i in range(len(branch)):
            hasMatch = False
            matchedKey = None

            for k, v in current_level_ptr.items():
                if(branch[i].nodeMatch(k)):
                    hasMatch = True
                    matchedKey = k
            if(not hasMatch):
                current_level_ptr[branch[i]] = {}
                matchedKey = branch[i]
            #TODO: program is lost in the following line
            current_level_ptr = current_level_ptr[matchedKey]
    return root

#Making json format
def printTree(treeDictionary):
    res = []
    for k, v in treeDictionary.items():
        d = {}
        d['utters'] = k.utters
        d['children'] = printTree(v)
        res.append(d)
    return res

def main(): 
    path_str = sys.argv[1]
    img_paths = path_str.split(" ")
    img_paths.pop()

    branches = []
    for i in range(len(img_paths)): 
        f = open(img_paths[i], "r")
        branch = makeBranch(f.read())
        branches.append(branch)
    treeDictionary = {}
    merge(treeDictionary, branches)
    toPrint = json.dumps(printTree(treeDictionary))
    print(toPrint)
main()










