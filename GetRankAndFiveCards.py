valueList = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
suitList = ["D", "C", "H", "S"]

reverseValueList = list(valueList)
reverseValueList.reverse()


#Hand Modifiers ######################################################################
def replacePicturesAndReturnValueHandList(handList):
    valueHandList = []
    for card in handList:
        valueHandList.append(card[0])

    for i, card in enumerate(valueHandList):
        if card == "J":
            valueHandList[i] = 11
        if card == "Q":
            valueHandList[i] = 12
        if card == "K":
            valueHandList[i] = 13
        if card == "A":
            valueHandList[i] = 14
    return valueHandList


def returnValueHandLists(handList):
    valueHandList = []
    for card in handList:
        valueHandList.append(card[0])
    return valueHandList

#determine rank########################################################################


def isFlush(handList):
    orderedHandList = []
    suitHandList = []
    for card in handList:
        suitHandList.append(card[1])

    isFlush = False
    for suit in suitList:
        if suitHandList.count(suit) >= 5:
            isFlush = True
            valueHandList = returnValueHandLists(handList)
            for value in reverseValueList:
                for card in handList:
                    if card[0] == value and card[1] == suit:
                        orderedHandList.append(card)
    return isFlush, orderedHandList


def isStraight(handList):
    orderedHandList = []
    valueHandList = replacePicturesAndReturnValueHandList(handList)

    isStraight = False
    for i in range(14, 5, -1):
        if all(elem in valueHandList for elem in range(i, i-5, -1)):
            isStraight = True
            straightRange = valueList[i-6: i-1]
            straightRange.reverse()
            # straightRange.reverse()
            for value in straightRange:
                for card in handList:
                    if card[0] == value:
                        orderedHandList.append(card)
                        break
    wheelStraight = [14, 2, 3, 4, 5]
    if isStraight == False:
        if all(elem in valueHandList for elem in wheelStraight):
            isStraight = True
            for value in ["A", 2, 3, 4, 5]:
                for card in handList:
                    if card[0] == value:
                        orderedHandList.append(card)
                        break

    return isStraight, orderedHandList[0:5]


def isFourOfAKind(handList):
    orderedHandList = []
    valueHandList = returnValueHandLists(handList)
    newHandList = list(handList)

    isFourOfAKind = False
    for value in valueList:
        if valueHandList.count(value) >= 4:
            isFourOfAKind = True

            for card in newHandList:
                if card[0] == value:
                    orderedHandList.append(card)

            for card in orderedHandList:
                newHandList.remove(card)

            for value in reverseValueList:
                for card in newHandList:
                    if card[0] == value:
                        orderedHandList.append(card)

    return isFourOfAKind, orderedHandList[0:5]


def isThreeOfAKind(handList):
    orderedHandList = []
    valueHandList = returnValueHandLists(handList)
    newHandList = list(handList)

    isThreeOfAKind = False
    for value in valueList:

        if valueHandList.count(value) >= 3:
            isThreeOfAKind = True

            for card in newHandList:
                if card[0] == value:
                    orderedHandList.append(card)

            for card in orderedHandList:
                newHandList.remove(card)

            for value in reverseValueList:
                for card in newHandList:
                    if card[0] == value:
                        orderedHandList.append(card)

    return isThreeOfAKind, orderedHandList[0:5]


def isFullHouse(handList):
    orderedHandList = []
    valueHandList = list(returnValueHandLists(handList))
    newHandList = list(handList)

    isThree = False
    isPair = False

    for value in reverseValueList:

        if valueHandList.count(value) >= 3:
            isThree = True
            for card in newHandList:
                if card[0] == value:
                    orderedHandList.append(card)
    for card in orderedHandList:
        newHandList.remove(card)

    for value in reverseValueList:
        if valueHandList.count(value) >= 2:
            isPair = True
            for card in newHandList:
                if card[0] == value:
                    orderedHandList.append(card)

    return isThree and isPair, orderedHandList[0:5]


def countPairs(handList):
    newHandList = list(handList)
    orderedHandList = []
    valueHandList = returnValueHandLists(handList)

    pairCount = 0

    for value in reverseValueList:
        if valueHandList.count(value) >= 2:
            for card in newHandList:
                if card[0] == value:
                    orderedHandList.append(card)
            pairCount += 1
        if len(orderedHandList) > 4:
            break

    for card in orderedHandList:
        newHandList.remove(card)

    for value in reverseValueList:
        for card in newHandList:
            if card[0] == value:
                orderedHandList.append(card)

    return pairCount, orderedHandList[0:5]


