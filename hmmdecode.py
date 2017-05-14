import itertools
import json
import pprint
import re
import sys
import timeit
import math
import operator
import copy
import io
import os
import codecs
import time
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

transitionList = {}
emissionListReversed = {}
transitionStates = {}


def createPOSTags(wordsList, transitionStates, transitionList, emissionListReversed):
    probability = {}
    backpointer = {}
    startDict = transitionList["start"]
    firstWord = wordsList[0].lower()
    for eachStateIndex, eachState in enumerate(startDict):
        if(firstWord not in emissionListReversed):
            probability[eachState] = {0: startDict.get(eachState) + 0}
        elif(firstWord in emissionListReversed and eachState in emissionListReversed.get(firstWord)):
            eachStateTransitionList = emissionListReversed.get(firstWord)
            probability[eachState] = {0: startDict.get(eachState) + eachStateTransitionList.get(eachState)}
        else:
            probability[eachState] = {0: -10000}
        backpointer[eachState] = {0: "start"}
    for eachWordToTagIndex, eachWordToTag in enumerate(wordsList):
        eachWordToTag = eachWordToTag.lower()
        if(eachWordToTagIndex > 0):
            prevStateDict = {}
            prevStateDict = probability.copy()
            prevStateDict = {
                key: value[eachWordToTagIndex - 1]
                for key, value in prevStateDict.items() if (eachWordToTagIndex - 1) in value.keys()
            }
            for currentStateIndex, currentState in enumerate(transitionStates):
                tempPrevState = {}
                tempPrevState = prevStateDict.copy()
                if(eachWordToTag not in emissionListReversed):
                    for prevStateKey, prevStateValue in enumerate(tempPrevState):
                        tempPrevState[prevStateValue] = tempPrevState[prevStateValue] + transitionList[prevStateValue][currentState]
                else:
                    eachStateTransitionList = emissionListReversed.get(eachWordToTag)
                    for prevStateKey, prevStateValue in enumerate(tempPrevState):
                        tempPrevState[prevStateValue] = tempPrevState[prevStateValue] + transitionList[prevStateValue][currentState]
                        if(currentState in eachStateTransitionList):
                            tempPrevState[prevStateValue] = tempPrevState[prevStateValue] + eachStateTransitionList.get(currentState)
                        else:
                            tempPrevState[prevStateValue] =  -10000
                maxProbability = max(tempPrevState.items(), key=operator.itemgetter(1))
                probability[currentState].update({eachWordToTagIndex : maxProbability[1]})
                backpointer[currentState].update({eachWordToTagIndex : maxProbability[0]})
    tempList = {}
    for eachIndex, eachValue in probability.items():
        tempList[eachIndex] = eachValue.get(len(wordsList) - 1)

    most_probable_state = max(tempList.items(), key=operator.itemgetter(1))[0]
    sequenceList = [most_probable_state]
    count = len(wordsList) - 1
    while (count > 0):
        most_probable_state = backpointer[most_probable_state][count]
        sequenceList = [most_probable_state] + sequenceList
        count = count - 1
    taggedSentence = ""
    for k, eachWordToTag in enumerate(wordsList):
        taggedSentence += eachWordToTag + "/" + sequenceList[k] + " "
    return taggedSentence

def main():
    for index, arg in enumerate(sys.argv):
        if index == 1:
            with io.open(arg, encoding="utf8") as text_file:
                test_text_list = text_file.readlines()
            test_text_list = [x.strip() for x in test_text_list]

    tempList = json.load(io.open("hmmmodel.txt", encoding="utf8"))
    transitionList = tempList["transitionList"]
    emissionListReversed = tempList["emissionListReversed"]
    transitionStates = list(transitionList.keys())
    transitionStates.remove("start")
    open('hmmoutput.txt', 'w').close()
    outputFile = io.open('hmmoutput.txt', 'a', encoding="utf8")
    for index, eachTestText in enumerate(test_text_list):
        eachTestText = eachTestText.split()
        taggedSentence = createPOSTags(eachTestText, transitionStates, transitionList, emissionListReversed)
        outputFile.write(taggedSentence + "\n")
    outputFile.close()

if __name__ == '__main__':
    print(timeit.timeit(lambda: main(), number=1))
