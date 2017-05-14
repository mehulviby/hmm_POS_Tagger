import json
import pprint
import re
import sys
import time
import timeit
import collections
import math
import io

transitionList = {}
transitionListSum = {}
emissionList = {}
emissionListReversed = {}


def createTransitionList(eachTrainList, transitionListSum, transitionList, emissionListReversed ):
    for index, currentPOS in enumerate(eachTrainList):
        currentTag = currentPOS[-3:][1:]
        currentWord = currentPOS[:-3].lower()
        transitionListSum[currentTag] = transitionListSum.get(currentTag, 0) + 1

        if (index == 0):
            if ("start" not in transitionList):
                transitionList["start"] = {currentTag: 0}
            if (currentTag not in transitionList["start"]):
                transitionList["start"].update({currentTag: 1})
            else:
                transitionList["start"][currentTag] = transitionList.get("start").get(currentTag) + 1
        if (index != (len(eachTrainList) - 1)):
            nextTag = eachTrainList[index + 1][-3:][1:]
            if (currentTag not in transitionList):
                transitionList[currentTag] = {nextTag: 0}
            if (nextTag not in transitionList[currentTag]):
                transitionList[currentTag].update({nextTag: 1})
            else:
                transitionList[currentTag][nextTag] = transitionList.get(currentTag).get(nextTag) + 1

        if (currentWord not in emissionListReversed):
            emissionListReversed[currentWord] = {currentTag: 0}
        if (currentTag not in emissionListReversed[currentWord]):
            emissionListReversed[currentWord].update({currentTag: 1})
        else:
            emissionListReversed[currentWord][currentTag] = emissionListReversed.get(currentWord).get(currentTag) + 1
    return transitionList, emissionListReversed

def main():
    for index, arg in enumerate(sys.argv):
        if index == 1:
            with io.open(arg, encoding="utf8") as text_file:
                train_text_list = text_file.readlines()
            train_text_list = [x.strip() for x in train_text_list]
    dummy = {}
    for index, eachTrainText in enumerate(train_text_list):
        eachTrainText = eachTrainText.split()
        createTransitionList(eachTrainText, transitionListSum, transitionList, emissionListReversed)

    smoothingSet = dict.fromkeys(transitionListSum, 1)

    for key, eachTransition in transitionList.items():
        diff = set(smoothingSet).difference(eachTransition)

        if (diff != 0):
            transitionList[key] = {
                x: eachTransition.get(x, 0) + smoothingSet.get(x, 0)
                for x in set(eachTransition).union(smoothingSet)
            }

    for key, value in transitionList.items():
        totalSum = float(sum(value.values()))
        transitionList[key].update({k: math.log(v / totalSum) for k, v in value.items()})

    for key, value in emissionListReversed.items():
        emissionListReversed[key].update({k: math.log(v / float(transitionListSum[k])) for k, v in value.items()})

    totalList = {}
    totalList["transitionList"] = transitionList
    totalList["emissionListReversed"] = emissionListReversed
    open('hmmmodel.txt', 'w').close()
    with io.open("hmmmodel.txt",'w',encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(totalList, ensure_ascii=False)))

if __name__ == '__main__':
    main()