def isStraightFlush(handList):
    orderedHandList = []

    suitHandList = []
    for card in handList:
        suitHandList.append(card[1])

    isStraightFlush = False
    for suit in suitList:
        if suitHandList.count(suit) >= 5:
            newHandList = list(handList)
            for card in newHandList:
                if card[1] != suit:
                    newHandList.remove(card)
            if isStraight(newHandList)[0]:
                isStraightFlush = True

                for value in reverseValueList:
                    for card in handList:
                        if card[0] == value and card[1] == suit:
                            orderedHandList.append(card)

    return isStraightFlush, orderedHandList[0:5]


def returnRank(handList):
    tempHand = []
    fiveCards = []

    rank = 1
    for value in reverseValueList:
        for card in handList:
            if card[0] == value:
                fiveCards.append(card)
                if len(fiveCards) >= 5:
                    break

    tempHand = countPairs(handList)
    if tempHand[0] >= 2:
        rank = 3
        fiveCards = tempHand[1]
    elif tempHand[0] >= 1:
        rank = 2
        fiveCards = tempHand[1]
    tempHand = isThreeOfAKind(handList)
    if tempHand[0]:
        rank = 4
        fiveCards = tempHand[1]
    tempHand = isStraight(handList)
    if tempHand[0]:
        rank = 5
        fiveCards = tempHand[1]
    tempHand = isFlush(handList)
    if tempHand[0]:
        rank = 6
        fiveCards = tempHand[1]
    tempHand = isFullHouse(handList)
    if tempHand[0]:
        rank = 7
        fiveCards = tempHand[1]
    tempHand = isFourOfAKind(handList)
    if tempHand[0]:
        rank = 8
        fiveCards = tempHand[1]
    tempHand = isStraightFlush(handList)
    if tempHand[0]:
        rank = 9
        fiveCards = tempHand[1]

    return rank, fiveCards[0:5]


def convertToUTFCardList(cardList):
    UTFDiamondList = ['🃂', '🃃', '🃄', '🃅', '🃆',
                      '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎', '🃁']
    UTFClubList = ['🃒', '🃓', '🃔', '🃕', '🃖',
                   '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞', '🃑']
    UTFHeartList = ['🂲', '🂳', '🂴', '🂵', '🂶',
                    '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾', '🂱']
    UTFSpadeList = ['🂢', '🂣', '🂤', '🂥', '🂦',
                    '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮', '🂡']

    UTFCardList = []

    reverseReverseValueList = list(reverseValueList)
    reverseReverseValueList.reverse()

    for card in cardList:
        if card[1] == "D":
            for i, value in enumerate(reverseReverseValueList):
                if value == card[0]:
                    UTFCardList.append(UTFDiamondList[i])
        if card[1] == "C":
            for i, value in enumerate(reverseReverseValueList):
                if value == card[0]:
                    UTFCardList.append(UTFClubList[i])
        if card[1] == "H":
            for i, value in enumerate(reverseReverseValueList):
                if value == card[0]:
                    UTFCardList.append(UTFHeartList[i])
        if card[1] == "S":
            for i, value in enumerate(reverseReverseValueList):
                if value == card[0]:
                    UTFCardList.append(UTFSpadeList[i])

    return UTFCardList

    # below is temp for testing
# for i in range(0, 20):

#     generateTemp = generateNineCardsList()[0:7]
#     for card in generateTemp:
#         print(f"{card[0]}{card[1]}", end=" ")
#     print()
#     print(" ".join(convertToUTFCardList(generateTemp)))
#     temp = returnRank(generateTemp)

#     if temp[0] == 1:
#         print("1. High Card")
#     if temp[0] == 2:
#         print("2. Pair")
#     if temp[0] == 3:
#         print("3. 2 Pair")
#     if temp[0] == 4:
#         print("4. 3 of a Kind")
#     if temp[0] == 5:
#         print("5. Straight")
#     if temp[0] == 6:
#         print("6. Flush")
#     if temp[0] == 7:
#         print("7. Full House")
#     if temp[0] == 8:
#         print("8. Four of a Kind")
#     if temp[0] == 9:
#         print("9. Straight Flush")

#     for card in temp[1]:
#         print(f"{card[0]}{card[1]}", end=" ")

#     print("\n\n")
